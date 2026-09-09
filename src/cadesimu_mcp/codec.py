from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

HEADER = "CADe_SIMU"
TRAILER_MARKER = "#$$$"
_HEADER_AT_START = re.compile(r"\*(\d+)\*(\d+)#")
_HEADER_AFTER_SEPARATOR = re.compile(r"#\*(\d+)\*(\d+)#")
_HEADER_WITHOUT_SEPARATOR = re.compile(r"\*(\d+)\*(\d+)#")


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
    """One raw CADe_SIMU record plus lossless separator metadata."""

    index: int
    type_code: int
    raw: str
    separator_before: str = ""

    @property
    def data(self) -> str:
        prefix = f"*{self.index}*{self.type_code}#"
        if not self.raw.startswith(prefix):
            raise CadFormatError(f"record {self.index} has an inconsistent header")
        return self.raw[len(prefix) :]

    @property
    def hash_fields(self) -> tuple[str, ...]:
        head = self.data.split("*", 1)[0]
        return tuple(head.split("#"))

    @property
    def star_fields(self) -> tuple[str, ...]:
        parts = self.data.split("*", 1)
        if len(parts) == 1:
            return ()
        return tuple(parts[1].split("*"))

    @property
    def reference(self) -> str | None:
        fields = self.hash_fields
        return (fields[0] or None) if fields else None

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
    """Lossless parsed CADe_SIMU document."""

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

        if not body:
            return cls(records=(), trailer=trailer)

        first = _HEADER_AT_START.match(body)
        if not first:
            raise CadFormatError("first component record does not start after CADe_SIMU header")

        records: list[CadRecord] = []
        current_start = 0
        current_index = int(first.group(1))
        current_type = int(first.group(2))
        separator_before = ""

        while True:
            if current_type == 8:
                next_match = cls._next_after_text(body, current_start)
                if next_match is None:
                    next_start = len(body)
                    next_separator = ""
                else:
                    next_start = next_match.start()
                    next_separator = ""
            else:
                next_match = _HEADER_AFTER_SEPARATOR.search(body, first.end())
                if next_match is None:
                    next_start = len(body)
                    next_separator = ""
                else:
                    next_start = next_match.start()
                    next_separator = "#"

            raw = body[current_start:next_start]
            records.append(
                CadRecord(
                    index=current_index,
                    type_code=current_type,
                    raw=raw,
                    separator_before=separator_before,
                )
            )

            if next_match is None:
                break

            if next_separator == "#":
                header_start = next_match.start() + 1
                current_index = int(next_match.group(1))
                current_type = int(next_match.group(2))
            else:
                header_start = next_match.start()
                current_index = int(next_match.group(1))
                current_type = int(next_match.group(2))

            current_start = header_start
            separator_before = next_separator
            first = _HEADER_AT_START.match(body, current_start)
            if first is None:
                raise CadFormatError("malformed component record header")

        return cls(records=tuple(records), trailer=trailer)

    @staticmethod
    def _next_after_text(body: str, record_start: int) -> re.Match[str] | None:
        """Locate the record immediately following a type-8 free-text object."""
        header = _HEADER_AT_START.match(body, record_start)
        if header is None:
            return None

        numeric_start = body.find("*", header.end())
        if numeric_start < 0:
            return None
        payload_start = body.find("#", numeric_start)
        if payload_start < 0:
            return None
        return _HEADER_WITHOUT_SEPARATOR.search(body, payload_start + 1)

    def dumps(self) -> str:
        body = "".join(record.separator_before + record.raw for record in self.records)
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
