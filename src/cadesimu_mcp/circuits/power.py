from __future__ import annotations

from ..annotations import power_annotations
from ..layout import PowerLayout
from ..model import PowerCircuitSpec
from ..records import (
    motor_protection,
    power_contactor,
    text_label,
    thermal_overload_power,
    three_phase_motor,
    three_phase_supply,
    wire,
)
from ..writer import serialize_records


def build_power_records(
    spec: PowerCircuitSpec,
    layout: PowerLayout,
    *,
    start_index: int = 0,
) -> list[str]:
    """Create only the electrical power-side records, without annotations."""
    base = start_index
    records = [
        three_phase_supply(base, layout.x, layout.y),
        motor_protection(base + 1, spec.protection, layout.x, layout.protection_y),
        power_contactor(base + 2, spec.contactor, layout.x, layout.contactor_y),
        thermal_overload_power(base + 3, spec.overload, layout.x, layout.overload_y),
        three_phase_motor(base + 4, spec.motor, layout.x, layout.motor_y),
    ]

    network = 1
    wire_ranges = (
        (layout.y, layout.protection_y),
        (layout.protection_bottom_y, layout.contactor_y),
        (layout.contactor_bottom_y, layout.overload_y),
        (layout.overload_bottom_y, layout.motor_y),
    )
    for start_y, end_y in wire_ranges:
        for x in layout.phase_xs:
            records.append(wire(start_index + len(records), x, start_y, x, end_y, network))
            network += 1

    return records


def build_three_phase_power_circuit(
    spec: PowerCircuitSpec | None = None,
    layout: PowerLayout | None = None,
) -> str:
    """Build the validated power side of a three-phase direct starter."""
    spec = spec or PowerCircuitSpec()
    layout = layout or PowerLayout()
    records = build_power_records(spec, layout)

    if spec.include_explanations:
        for annotation in power_annotations(spec, layout):
            records.append(text_label(len(records), annotation))

    return serialize_records(records, spec.title)
