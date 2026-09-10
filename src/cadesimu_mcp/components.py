from __future__ import annotations

from enum import IntEnum


class CadType(IntEnum):
    """Observed CADe_SIMU record type codes used by this project."""

    FREE_TEXT = 8
    THREE_PHASE_MOTOR = 1000
    THREE_POLE_CONTACTOR = 2001
    CONTROL_SUPPLY = 3000
    CONTROL_RETURN = 3001
    THREE_PHASE_SUPPLY = 3004
    SUPPLY_OR_TERMINAL_VARIANT = 3011
    WIRE = 4000
    JUNCTION = 4001
    NEUTRAL_WIRE = 4009
    PE_WIRE = 4010
    PHASE_WIRE = 4018
    TWO_POLE_RCD = 6005
    THREE_POLE_FUSE_BLOCK = 6003
    THERMAL_OVERLOAD_POWER = 6007
    TWO_POLE_BREAKER = 6008
    THREE_POLE_MOTOR_PROTECTION = 6009
    PROTECTION_AUXILIARY = 6010
    AUXILIARY_CONTACT_NO = 7000
    AUXILIARY_CONTACT_NC = 7001
    PUSHBUTTON_NO = 8000
    PUSHBUTTON_NC = 8001
    MAINTAINED_SWITCH_NO = 8008
    OVERLOAD_CONTACT_VARIANT = 8017
    OVERLOAD_AUXILIARY = 8018
    CONTACTOR_COIL = 9000
    INDICATOR_LAMP = 9008


TYPE_CODES: dict[int, str] = {
    int(CadType.FREE_TEXT): "free_text_label",
    int(CadType.THREE_PHASE_MOTOR): "three_phase_motor",
    int(CadType.THREE_POLE_CONTACTOR): "three_pole_contactor",
    int(CadType.CONTROL_SUPPLY): "control_supply",
    int(CadType.CONTROL_RETURN): "control_return",
    int(CadType.THREE_PHASE_SUPPLY): "three_phase_supply",
    int(CadType.SUPPLY_OR_TERMINAL_VARIANT): "supply_or_terminal_variant",
    int(CadType.WIRE): "wire_segment",
    int(CadType.JUNCTION): "junction",
    int(CadType.NEUTRAL_WIRE): "neutral_wire",
    int(CadType.PE_WIRE): "protective_earth_wire",
    int(CadType.PHASE_WIRE): "phase_wire",
    int(CadType.TWO_POLE_RCD): "two_pole_rcd",
    int(CadType.THREE_POLE_FUSE_BLOCK): "three_pole_fuse_block",
    int(CadType.THERMAL_OVERLOAD_POWER): "thermal_overload_power",
    int(CadType.TWO_POLE_BREAKER): "two_pole_breaker",
    int(CadType.THREE_POLE_MOTOR_PROTECTION): "three_pole_motor_protection",
    int(CadType.PROTECTION_AUXILIARY): "protection_auxiliary",
    int(CadType.AUXILIARY_CONTACT_NO): "auxiliary_contact_no",
    int(CadType.AUXILIARY_CONTACT_NC): "auxiliary_contact_nc",
    int(CadType.PUSHBUTTON_NO): "pushbutton_no",
    int(CadType.PUSHBUTTON_NC): "pushbutton_nc",
    int(CadType.MAINTAINED_SWITCH_NO): "maintained_switch_no",
    int(CadType.OVERLOAD_CONTACT_VARIANT): "overload_contact_variant",
    int(CadType.OVERLOAD_AUXILIARY): "overload_auxiliary",
    int(CadType.CONTACTOR_COIL): "contactor_coil",
    int(CadType.INDICATOR_LAMP): "indicator_lamp",
}


def type_name(type_code: int) -> str:
    return TYPE_CODES.get(type_code, "unknown")
