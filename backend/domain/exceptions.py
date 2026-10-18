"""
Domain Layer: Typed domain exceptions.
"""

class DomainException(Exception):
    """Base domain exception."""
    pass

class SchemaDriftException(DomainException):
    """Raised when incoming payload violates formal schema expectations."""
    def __init__(self, message: str, mutations: list = None):
        super().__init__(message)
        self.mutations = mutations or []

class InvariantViolationException(DomainException):
    """Raised when financial conservation or primary key invariants are violated."""
    def __init__(self, invariant_name: str, details: str):
        super().__init__(f"Invariant breach in {invariant_name}: {details}")
        self.invariant_name = invariant_name
        self.details = details

class PoisonPillQuarantineException(DomainException):
    """Raised when an unrecoverable poison-pill payload must be routed to DLQ."""
    def __init__(self, payload_id: str, reason: str):
        super().__init__(f"Payload {payload_id} routed to DLQ: {reason}")
        self.payload_id = payload_id
        self.reason = reason

class TenantIsolationException(DomainException):
    """Raised when tenant cryptographic boundaries or namespace barriers fail."""
    pass
