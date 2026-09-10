from __future__ import annotations

from .model import Annotation


def normalize_reference(value: str) -> str:
    value = value.strip().lstrip("-")
    if not value or any(char in value for char in "#*"):
        raise ValueError("CADe_SIMU references must be non-empty and cannot contain # or *")
    return f"-{value}"


def normalize_text(value: str) -> str:
    value = value.strip()
    if not value or any(char in value for char in "#*"):
        raise ValueError("CADe_SIMU text must be non-empty and cannot contain # or *")
    return value


def three_phase_supply(index: int, x: int, y: int) -> str:
    return (
        f"*{index}*3004#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*"
        "-12*-9*18*3*0*0*0*1*0*0*0"
    )


def single_phase_supply(index: int, x: int, y: int) -> str:
    """Observed L/N/PE supply symbol (type 3011)."""
    return (
        f"*{index}*3011#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*"
        "-12*-8*17*3*0*0*0*1*0*0*0"
    )


def motor_protection(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*6009#{ref}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*"
        f"{x}*{y}*0*0*-21*-3*18*24*0*0*0*1*0*1*2"
    )


def power_contactor(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*2001#{ref}##1#3#5#2#4#6#6#8*1*1*1*1*1*1*1*1*"
        f"{x}*{y}*0*0*-12*-3*18*15*0*0*0*1*0*4*6"
    )


def thermal_overload_power(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*6007#{ref}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*"
        f"{x}*{y}*0*0*-15*-3*21*15*0*0*0*1*0*7*8"
    )


def three_phase_motor(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*1000#{ref}##U1#V1#W1#PE####*1*1*1*1*0*0*0*0*"
        f"{x}*{y}*0*0*-12*-6*24*24*0*0*0*1*0*14*15"
    )


def two_pole_rcd(index: int, reference: str, x: int, y: int) -> str:
    """Observed two-pole residual-current device (type 6005)."""
    ref = normalize_reference(reference)
    return (
        f"*{index}*6005#{ref}##1#3#2#4####*1*1*1*1*0*0*0*0*"
        f"{x}*{y}*0*0*-21*-3*12*21*0*0*0*1*0*1*4"
    )


def two_pole_breaker(index: int, reference: str, x: int, y: int) -> str:
    """Observed two-pole magnetothermic breaker (type 6008)."""
    ref = normalize_reference(reference)
    return (
        f"*{index}*6008#{ref}##1#3#2#4####*1*1*1*1*0*0*0*0*"
        f"{x}*{y}*0*0*-21*-3*12*24*0*0*0*1*0*2*5"
    )


def maintained_switch_no(index: int, reference: str, x: int, y: int) -> str:
    """Observed maintained normally-open switch (type 8008)."""
    ref = normalize_reference(reference)
    return (
        f"*{index}*8008#{ref}##13#14######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-17*-3*6*15*0*0*0*1*0*3*8"
    )


def indicator_lamp(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*9008#{ref}##X1#X2#0#####*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-15*-3*8*15*0*0*0*1*0*18*19"
    )


def control_supply(index: int, x: int, y: int) -> str:
    return (
        f"*{index}*3000#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*"
        "-9*-6*3*12*0*3*0*1*0*0*0"
    )


def control_return(index: int, x: int, y: int) -> str:
    return (
        f"*{index}*3001#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*"
        "-9*-6*3*12*0*3*0*1*0*0*0"
    )


def protection_auxiliary(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*6010#{ref}##1#2######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-21*-3*6*24*0*0*0*1*0*13*14"
    )


def overload_auxiliary(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*8018#{ref}##95#97#96#98####*1*1*1*1*0*0*0*0*"
        f"{x}*{y}*0*0*-18*-3*15*15*0*0*0*1*0*14*14"
    )


def pushbutton_nc(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*8001#{ref}##11#12######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-18*-3*6*15*0*0*0*1*0*15*20"
    )


def pushbutton_no(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*8000#{ref}##13#14######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-18*-3*6*15*0*0*0*1*0*20*19"
    )


def auxiliary_contact_no(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*7000#{ref}##13#14######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-12*-3*6*15*0*0*0*1*0*0*19"
    )


def contactor_coil(index: int, reference: str, x: int, y: int) -> str:
    ref = normalize_reference(reference)
    return (
        f"*{index}*9000#{ref}##A1#A2######*1*1*0*0*0*0*0*0*"
        f"{x}*{y}*0*0*-15*-3*9*15*0*0*0*1*0*0*0"
    )


def _wire_variant(
    index: int,
    type_code: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    network: int,
) -> str:
    return (
        f"*{index}*{type_code}##########*0*0*0*0*0*0*0*0*"
        f"{x1}*{y1}*{x2}*{y2}*0*0*0*0*0*0*0*0*0*{network}*0"
    )


def wire(index: int, x1: int, y1: int, x2: int, y2: int, network: int) -> str:
    return _wire_variant(index, 4000, x1, y1, x2, y2, network)


def phase_wire(index: int, x1: int, y1: int, x2: int, y2: int, network: int) -> str:
    return _wire_variant(index, 4018, x1, y1, x2, y2, network)


def neutral_wire(index: int, x1: int, y1: int, x2: int, y2: int, network: int) -> str:
    return _wire_variant(index, 4009, x1, y1, x2, y2, network)


def protective_earth_wire(
    index: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    network: int,
) -> str:
    return _wire_variant(index, 4010, x1, y1, x2, y2, network)


def junction(index: int, x: int, y: int, network: int) -> str:
    return (
        f"*{index}*4001##########*0*0*0*0*0*0*0*0*"
        f"{x}*{y}*{x}*{y}*0*0*0*0*0*0*0*0*0*{network}*0"
    )


def text_label(index: int, annotation: Annotation) -> str:
    value = normalize_text(annotation.text)
    x2 = annotation.x + max(8, min(70, len(value) + 4))
    y2 = annotation.y + 3
    return (
        f"*{index}*8##########*0*0*0*0*0*0*0*0*"
        f"{annotation.x}*{annotation.y}*{x2}*{y2}*0*0*0*0*0*0*0*0*0*0*0#{value}"
    )
