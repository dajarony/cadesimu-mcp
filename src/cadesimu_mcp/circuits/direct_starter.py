from __future__ import annotations

from ..annotations import direct_starter_annotations
from ..layout import ControlLayout, PowerLayout
from ..model import DirectStarterSpec, PowerCircuitSpec
from ..records import text_label
from ..writer import serialize_records
from .control import build_direct_starter_control_records
from .power import build_power_records


def build_direct_starter_with_control(
    spec: DirectStarterSpec | None = None,
    *,
    power_layout: PowerLayout | None = None,
    control_layout: ControlLayout | None = None,
) -> str:
    """Compose power + STOP/START control + KM1 self-hold into one CADe_SIMU file."""
    spec = spec or DirectStarterSpec()
    power_layout = power_layout or PowerLayout()
    control_layout = control_layout or ControlLayout()

    power_spec = PowerCircuitSpec(
        protection=spec.protection,
        contactor=spec.contactor,
        overload=spec.overload,
        motor=spec.motor,
        title=spec.title,
        include_explanations=False,
    )
    records = build_power_records(power_spec, power_layout)
    records.extend(
        build_direct_starter_control_records(
            spec,
            control_layout,
            start_index=len(records),
        )
    )

    if spec.include_explanations:
        for annotation in direct_starter_annotations(spec, power_layout, control_layout):
            records.append(text_label(len(records), annotation))

    return serialize_records(records, spec.title)
