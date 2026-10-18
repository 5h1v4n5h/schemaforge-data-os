import json
import re
from typing import Dict, Any, List, Union
from collections import defaultdict

class InputProfileAnalyzer:
    """Stage 1: Profiles messy input datasets to compress structural metadata for the LLM."""

    @staticmethod
    def detect_pii(val: Any) -> bool:
        if not isinstance(val, str):
            return False
        # Email
        if re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', val):
            return True
        # Phone
        if re.search(r'^\+?[0-9\s-]{10,15}$', val):
            return True
        # Credit Card
        if re.search(r'^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$', val):
            return True
        return False

    @staticmethod
    def mask_pii(val: Any) -> Any:
        if isinstance(val, str) and InputProfileAnalyzer.detect_pii(val):
            return "[REDACTED_PII]"
        return val

    @classmethod
    def profile_json_records(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Profiles a list of JSON dictionaries, detecting polymorphic keys and types."""
        if not records:
            return {"error": "Empty records"}

        field_types = defaultdict(set)
        field_nulls = defaultdict(int)
        field_samples = defaultdict(list)
        polymorphic_keys = set()

        total = len(records)

        for rec in records:
            if not isinstance(rec, dict):
                continue
            for k, v in rec.items():
                masked_v = cls.mask_pii(v)
                t_name = type(v).__name__
                field_types[k].add(t_name)
                if v is None:
                    field_nulls[k] += 1
                elif len(field_samples[k]) < 3:
                    field_samples[k].append(masked_v)

        for k, types in field_types.items():
            if len(types) > 1:
                polymorphic_keys.add(k)

        summary = {
            "total_records": total,
            "fields_detected": len(field_types),
            "polymorphic_fields": list(polymorphic_keys),
            "field_catalog": {}
        }

        for k in sorted(field_types.keys()):
            summary["field_catalog"][k] = {
                "types_observed": list(field_types[k]),
                "null_count": field_nulls[k],
                "null_ratio": round(field_nulls[k] / total, 3),
                "samples": field_samples[k],
                "is_polymorphic": k in polymorphic_keys
            }

        return summary

    @classmethod
    def generate_compact_prompt_context(cls, raw_data_str: str, target_schema_ddl: str) -> Dict[str, Any]:
        """Generates a compressed 4KB profile context for Gemini 1.5 Pro."""
        try:
            parsed = json.loads(raw_data_str)
            if isinstance(parsed, list):
                profile = cls.profile_json_records(parsed)
                sample_rows = parsed[:4]
            else:
                profile = cls.profile_json_records([parsed])
                sample_rows = [parsed]
        except Exception:
            profile = {"raw_preview": raw_data_str[:1000]}
            sample_rows = []

        return {
            "input_profile": profile,
            "target_schema": target_schema_ddl.strip(),
            "sample_input_rows": sample_rows
        }

    @classmethod
    def profile_multi_source(
        cls,
        sources: Dict[str, Union[str, List[Dict[str, Any]]]],
        target_schema_ddl: str
    ) -> Dict[str, Any]:
        """Profiles multiple heterogeneous sources simultaneously and detects candidate join/mastering keys."""
        source_profiles = {}
        sample_rows_by_source = {}
        id_candidates_by_source = defaultdict(list)
        email_domains_by_source = defaultdict(set)

        for src_name, data in sources.items():
            parsed = data if isinstance(data, list) else (json.loads(data) if isinstance(data, str) else [data])
            source_profiles[src_name] = cls.profile_json_records(parsed)
            sample_rows_by_source[src_name] = parsed[:3]

            # Inspect potential keys for cross-source linkage
            for r in parsed:
                if isinstance(r, dict):
                    for k, v in r.items():
                        if any(term in k.lower() for term in ["id", "ref", "code", "header"]):
                            if isinstance(v, (str, int)) and str(v) not in id_candidates_by_source[src_name]:
                                id_candidates_by_source[src_name].append(str(v))
                        # Check nested dicts
                        if isinstance(v, dict):
                            for nk, nv in v.items():
                                if "email" in nk.lower() and isinstance(nv, str) and "@" in nv:
                                    domain = nv.split("@")[-1].lower()
                                    email_domains_by_source[src_name].add(domain)
                                if "domain" in nk.lower() and isinstance(nv, str):
                                    email_domains_by_source[src_name].add(nv.lower())

        # Cross-source key overlaps
        cross_source_links = []
        source_names = list(sources.keys())
        for i in range(len(source_names)):
            for j in range(i + 1, len(source_names)):
                s1, s2 = source_names[i], source_names[j]
                
                # Check ID overlap
                s1_ids = set(id_candidates_by_source[s1])
                s2_ids = set(id_candidates_by_source[s2])
                id_overlap = s1_ids.intersection(s2_ids)
                
                # Check domain overlap
                dom_overlap = email_domains_by_source[s1].intersection(email_domains_by_source[s2])

                if id_overlap:
                    cross_source_links.append({
                        "source_a": s1,
                        "source_b": s2,
                        "link_type": "EXACT_ORDER_OR_RECORD_ID",
                        "matching_samples": list(id_overlap)[:3]
                    })
                if dom_overlap:
                    cross_source_links.append({
                        "source_a": s1,
                        "source_b": s2,
                        "link_type": "SHARED_CORPORATE_DOMAIN",
                        "matching_domains": list(dom_overlap)[:3]
                    })

        return {
            "multi_source_profiles": source_profiles,
            "detected_cross_links": cross_source_links,
            "target_schema": target_schema_ddl.strip(),
            "sample_rows_by_source": sample_rows_by_source
        }
