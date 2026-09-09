from __future__ import annotations

from ..layout import ControlLayout
from ..model import DirectStarterSpec
from ..records import (
    auxiliary_contact_no,
    contactor_coil,
    control_return,
    control_supply,
    junction,
    overload_auxiliary,
    protection_auxiliary,
    pushbutton_nc,
    pushbutton_no,
    wire,
)

# Network ids observed in the known-working direct-starter sample.
SUPPLY_NET = 13
AFTER_PROTECTION_NET = 14
AFTER_OVERLOAD_NET = 15
BEFORE_START_NET = 20
HOLD_NET = 19
RETURN_NET = 18


def build_direct_starter_control_records(
    spec: DirectStarterSpec,
    layout: ControlLayout,
    *,
    start_index: int,
) -> list[str]:
    """Create STOP/START, KM1 coil and self-hold records for a direct starter."""
    base = start_index
    records = [
        control_supply(base, layout.source_x, layout.source_y),
        protection_auxiliary(base + 1, spec.protection, layout.control_x, layout.source_y),
        overload_auxiliary(base + 2, spec.overload, layout.control_x, layout.overload_y),
        pushbutton_nc(base + 3, spec.stop_button, layout.control_x, layout.stop_y),
        pushbutton_no(base + 4, spec.start_button, layout.control_x, layout.start_y),
        auxiliary_contact_no(base + 5, spec.contactor, layout.hold_x, layout.start_y),
        contactor_coil(base + 6, spec.contactor, layout.control_x, layout.coil_y),
        control_return(base + 7, layout.return_x, layout.return_y),
    ]

    def add_wire(x1: int, y1: int, x2: int, y2: int, network: int) -> None:
        records.append(wire(start_index + len(records), x1, y1, x2, y2, network))

    def add_junction(x: int, y: int, network: int) -> None:
        records.append(junction(start_index + len(records), x, y, network))

    # Main control path.
    add_wire(layout.source_x, layout.source_y, layout.control_x, layout.source_y, SUPPLY_NET)
    add_wire(
        layout.control_x,
        layout.protection_bottom_y,
        layout.control_x,
        layout.overload_y,
        AFTER_PROTECTION_NET,
    )
    add_wire(
        layout.control_x,
        layout.overload_bottom_y,
        layout.control_x,
        layout.stop_y,
        AFTER_OVERLOAD_NET,
    )
    add_wire(
        layout.control_x,
        layout.stop_bottom_y,
        layout.control_x,
        layout.start_y,
        BEFORE_START_NET,
    )
    add_wire(
        layout.control_x,
        layout.start_bottom_y,
        layout.control_x,
        layout.coil_y,
        HOLD_NET,
    )
    add_wire(
        layout.control_x,
        layout.coil_bottom_y,
        layout.control_x,
        layout.return_y,
        RETURN_NET,
    )
    add_wire(layout.return_x, layout.return_y, layout.hold_x, layout.return_y, RETURN_NET)
    add_junction(layout.control_x, layout.return_y, RETURN_NET)

    # KM1 NO auxiliary contact in parallel with START (self-hold branch).
    branch_x = layout.hold_x - 3
    add_wire(
        layout.control_x,
        layout.branch_top_y,
        branch_x,
        layout.branch_top_y,
        BEFORE_START_NET,
    )
    add_junction(layout.control_x, layout.branch_top_y, BEFORE_START_NET)
    add_wire(branch_x, layout.branch_top_y, branch_x, layout.branch_bottom_y, BEFORE_START_NET)
    add_wire(layout.hold_x, layout.start_bottom_y, layout.hold_x, layout.coil_y, HOLD_NET)
    add_wire(
        layout.control_x,
        layout.hold_join_y,
        layout.hold_x,
        layout.hold_join_y,
        HOLD_NET,
    )
    add_junction(layout.control_x, layout.hold_join_y, HOLD_NET)
    add_junction(layout.hold_x, layout.hold_join_y, HOLD_NET)

    return records
