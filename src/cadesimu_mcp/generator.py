"""Compatibility facade for circuit generation.

Generation logic lives in focused modules; this facade keeps the original
public imports stable for callers created during the prototype phase.
"""

from .circuits.direct_starter import build_direct_starter_with_control
from .circuits.power import build_three_phase_power_circuit
from .circuits.single_phase_lighting import build_single_phase_lighting_circuit
from .model import DirectStarterSpec, PowerCircuitSpec, SinglePhaseLightingSpec
from .reference_adapter import build_direct_starter_reference_clone

__all__ = [
    "DirectStarterSpec",
    "PowerCircuitSpec",
    "SinglePhaseLightingSpec",
    "build_direct_starter_reference_clone",
    "build_direct_starter_with_control",
    "build_single_phase_lighting_circuit",
    "build_three_phase_power_circuit",
]
