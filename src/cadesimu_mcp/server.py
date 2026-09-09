from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .codec import CadDocument
from .components import TYPE_CODES, type_name
from .generator import (
    DirectStarterSpec,
    PowerCircuitSpec,
    build_direct_starter_with_control,
    build_three_phase_power_circuit,
)

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
    """Generate the manually validated CADe_SIMU power side of a direct starter."""
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
        "annotation_records_validated_in_cadesimu": True,
        "record_count": len(doc.records),
        "cad_text": cad_text,
    }


@mcp.tool()
def generate_direct_starter_with_control(
    protection: str = "QF1",
    contactor: str = "KM1",
    overload: str = "FR1",
    motor: str = "M1",
    stop_button: str = "S0",
    start_button: str = "S1",
    title: str = "Auralis Direct Starter",
    include_explanations: bool = True,
) -> dict[str, object]:
    """Generate power + STOP/START control + KM1 self-hold.

    The power and annotation record families are already validated in the target
    CADe_SIMU version. The combined control layout is the next validation step.
    """
    spec = DirectStarterSpec(
        protection=protection,
        contactor=contactor,
        overload=overload,
        motor=motor,
        stop_button=stop_button,
        start_button=start_button,
        title=title,
        include_explanations=include_explanations,
    )
    cad_text = build_direct_starter_with_control(spec)
    doc = CadDocument.parse(cad_text)
    return {
        "power_layout_validated_in_cadesimu": True,
        "annotation_records_validated_in_cadesimu": True,
        "control_layout_validation_pending": True,
        "record_count": len(doc.records),
        "cad_text": cad_text,
        "next_step": "Open the generated .cad in CADe_SIMU and test START/STOP simulation.",
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
