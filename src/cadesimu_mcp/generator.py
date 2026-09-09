"""Compatibility facade for circuit generation.

Generation logic lives in :mod:`cadesimu_mcp.circuits`; this module keeps the
original public imports stable for callers created during the prototype phase.
"""

from .circuits.direct_starter import build_direct_starter_with_control
from .circuits.power import build_three_phase_power_circuit
from .model import DirectStarterSpec, PowerCircuitSpec

__all__ = [
    "DirectStarterSpec",
    "PowerCircuitSpec",
    "build_direct_starter_with_control",
    "build_three_phase_power_circuit",
]
