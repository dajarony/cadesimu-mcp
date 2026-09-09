"""Observed CADe_SIMU type codes.

These mappings are provisional. They were inferred by comparing public CADe_SIMU
project files and must be verified with controlled files produced in CADe_SIMU.
"""

TYPE_CODES: dict[int, str] = {
    1000: "three_phase_motor",
    2001: "three_pole_contactor",
    3004: "three_phase_supply",
    3011: "supply_or_terminal_variant",
    4000: "wire_segment",
    4001: "junction",
    6003: "three_pole_fuse_block",
    6007: "thermal_overload_power",
    6009: "three_pole_motor_protection",
    6010: "protection_auxiliary",
    7000: "auxiliary_contact_no",
    7001: "auxiliary_contact_nc",
    8000: "pushbutton_no",
    8001: "pushbutton_nc",
    8017: "overload_contact_variant",
    8018: "overload_auxiliary",
    9000: "contactor_coil",
    9008: "indicator_lamp",
}


def type_name(type_code: int) -> str:
    return TYPE_CODES.get(type_code, "unknown")
