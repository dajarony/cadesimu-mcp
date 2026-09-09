from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Annotation:
    """A free-text teaching label positioned in CADe_SIMU coordinates."""

    text: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class PowerCircuitSpec:
    """User-facing names and presentation options for the power circuit."""

    protection: str = "QF1"
    contactor: str = "KM1"
    overload: str = "FR1"
    motor: str = "M1"
    title: str = "Auralis Power"
    include_explanations: bool = False


@dataclass(frozen=True, slots=True)
class DirectStarterSpec:
    """User-facing names and presentation options for a direct motor starter."""

    protection: str = "QF1"
    contactor: str = "KM1"
    overload: str = "FR1"
    motor: str = "M1"
    stop_button: str = "S0"
    start_button: str = "S1"
    title: str = "Auralis Direct Starter"
    include_explanations: bool = True
