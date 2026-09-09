from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .codec import CadDocument
from .components import TYPE_CODES, type_name
from .generator import PowerCircuitSpec, build_three_phase_power_circuit

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


@mcp.tool()
def generate_three_phase_power_circuit(
    protection: str = "Q1",
    contactor: str = "K1",
    overload: str = "F1",
    motor: str = "M1",
    title: str = "Auralis Power",
    include_explanations: bool = True,
) -> dict[str, object]:
    """Generate a CADe_SIMU direct-starter power circuit.

    The electrical power layout has been manually validated in CADe_SIMU.
    Optional explanatory text labels use the observed CADe_SIMU text-record
    format and are independently testable.
    """
    spec = PowerCircuitSpec(
        protection=protection,
        contactor=contactor,
        overload=overload,
        motor=motor,
        title=title,
        include_explanations=include_explanations,
    )
    cad_text = build_three_phase_power_circuit(spec)
    doc = CadDocument.parse(cad_text)
    return {
        "power_layout_validated_in_cadesimu": True,
        "annotations_requested": include_explanations,
        "annotations_validation_pending": include_explanations,
        "record_count": len(doc.records),
        "cad_text": cad_text,
        "next_step": (
            "Save cad_text as a .cad file and open it in CADe_SIMU; if labels render correctly, "
            "annotation support can be marked validated."
            if include_explanations
            else "Save cad_text as a .cad file and open it in CADe_SIMU."
        ),
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
