-- SchemaForge Gold Layer: Unified Master Data & Reconciled Financials

-- 1. Master Customer Dimension (Single Source of Truth / Golden Record)
CREATE TABLE `gold_analytics.dim_master_customer` (
  master_customer_id STRING NOT NULL,          -- e.g. MST_CUST_10421
  legal_company_name STRING,                  -- Survived from CRM / SAP
  primary_contact_name STRING NOT NULL,        -- Survived from Stripe / CRM
  primary_billing_email STRING NOT NULL,       -- Verified from Stripe
  corporate_domain STRING,                    -- e.g. acmecorp.com
  primary_country STRING NOT NULL,            -- ISO code or standardized name
  primary_postal_code STRING,
  thelook_user_id INT64,                      -- Source 1 Link
  stripe_customer_id STRING,                  -- Source 2 Link
  crm_company_name STRING,                    -- Source 3 Link
  total_support_tickets INT64 DEFAULT 0,
  average_csat_score FLOAT64,
  mastering_confidence_score FLOAT64 NOT NULL, -- e.g. 0.98
  mastering_rule_applied STRING               -- e.g. 'EXACT_EMAIL_DOMAIN_MATCH'
);

-- 2. Fact Reconciled Orders (Cross-System Financial & SLA Truth)
CREATE TABLE `gold_analytics.fact_reconciled_orders` (
  order_id STRING NOT NULL,                   -- e.g. ORD-88101
  master_customer_id STRING NOT NULL,         -- Foreign Key to dim_master_customer
  order_date DATE NOT NULL,
  thelook_gross_amount_usd FLOAT64 NOT NULL,  -- Storefront cart total
  stripe_charge_amount_usd FLOAT64 NOT NULL,  -- Actual amount billed (converted from cents)
  stripe_fee_amount_usd FLOAT64 NOT NULL,     -- Gateway fee (converted from cents)
  net_realized_revenue_usd FLOAT64 NOT NULL,  -- Stripe charge minus Stripe fee
  payment_brand STRING NOT NULL,              -- e.g. 'visa', 'mastercard'
  reconciliation_status STRING NOT NULL,      -- 'BALANCED', 'DISCREPANCY'
  delivery_sla_breached BOOLEAN NOT NULL      -- True if actual_delivery > promised_delivery
);
