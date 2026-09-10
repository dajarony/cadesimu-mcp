from __future__ import annotations

from ..annotations import single_phase_lighting_annotations
from ..layout import SinglePhaseLightingLayout
from ..model import SinglePhaseLightingSpec
from ..records import (
    indicator_lamp,
    maintained_switch_no,
    neutral_wire,
    phase_wire,
    protective_earth_wire,
    single_phase_supply,
    text_label,
    two_pole_breaker,
    two_pole_rcd,
)
from ..writer import serialize_records


def build_single_phase_lighting_records(
    spec: SinglePhaseLightingSpec,
    layout: SinglePhaseLightingLayout,
    *,
    start_index: int = 0,
) -> list[str]:
    """Create the electrical records for L/N/PE, protections, switch and lamp."""
    base = start_index
    records = [
        single_phase_supply(base, layout.x, layout.source_y),
        two_pole_breaker(base + 1, spec.main_breaker, layout.x, layout.main_breaker_y),
        two_pole_rcd(base + 2, spec.residual_device, layout.x, layout.residual_device_y),
        two_pole_breaker(base + 3, spec.branch_breaker, layout.x, layout.branch_breaker_y),
        maintained_switch_no(base + 4, spec.switch, layout.phase_x, layout.switch_y),
        indicator_lamp(base + 5, spec.lamp, layout.phase_x, layout.lamp_y),
    ]

    def add_phase(x1: int, y1: int, x2: int, y2: int, network: int) -> None:
        records.append(phase_wire(start_index + len(records), x1, y1, x2, y2, network))

    def add_neutral(x1: int, y1: int, x2: int, y2: int, network: int) -> None:
        records.append(neutral_wire(start_index + len(records), x1, y1, x2, y2, network))

    add_phase(layout.phase_x, layout.source_y, layout.phase_x, layout.main_breaker_y, 1)
    add_neutral(layout.neutral_x, layout.source_y, layout.neutral_x, layout.main_breaker_y, 2)

    add_phase(
        layout.phase_x,
        layout.main_breaker_bottom_y,
        layout.phase_x,
        layout.residual_device_y,
        3,
    )
    add_neutral(
        layout.neutral_x,
        layout.main_breaker_bottom_y,
        layout.neutral_x,
        layout.residual_device_y,
        4,
    )

    add_phase(
        layout.phase_x,
        layout.residual_device_bottom_y,
        layout.phase_x,
        layout.branch_breaker_y,
        5,
    )
    add_neutral(
        layout.neutral_x,
        layout.residual_device_bottom_y,
        layout.neutral_x,
        layout.branch_breaker_y,
        6,
    )

    add_phase(
        layout.phase_x,
        layout.branch_breaker_bottom_y,
        layout.phase_x,
        layout.switch_y,
        7,
    )
    add_phase(
        layout.phase_x,
        layout.switch_bottom_y,
        layout.phase_x,
        layout.lamp_y,
        8,
    )

    neutral_bottom = layout.lamp_bottom_y
    add_neutral(
        layout.neutral_x,
        layout.branch_breaker_bottom_y,
        layout.neutral_x,
        neutral_bottom,
        9,
    )
    add_neutral(layout.neutral_x, neutral_bottom, layout.phase_x, neutral_bottom, 9)

    records.append(
        protective_earth_wire(
            start_index + len(records),
            layout.pe_x,
            layout.source_y,
            layout.pe_x,
            layout.source_y + 18,
            10,
        )
    )
    return records


def build_single_phase_lighting_circuit(
    spec: SinglePhaseLightingSpec | None = None,
    layout: SinglePhaseLightingLayout | None = None,
) -> str:
    """Build a protected single-phase lamp circuit suitable for CADe_SIMU."""
    spec = spec or SinglePhaseLightingSpec()
    layout = layout or SinglePhaseLightingLayout()
    records = build_single_phase_lighting_records(spec, layout)

    if spec.include_explanations:
        for annotation in single_phase_lighting_annotations(spec, layout):
            records.append(text_label(len(records), annotation))

    return serialize_records(records, spec.title)
