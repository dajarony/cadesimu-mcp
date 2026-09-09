from __future__ import annotations

"""Experimental CADe_SIMU text generation.

The record shapes in this module are inferred from multiple public CADe_SIMU
files. They are intentionally isolated from the parser until a generated file
has been opened and saved successfully by the user's CADe_SIMU version.
"""

from dataclasses import dataclass

from .codec import CadDocument


@dataclass(frozen=True, slots=True)
class PowerCircuitSpec:
    protection: str = "Q1"
    contactor: str = "K1"
    overload: str = "F1"
    motor: str = "M1"
    title: str = "Auralis Power"
    x: int = 69
    y: int = 51


def _ref(value: str) -> str:
    value = value.strip().lstrip("-")
    if not value or any(char in value for char in "#*"):
        raise ValueError("CADe_SIMU references must be non-empty and cannot contain # or *")
    return f"-{value}"


def _field(value: str, width: int) -> str:
    return value[:width].ljust(width)


def _trailer(title: str) -> str:
    # Page/configuration values are provisional and copied as format facts from
    # a known-working family of CADe_SIMU files; human-readable metadata is ours.
    return (
        "#$$$*1*1*1*2*4*0*1*0*0*333*3234&&&"
        f"*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}"
        f"*{_field('', 25)}*{_field('', 25)}*{_field('09-Sep-2026', 11)}"
        f"*{_field('1', 11)}*{_field('1', 11)}*{_field(title, 21)}"
        "*1*1*1*1*1*1*1*1*1*1*1*1*1*1***$$$&&&"
    )


def build_three_phase_power_circuit(spec: PowerCircuitSpec | None = None) -> str:
    """Build an *experimental* power-only direct-starter CADe_SIMU document.

    Layout: 3-phase supply -> 3-pole motor protection -> power contactor ->
    thermal overload -> 3-phase motor. No control circuit or contactor coil is
    generated yet, so this milestone is for opening/layout validation first.
    """
    spec = spec or PowerCircuitSpec()
    x, y = spec.x, spec.y
    xs = (x, x + 6, x + 12)

    q = _ref(spec.protection)
    k = _ref(spec.contactor)
    f = _ref(spec.overload)
    m = _ref(spec.motor)

    records = [
        f"*0*3004#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*-12*-9*18*3*0*0*0*1*0*0*0",
        f"*1*6009#{q}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*{y + 6}*0*0*-21*-3*18*24*0*0*0*1*0*1*2",
        f"*2*2001#{k}##1#3#5#2#4#6#6#8*1*1*1*1*1*1*1*1*{x}*{y + 36}*0*0*-12*-3*18*15*0*0*0*1*0*4*6",
        f"*3*6007#{f}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*{y + 57}*0*0*-15*-3*21*15*0*0*0*1*0*7*8",
        f"*4*1000#{m}##U1#V1#W1#PE####*1*1*1*1*0*0*0*0*{x}*{y + 78}*0*0*-12*-6*24*24*0*0*0*1*0*14*15",
    ]

    wire_ranges = (
        (y, y + 6),
        (y + 27, y + 36),
        (y + 48, y + 57),
        (y + 69, y + 78),
    )
    wire_index = 5
    circuit_id = 1
    for start_y, end_y in wire_ranges:
        for wire_x in xs:
            records.append(
                f"*{wire_index}*4000##########*0*0*0*0*0*0*0*0*"
                f"{wire_x}*{start_y}*{wire_x}*{end_y}*0*0*0*0*0*0*0*0*0*{circuit_id}*0"
            )
            wire_index += 1
            circuit_id += 1

    cad_text = "CADe_SIMU" + "#".join(records) + _trailer(spec.title)

    # Internal structural guard: if our own lossless parser cannot round-trip
    # what we generated, never hand the result to CADe_SIMU.
    parsed = CadDocument.parse(cad_text)
    if parsed.dumps() != cad_text:
        raise RuntimeError("generated CADe_SIMU text failed internal round-trip")
    return cad_text
