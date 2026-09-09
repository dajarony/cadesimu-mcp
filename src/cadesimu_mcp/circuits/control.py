from __future__ import annotations

from collections.abc import Callable

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

# Network ids observed in a known-working CADe_SIMU direct-starter sample.
SUPPLY_NET = 13
AFTER_PROTECTION_NET = 14
AFTER_OVERLOAD_NET = 15
BEFORE_START_NET = 20
HOLD_NET = 19
RETURN_NET = 18


def _component_records(
    spec: DirectStarterSpec,
    layout: ControlLayout,
    *,
    start_index: int,
) -> list[str]:
    """Emit active control devices in CADe_SIMU's observed simulation-scan order."""
    base = start_index
    return [
        protection_auxiliary(base, spec.protection, layout.control_x, layout.source_y),
        overload_auxiliary(base + 1, spec.overload, layout.control_x, layout.overload_y),
        pushbutton_nc(base + 2, spec.stop_button, layout.control_x, layout.stop_y),
        pushbutton_no(base + 3, spec.start_button, layout.control_x, layout.start_y),
        # The known-working sample evaluates the coil before its NO self-hold contact.
        # Keeping this order matters for momentary START operation in CADe_SIMU.
        contactor_coil(base + 4, spec.contactor, layout.control_x, layout.coil_y),
        control_supply(base + 5, layout.source_x, layout.source_y),
        control_return(base + 6, layout.return_x, layout.return_y),
    ]


def _append_main_path(
    records: list[str],
    layout: ControlLayout,
    *,
    start_index: int,
    add_wire: Callable[[int, int, int, int, int], None],
    add_junction: Callable[[int, int, int], None],
) -> None:
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


def _append_self_hold_branch(
    records: list[str],
    spec: DirectStarterSpec,
    layout: ControlLayout,
    *,
    start_index: int,
    add_wire: Callable[[int, int, int, int, int], None],
    add_junction: Callable[[int, int, int], None],
) -> None:
    # Match the ordering and geometry of the known-working direct-starter sample:
    # main-path wires first, then KM1 auxiliary contact, then its branch wires.
    records.append(
        auxiliary_contact_no(
            start_index + len(records),
            spec.contactor,
            layout.hold_x,
            layout.start_y,
        )
    )

    branch_x = layout.hold_x - 3
    add_wire(layout.hold_x, layout.start_bottom_y, layout.hold_x, layout.coil_y, HOLD_NET)
    add_wire(branch_x, layout.branch_top_y, branch_x, layout.branch_bottom_y, BEFORE_START_NET)
    add_wire(
        layout.control_x,
        layout.branch_top_y,
        branch_x,
        layout.branch_top_y,
        BEFORE_START_NET,
    )
    add_junction(layout.control_x, layout.branch_top_y, BEFORE_START_NET)
    add_wire(
        layout.control_x,
        layout.hold_join_y,
        layout.hold_x,
        layout.hold_join_y,
        HOLD_NET,
    )
    add_junction(layout.control_x, layout.hold_join_y, HOLD_NET)
    add_junction(layout.hold_x, layout.hold_join_y, HOLD_NET)


def build_direct_starter_control_records(
    spec: DirectStarterSpec,
    layout: ControlLayout,
    *,
    start_index: int,
) -> list[str]:
    """Create STOP/START, KM1 coil and self-hold records for a direct starter."""
    records = _component_records(spec, layout, start_index=start_index)

    def add_wire(x1: int, y1: int, x2: int, y2: int, network: int) -> None:
        records.append(wire(start_index + len(records), x1, y1, x2, y2, network))

    def add_junction(x: int, y: int, network: int) -> None:
        records.append(junction(start_index + len(records), x, y, network))

    _append_main_path(
        records,
        layout,
        start_index=start_index,
        add_wire=add_wire,
        add_junction=add_junction,
    )
    _append_self_hold_branch(
        records,
        spec,
        layout,
        start_index=start_index,
        add_wire=add_wire,
        add_junction=add_junction,
    )
    return records
