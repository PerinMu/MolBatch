class MolBatchError(Exception):
    """Base exception for MolBatch."""


class ConfigError(MolBatchError):
    """Raised when configuration loading or validation fails."""


class PlanError(MolBatchError):
    """Raised when an execution plan cannot be created."""


class BackendError(MolBatchError):
    """Raised when backend rendering fails."""


class RuntimeErrorExternal(MolBatchError):
    """Raised when launching an external viewer fails."""
