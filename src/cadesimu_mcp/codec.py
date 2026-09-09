from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

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


def _split_body_and_trailer(text: str) -> tuple[str, str]:
    if not text.startswith(HEADER):
        raise CadFormatError("missing CADe_SIMU header")

    trailer_at = text.find(TRAILER_MARKER, len(HEADER))
    if trailer_at < 0:
        return text[len(HEADER) :], ""
    return text[len(HEADER) : trailer_at], text[trailer_at:]


def _require_header(body: str, position: int) -> re.Match[str]:
    header = _HEADER_AT_START.match(body, position)
    if header is None:
        raise CadFormatError("malformed component record header")
    return header


@dataclass(frozen=True, slots=True)
class _NextBoundary:
    raw_end: int
    header_start: int
    separator: str


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


def _next_boundary(
    body: str,
    record_start: int,
    type_code: int,
    header_end: int,
) -> _NextBoundary | None:
    if type_code == 8:
        next_match = _next_after_text(body, record_start)
        if next_match is None:
            return None
        return _NextBoundary(
            raw_end=next_match.start(),
            header_start=next_match.start(),
            separator="",
        )

    next_match = _HEADER_AFTER_SEPARATOR.search(body, header_end)
    if next_match is None:
        return None
    return _NextBoundary(
        raw_end=next_match.start(),
        header_start=next_match.start() + 1,
        separator="#",
    )


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
    def parse(cls, text: str) -> CadDocument:
        body, trailer = _split_body_and_trailer(text)
        if not body:
            return cls(records=(), trailer=trailer)

        current_start = 0
        separator_before = ""
        records: list[CadRecord] = []

        while current_start < len(body):
            header = _require_header(body, current_start)
            index = int(header.group(1))
            type_code = int(header.group(2))
            boundary = _next_boundary(body, current_start, type_code, header.end())
            raw_end = boundary.raw_end if boundary else len(body)

            records.append(
                CadRecord(
                    index=index,
                    type_code=type_code,
                    raw=body[current_start:raw_end],
                    separator_before=separator_before,
                )
            )

            if boundary is None:
                break
            current_start = boundary.header_start
            separator_before = boundary.separator

        return cls(records=tuple(records), trailer=trailer)

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
