from __future__ import annotations

import re

from .codec import CadDocument
from .components import CadType

_RECORD_TYPE = re.compile(r"\*\d+\*(\d+)#")


def _field(value: str, width: int) -> str:
    return value[:width].ljust(width)


def build_trailer(title: str) -> str:
    """Build the page/footer trailer used by generated CADe_SIMU files."""
    return (
        "#$$$*1*1*1*2*4*0*1*0*0*333*3234&&&"
        f"*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}*{_field('', 11)}"
        f"*{_field('', 25)}*{_field('', 25)}*{_field('', 11)}"
        f"*{_field('1', 11)}*{_field('1', 11)}*{_field(title, 21)}"
        "*1*1*1*1*1*1*1*1*1*1*1*1*1*1***$$$&&&"
    )


def record_type(raw: str) -> int:
    match = _RECORD_TYPE.match(raw)
    if not match:
        raise ValueError("invalid generated CADe_SIMU record")
    return int(match.group(1))


def serialize_records(records: list[str], title: str) -> str:
    """Compose records into a lossless CADe_SIMU document.

    CADe_SIMU free-text records use a special transition: the next record starts
    immediately after the text payload instead of being prefixed by '#'.
    """
    if not records:
        return "CADe_SIMU" + build_trailer(title)

    chunks = ["CADe_SIMU", records[0]]
    previous_type = record_type(records[0])
    for raw in records[1:]:
        chunks.append("" if previous_type == int(CadType.FREE_TEXT) else "#")
        chunks.append(raw)
        previous_type = record_type(raw)
    chunks.append(build_trailer(title))

    cad_text = "".join(chunks)
    if CadDocument.parse(cad_text).dumps() != cad_text:
        raise RuntimeError("generated CADe_SIMU text failed internal round-trip")
    return cad_text
