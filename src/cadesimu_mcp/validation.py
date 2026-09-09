from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ValidationStatus:
    """Manual validation state against the user's CADe_SIMU installation."""

    power_layout_opened: bool = True
    annotations_rendered: bool = True
    control_layout_opened: bool = True
    control_simulation_passed: bool = False

    def as_dict(self) -> dict[str, bool]:
        return asdict(self)


VALIDATION_STATUS = ValidationStatus()
