class AviMindError(Exception):
    """Base exception for AviMind SDK."""
    pass


class APIError(AviMindError):
    """Raised when the AviMind API returns an error."""
    pass


class ConnectionError(AviMindError):
    """Raised when the SDK cannot connect to the AviMind server."""
    pass


class ValidationError(AviMindError):
    """Raised when invalid data is provided."""
    pass