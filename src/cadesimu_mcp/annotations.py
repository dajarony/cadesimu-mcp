from __future__ import annotations

from .layout import ControlLayout, PowerLayout, SinglePhaseLightingLayout
from .model import Annotation, DirectStarterSpec, PowerCircuitSpec, SinglePhaseLightingSpec


def power_annotations(spec: PowerCircuitSpec, layout: PowerLayout) -> tuple[Annotation, ...]:
    """Teaching labels aligned with the corresponding power components."""
    label_x = layout.x + 26
    return (
        Annotation("FUERZA", layout.x - 9, layout.y - 15),
        Annotation("L1 L2 L3 - alimentacion trifasica", label_x, layout.y + 1),
        Annotation(f"{spec.protection} - proteccion trifasica", label_x, layout.protection_y + 9),
        Annotation(f"{spec.contactor} - contactor de potencia", label_x, layout.contactor_y + 5),
        Annotation(f"{spec.overload} - rele termico", label_x, layout.overload_y + 5),
        Annotation(f"{spec.motor} - motor trifasico", label_x, layout.motor_y + 7),
    )


def direct_starter_annotations(
    spec: DirectStarterSpec,
    power: PowerLayout,
    control: ControlLayout,
) -> tuple[Annotation, ...]:
    """Labels placed beside the exact component they describe."""
    power_x = power.x + 26
    control_right = control.hold_x + 15
    return (
        Annotation("FUERZA", power.x - 9, power.y - 15),
        Annotation("MANDO", control.control_x - 6, control.source_y - 12),
        Annotation(f"{spec.protection} - proteccion trifasica", power_x, power.protection_y + 9),
        Annotation(f"{spec.contactor} - contactor de potencia", power_x, power.contactor_y + 5),
        Annotation(f"{spec.overload} - rele termico", power_x, power.overload_y + 5),
        Annotation(f"{spec.motor} - motor trifasico", power_x, power.motor_y + 7),
        Annotation(
            f"{spec.protection} aux - contacto de proteccion",
            control_right,
            control.source_y + 10,
        ),
        Annotation(
            f"{spec.overload} 95-96 - contacto NC de sobrecarga",
            control_right,
            control.overload_y + 6,
        ),
        Annotation(f"{spec.stop_button} 11-12 - PARO NC", control_right, control.stop_y + 5),
        Annotation(f"{spec.start_button} 13-14 - MARCHA NO", 132, control.start_y + 5),
        Annotation(
            f"{spec.contactor} aux 13-14 - automantenimiento",
            control_right,
            control.start_y + 5,
        ),
        Annotation(
            f"{spec.contactor} A1-A2 - bobina del contactor",
            control_right,
            control.coil_y + 5,
        ),
    )


def single_phase_lighting_annotations(
    spec: SinglePhaseLightingSpec,
    layout: SinglePhaseLightingLayout,
) -> tuple[Annotation, ...]:
    """Aligned teaching labels for the protected single-phase lamp circuit."""
    label_x = layout.x + 34
    return (
        Annotation("CIRCUITO MONOFASICO BASICO", layout.x - 18, layout.source_y - 18),
        Annotation("ACOMETIDA (ALIM) - L N PE", label_x, layout.source_y + 1),
        Annotation(f"{spec.main_breaker} - INT MAG (IGA)", label_x, layout.main_breaker_y + 8),
        Annotation(
            f"{spec.residual_device} - INT DIFERENCIAL (ID)",
            label_x,
            layout.residual_device_y + 7,
        ),
        Annotation(
            f"{spec.branch_breaker} - INT MAGN (INT AUTOMATICO)",
            label_x,
            layout.branch_breaker_y + 8,
        ),
        Annotation(f"{spec.switch} 13-14 - INTERRUPTOR (NA)", label_x, layout.switch_y + 5),
        Annotation(f"{spec.lamp} X1-X2 - BOMBILLA", label_x, layout.lamp_y + 5),
        Annotation("PE - tierra de proteccion", label_x, layout.source_y + 10),
    )
