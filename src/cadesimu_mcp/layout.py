from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PowerLayout:
    """Coordinates for the validated three-phase power column."""

    x: int = 69
    y: int = 51
    phase_spacing: int = 6

    @property
    def phase_xs(self) -> tuple[int, int, int]:
        return (self.x, self.x + self.phase_spacing, self.x + 2 * self.phase_spacing)

    @property
    def protection_y(self) -> int:
        return self.y + 6

    @property
    def protection_bottom_y(self) -> int:
        return self.y + 27

    @property
    def contactor_y(self) -> int:
        return self.y + 36

    @property
    def contactor_bottom_y(self) -> int:
        return self.y + 48

    @property
    def overload_y(self) -> int:
        return self.y + 57

    @property
    def overload_bottom_y(self) -> int:
        return self.y + 69

    @property
    def motor_y(self) -> int:
        return self.y + 78


@dataclass(frozen=True, slots=True)
class ControlLayout:
    """Coordinates for the STOP/START and KM1 self-hold control column."""

    source_x: int = 150
    control_x: int = 171
    hold_x: int = 195
    source_y: int = 48
    overload_y: int = 78
    stop_y: int = 96
    start_y: int = 114
    coil_y: int = 132
    return_x: int = 153
    return_y: int = 147

    @property
    def protection_bottom_y(self) -> int:
        return self.source_y + 21

    @property
    def overload_bottom_y(self) -> int:
        return self.overload_y + 12

    @property
    def stop_bottom_y(self) -> int:
        return self.stop_y + 12

    @property
    def start_bottom_y(self) -> int:
        return self.start_y + 12

    @property
    def coil_bottom_y(self) -> int:
        return self.coil_y + 12

    @property
    def branch_top_y(self) -> int:
        return self.start_y - 3

    @property
    def branch_bottom_y(self) -> int:
        return self.start_y + 3

    @property
    def hold_join_y(self) -> int:
        return self.coil_y - 3
