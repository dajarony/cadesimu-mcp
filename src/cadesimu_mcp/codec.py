from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

HEADER = "CADe_SIMU"
TRAILER_MARKER = "#$$$"
_RECORD_HEADER = re.compile(r"(?:^|#)(\*(\d+)\*(\d+)#)")


class CadFormatError(ValueError):
    """Raised when text does not look like a CADe_SIMU document."""


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


@dataclass(frozen=True, slots=True)
class CadRecord:
    index: int
    type_code: int
    raw: str

    @property
    def data(self) -> str:
        prefix = f"*{self.index}*{self.type_code}#"
        if not self.raw.startswith(prefix):
            raise CadFormatError(f"record {self.index} has an inconsistent header")
        return self.raw[len(prefix) :]

    @property
    def hash_fields(self) -> tuple[str, ...]:
        """Fields before the first star-delimited numeric block."""
        head = self.data.split("*", 1)[0]
        return tuple(head.split("#"))

    @property
    def star_fields(self) -> tuple[str, ...]:
        """Star-delimited fields after the hash-labelled block."""
        parts = self.data.split("*", 1)
        if len(parts) == 1:
            return ()
        return tuple(parts[1].split("*"))

    @property
    def reference(self) -> str | None:
        fields = self.hash_fields
        return fields[0] or None if fields else None

    @property
    def terminals(self) -> tuple[str, ...]:
        fields = self.hash_fields
        return tuple(value for value in fields[2:] if value) if len(fields) > 2 else ()

    @property
    def x(self) -> int | None:
        fields = self.star_fields
        return _to_int(fields[8]) if len(fields) > 8 else None

    @property
    def y(self) -> int | None:
        fields = self.star_fields
        return _to_int(fields[9]) if len(fields) > 9 else None

    @property
    def x2(self) -> int | None:
        fields = self.star_fields
        return _to_int(fields[10]) if len(fields) > 10 else None

    @property
    def y2(self) -> int | None:
        fields = self.star_fields
        return _to_int(fields[11]) if len(fields) > 11 else None


@dataclass(frozen=True, slots=True)
class CadDocument:
    records: tuple[CadRecord, ...]
    trailer: str

    @classmethod
    def parse(cls, text: str) -> "CadDocument":
        if not text.startswith(HEADER):
            raise CadFormatError("missing CADe_SIMU header")

        trailer_at = text.find(TRAILER_MARKER, len(HEADER))
        if trailer_at < 0:
            body = text[len(HEADER) :]
            trailer = ""
        else:
            body = text[len(HEADER) : trailer_at]
            trailer = text[trailer_at:]

        matches = list(_RECORD_HEADER.finditer(body))
        if body and not matches:
            raise CadFormatError("no component records found")

        records: list[CadRecord] = []
        for pos, match in enumerate(matches):
            start = match.start(1)
            end = matches[pos + 1].start(1) - 1 if pos + 1 < len(matches) else len(body)
            raw = body[start:end]
            records.append(CadRecord(index=int(match.group(2)), type_code=int(match.group(3)), raw=raw))

        return cls(records=tuple(records), trailer=trailer)

    def dumps(self) -> str:
        if not self.records:
            return HEADER + self.trailer
        body = "#".join(record.raw for record in self.records)
        return HEADER + body + self.trailer

    def summary(self) -> list[dict[str, object]]:
        return [
            {
                "index": record.index,
                "type_code": record.type_code,
                "reference": record.reference,
                "terminals": list(record.terminals),
                "x": record.x,
                "y": record.y,
                "x2": record.x2,
                "y2": record.y2,
            }
            for record in self.records
        ]

    def records_of_type(self, *type_codes: int) -> Iterable[CadRecord]:
        wanted = set(type_codes)
        return (record for record in self.records if record.type_code in wanted)
