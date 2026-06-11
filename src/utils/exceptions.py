class SEIPError(Exception):
    """Base exception for SEIP ETL errors."""

class ExtractError(SEIPError):
    """Raised when source extraction fails."""

class ValidationError(SEIPError):
    """Raised when validation fails."""

class LoadError(SEIPError):
    """Raised when PostgreSQL loading fails."""

class ConfigurationError(SEIPError):
    """Raised when environment/configuration is invalid."""
