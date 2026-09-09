from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .codec import CadDocument
from .components import TYPE_CODES, type_name

mcp = FastMCP("cadesimu")


@mcp.tool()
def inspect_cad_text(cad_text: str) -> dict[str, object]:
    """Parse CADe_SIMU text and return a non-destructive component summary."""
    doc = CadDocument.parse(cad_text)
    records = doc.summary()
    for record in records:
        record["type_name"] = type_name(int(record["type_code"]))
    return {
        "record_count": len(records),
        "has_trailer": bool(doc.trailer),
        "records": records,
    }


@mcp.tool()
def roundtrip_cad_text(cad_text: str) -> dict[str, object]:
    """Check whether the current parser can reconstruct a CADe_SIMU document exactly."""
    doc = CadDocument.parse(cad_text)
    rebuilt = doc.dumps()
    result: dict[str, object] = {
        "exact": rebuilt == cad_text,
        "record_count": len(doc.records),
    }
    if rebuilt != cad_text:
        result["rebuilt"] = rebuilt
    return result


@mcp.tool()
def known_type_codes() -> dict[str, str]:
    """Return provisional CADe_SIMU component type-code mappings."""
    return {str(code): name for code, name in sorted(TYPE_CODES.items())}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
