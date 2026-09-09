"""CADe_SIMU parser, generator and MCP bridge."""

from .codec import CadDocument, CadFormatError, CadRecord
from .model import DirectStarterSpec, PowerCircuitSpec

__all__ = [
    "CadDocument",
    "CadFormatError",
    "CadRecord",
    "DirectStarterSpec",
    "PowerCircuitSpec",
]
__version__ = "0.2.0"
