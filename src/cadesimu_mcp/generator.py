from __future__ import annotations

"""Experimental CADe_SIMU text generation.

The power circuit record shapes have been validated by opening a generated file
successfully in the user's CADe_SIMU version. Text annotation records are based
on observed public CADe_SIMU files and remain separately testable/optional.
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
    include_explanations: bool = False


def _ref(value: str) -> str:
    value = value.strip().lstrip("-")
    if not value or any(char in value for char in "#*"):
        raise ValueError("CADe_SIMU references must be non-empty and cannot contain # or *")
    return f"-{value}"


def _text(value: str) -> str:
    value = value.strip()
    if not value or any(char in value for char in "#*"):
        raise ValueError("CADe_SIMU text must be non-empty and cannot contain # or *")
    return value


def _field(value: str, width: int) -> str:
    return value[:width].ljust(width)


def _trailer(title: str) -> str:
    return (
        "#$$$*1*1*1*2*4*0*1*0*0*333*3234&&&"
        f"*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}"
        f"*{_field('', 25)}*{_field('', 25)}*{_field('09-Sep-2026', 11)}"
        f"*{_field('1', 11)}*{_field('1', 11)}*{_field(title, 21)}"
        "*1*1*1*1*1*1*1*1*1*1*1*1*1*1***$$$&&&"
    )


def _text_record(index: int, value: str, x: int, y: int) -> str:
    """Create a CADe_SIMU free-text record (observed type code 8)."""
    value = _text(value)
    x2 = x + max(8, min(60, len(value) + 4))
    y2 = y + 3
    return (
        f"*{index}*8##########*0*0*0*0*0*0*0*0*"
        f"{x}*{y}*{x2}*{y2}*0*0*0*0*0*0*0*0*0*0*0#{value}"
    )


def build_three_phase_power_circuit(spec: PowerCircuitSpec | None = None) -> str:
    """Build a direct-starter power circuit for CADe_SIMU.

    Layout: 3-phase supply -> 3-pole motor protection -> power contactor ->
    thermal overload -> 3-phase motor.

    Set ``include_explanations=True`` to add a title and a short legend beside
    the schematic using CADe_SIMU text records. The electrical power layout was
    manually validated in CADe_SIMU on 2026-09-09; annotation rendering is kept
    optional so it can be validated independently.
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

    if spec.include_explanations:
        tx = x + 45
        labels = (
            ("CUADRO DE FUERZA - ARRANQUE DIRECTO", tx, y - 12),
            ("L1 L2 L3: alimentacion trifasica", tx, y),
            (f"{spec.protection}: proteccion del motor", tx, y + 12),
            (f"{spec.contactor}: contactor de potencia", tx, y + 36),
            (f"{spec.overload}: rele termico", tx, y + 57),
            (f"{spec.motor}: motor trifasico", tx, y + 78),
        )
        for value, label_x, label_y in labels:
            records.append(_text_record(len(records), value, label_x, label_y))

    cad_text = "CADe_SIMU" + "#".join(records) + _trailer(spec.title)

    parsed = CadDocument.parse(cad_text)
    if parsed.dumps() != cad_text:
        raise RuntimeError("generated CADe_SIMU text failed internal round-trip")
    return cad_text
