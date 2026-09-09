from __future__ import annotations

"""CADe_SIMU text generation for small industrial-control teaching circuits."""

from dataclasses import dataclass
import re

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


@dataclass(frozen=True, slots=True)
class DirectStarterSpec:
    protection: str = "QF1"
    contactor: str = "KM1"
    overload: str = "FR1"
    motor: str = "M1"
    stop_button: str = "S0"
    start_button: str = "S1"
    title: str = "Auralis Direct Starter"
    include_explanations: bool = True


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


def _type_code(raw: str) -> int:
    match = re.match(r"\*\d+\*(\d+)#", raw)
    if not match:
        raise ValueError("invalid generated CADe_SIMU record")
    return int(match.group(1))


def _serialize(records: list[str], title: str) -> str:
    """Serialize records using CADe_SIMU's special no-separator rule after text records."""
    if not records:
        return "CADe_SIMU" + _trailer(title)
    chunks = ["CADe_SIMU", records[0]]
    previous_type = _type_code(records[0])
    for record in records[1:]:
        chunks.append("" if previous_type == 8 else "#")
        chunks.append(record)
        previous_type = _type_code(record)
    chunks.append(_trailer(title))
    cad_text = "".join(chunks)
    parsed = CadDocument.parse(cad_text)
    if parsed.dumps() != cad_text:
        raise RuntimeError("generated CADe_SIMU text failed internal round-trip")
    return cad_text


def _text_record(index: int, value: str, x: int, y: int) -> str:
    value = _text(value)
    x2 = x + max(8, min(60, len(value) + 4))
    y2 = y + 3
    return (
        f"*{index}*8##########*0*0*0*0*0*0*0*0*"
        f"{x}*{y}*{x2}*{y2}*0*0*0*0*0*0*0*0*0*0*0#{value}"
    )


def _wire(index: int, x1: int, y1: int, x2: int, y2: int, network: int) -> str:
    return (
        f"*{index}*4000##########*0*0*0*0*0*0*0*0*"
        f"{x1}*{y1}*{x2}*{y2}*0*0*0*0*0*0*0*0*0*{network}*0"
    )


def _junction(index: int, x: int, y: int, network: int) -> str:
    return (
        f"*{index}*4001##########*0*0*0*0*0*0*0*0*"
        f"{x}*{y}*{x}*{y}*0*0*0*0*0*0*0*0*0*{network}*0"
    )


def build_three_phase_power_circuit(spec: PowerCircuitSpec | None = None) -> str:
    """Build the validated three-phase power side of a direct starter."""
    spec = spec or PowerCircuitSpec()
    x, y = spec.x, spec.y
    xs = (x, x + 6, x + 12)
    q, k, f, m = map(_ref, (spec.protection, spec.contactor, spec.overload, spec.motor))

    records = [
        f"*0*3004#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*-12*-9*18*3*0*0*0*1*0*0*0",
        f"*1*6009#{q}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*{y + 6}*0*0*-21*-3*18*24*0*0*0*1*0*1*2",
        f"*2*2001#{k}##1#3#5#2#4#6#6#8*1*1*1*1*1*1*1*1*{x}*{y + 36}*0*0*-12*-3*18*15*0*0*0*1*0*4*6",
        f"*3*6007#{f}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*{y + 57}*0*0*-15*-3*21*15*0*0*0*1*0*7*8",
        f"*4*1000#{m}##U1#V1#W1#PE####*1*1*1*1*0*0*0*0*{x}*{y + 78}*0*0*-12*-6*24*24*0*0*0*1*0*14*15",
    ]

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

    circuit_id = 1
    for start_y, end_y in ((y, y + 6), (y + 27, y + 36), (y + 48, y + 57), (y + 69, y + 78)):
        for wire_x in xs:
            records.append(_wire(len(records), wire_x, start_y, wire_x, end_y, circuit_id))
            circuit_id += 1

    return _serialize(records, spec.title)


def build_direct_starter_with_control(spec: DirectStarterSpec | None = None) -> str:
    """Build power + start/stop control + KM1 self-hold for CADe_SIMU.

    The control topology follows a known CADe_SIMU direct-starter family:
    QF1 auxiliary -> FR1 overload auxiliary -> STOP NC -> START NO -> KM1 coil,
    with a KM1 NO auxiliary contact in parallel with START for self-holding.
    """
    spec = spec or DirectStarterSpec()
    q, k, f, m, s0, s1 = map(
        _ref,
        (spec.protection, spec.contactor, spec.overload, spec.motor, spec.stop_button, spec.start_button),
    )

    # Power side: same coordinates already validated in CADe_SIMU.
    x, y = 69, 51
    records = [
        f"*0*3004#-X#########*0*0*0*0*0*0*0*0*{x}*{y}*0*0*-12*-9*18*3*0*0*0*1*0*0*0",
        f"*1*6009#{q}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*57*0*0*-21*-3*18*24*0*0*0*1*0*1*2",
        f"*2*2001#{k}##1#3#5#2#4#6#6#8*1*1*1*1*1*1*1*1*{x}*87*0*0*-12*-3*18*15*0*0*0*1*0*4*6",
        f"*3*6007#{f}##1#3#5#2#4#6##*1*1*1*1*1*1*0*0*{x}*108*0*0*-15*-3*21*15*0*0*0*1*0*7*8",
        f"*4*1000#{m}##U1#V1#W1#PE####*1*1*1*1*0*0*0*0*{x}*129*0*0*-12*-6*24*24*0*0*0*1*0*14*15",
    ]

    if spec.include_explanations:
        labels = (
            ("FUERZA", 69, 36),
            ("MANDO", 171, 36),
            ("QF1: proteccion general y del motor", 225, 54),
            ("KM1: contactor que conecta el motor", 225, 72),
            ("FR1: rele termico contra sobrecarga", 225, 90),
            ("S0: pulsador PARO normalmente cerrado", 225, 108),
            ("S1: pulsador MARCHA normalmente abierto", 225, 126),
            ("KM1 aux: mantiene la bobina activada", 225, 144),
            ("M1: motor trifasico", 225, 162),
        )
        for value, tx, ty in labels:
            records.append(_text_record(len(records), value, tx, ty))

    # Power wiring.
    for xw, network in zip((69, 75, 81), (1, 2, 3)):
        records.append(_wire(len(records), xw, 51, xw, 57, network))
    for xw, network in zip((69, 75, 81), (4, 5, 6)):
        records.append(_wire(len(records), xw, 78, xw, 87, network))
    for xw, network in zip((69, 75, 81), (7, 8, 9)):
        records.append(_wire(len(records), xw, 99, xw, 108, network))
    for xw, network in zip((69, 75, 81), (10, 11, 12)):
        records.append(_wire(len(records), xw, 120, xw, 129, network))

    # Control components. Coordinates are shifted from a known-working public
    # CADe_SIMU direct-starter sample while preserving record geometry.
    records.extend(
        [
            f"*{len(records)}*3000#-X#########*0*0*0*0*0*0*0*0*150*48*0*0*-9*-6*3*12*0*3*0*1*0*0*0",
            f"*{len(records)+1}*6010#{q}##1#2######*1*1*0*0*0*0*0*0*171*48*0*0*-21*-3*6*24*0*0*0*1*0*13*14",
            f"*{len(records)+2}*8018#{f}##95#97#96#98####*1*1*1*1*0*0*0*0*171*78*0*0*-18*-3*15*15*0*0*0*1*0*14*14",
            f"*{len(records)+3}*8001#{s0}##11#12######*1*1*0*0*0*0*0*0*171*96*0*0*-18*-3*6*15*0*0*0*1*0*15*20",
            f"*{len(records)+4}*8000#{s1}##13#14######*1*1*0*0*0*0*0*0*171*114*0*0*-18*-3*6*15*0*0*0*1*0*20*19",
            f"*{len(records)+5}*7000#{k}##13#14######*1*1*0*0*0*0*0*0*195*114*0*0*-12*-3*6*15*0*0*0*1*0*0*19",
            f"*{len(records)+6}*9000#{k}##A1#A2######*1*1*0*0*0*0*0*0*171*132*0*0*-15*-3*9*15*0*0*0*1*0*0*0",
            f"*{len(records)+7}*3001#-X#########*0*0*0*0*0*0*0*0*153*147*0*0*-9*-6*3*12*0*3*0*1*0*0*0",
        ]
    )

    # Control wiring and the two junctions that create the KM1 self-hold branch.
    records.extend(
        [
            _wire(len(records), 150, 48, 171, 48, 13),
            _wire(len(records)+1, 171, 69, 171, 78, 14),
            _wire(len(records)+2, 171, 90, 171, 96, 15),
            _wire(len(records)+3, 171, 108, 171, 114, 20),
            _wire(len(records)+4, 171, 126, 171, 132, 19),
            _wire(len(records)+5, 171, 144, 171, 147, 18),
            _wire(len(records)+6, 153, 147, 195, 147, 18),
            _junction(len(records)+7, 171, 147, 18),
            _wire(len(records)+8, 171, 111, 192, 111, 20),
            _junction(len(records)+9, 171, 111, 20),
            _wire(len(records)+10, 192, 111, 192, 117, 20),
            _wire(len(records)+11, 195, 126, 195, 132, 19),
            _wire(len(records)+12, 171, 129, 195, 129, 19),
            _junction(len(records)+13, 171, 129, 19),
            _junction(len(records)+14, 195, 129, 19),
        ]
    )

    return _serialize(records, spec.title)
