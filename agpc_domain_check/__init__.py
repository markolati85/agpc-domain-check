"""Free domain authentication check — no key, no account."""
from .client import CheckError, check

__all__ = ["check", "CheckError"]
__version__ = "1.0.0"
