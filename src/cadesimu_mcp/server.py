from __future__ import annotations

from mcp.server import MCPServer

from .codec import CadDocument
from .components import TYPE_CODES, type_name
from .generator import (
    DirectStarterSpec,
    PowerCircuitSpec,
    SinglePhaseLightingSpec,
    build_direct_starter_reference_clone,
    build_direct_starter_with_control,
    build_single_phase_lighting_circuit,
    build_three_phase_power_circuit,
)
from .validation import VALIDATION_STATUS

mcp = MCPServer("cadesimu")


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
    """Check whether the parser can reconstruct a CADe_SIMU document exactly."""
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
    """Return observed CADe_SIMU component type-code mappings."""
    return {str(code): name for code, name in sorted(TYPE_CODES.items())}


@mcp.tool()
def validation_status() -> dict[str, bool]:
    """Return the current manual validation state against CADe_SIMU."""
    return VALIDATION_STATUS.as_dict()


@mcp.tool()
def generate_three_phase_power_circuit(
    protection: str = "QF1",
    contactor: str = "KM1",
    overload: str = "FR1",
    motor: str = "M1",
    title: str = "Auralis Power",
    include_explanations: bool = True,
) -> dict[str, object]:
    """Generate the validated CADe_SIMU power side of a direct starter."""
    cad_text = build_three_phase_power_circuit(
        PowerCircuitSpec(
            protection=protection,
            contactor=contactor,
            overload=overload,
            motor=motor,
            title=title,
            include_explanations=include_explanations,
        )
    )
    return {
        "validation": VALIDATION_STATUS.as_dict(),
        "record_count": len(CadDocument.parse(cad_text).records),
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
    """Generate power + STOP/START control + KM1 self-hold synthetically."""
    cad_text = build_direct_starter_with_control(
        DirectStarterSpec(
            protection=protection,
            contactor=contactor,
            overload=overload,
            motor=motor,
            stop_button=stop_button,
            start_button=start_button,
            title=title,
            include_explanations=include_explanations,
        )
    )
    return {
        "validation": VALIDATION_STATUS.as_dict(),
        "record_count": len(CadDocument.parse(cad_text).records),
        "cad_text": cad_text,
        "next_step": (
            "Open the generated .cad in CADe_SIMU and validate START/STOP simulation."
            if not VALIDATION_STATUS.control_simulation_passed
            else "Control simulation is validated."
        ),
    }


@mcp.tool()
def generate_direct_starter_reference_clone(
    protection: str = "QF1",
    contactor: str = "KM1",
    overload: str = "FR1",
    motor: str = "M1",
    stop_button: str = "S0",
    start_button: str = "S1",
) -> dict[str, object]:
    """Clone a canonical working starter without regenerating network metadata."""
    cad_text = build_direct_starter_reference_clone(
        DirectStarterSpec(
            protection=protection,
            contactor=contactor,
            overload=overload,
            motor=motor,
            stop_button=stop_button,
            start_button=start_button,
            include_explanations=False,
        )
    )
    return {
        "reference_preserving": True,
        "record_count": len(CadDocument.parse(cad_text).records),
        "cad_text": cad_text,
        "next_step": "Open in CADe_SIMU and test one momentary START, then STOP.",
    }


@mcp.tool()
def generate_single_phase_lighting_circuit(
    main_breaker: str = "Q1",
    residual_device: str = "F",
    branch_breaker: str = "Q2",
    switch: str = "S1",
    lamp: str = "H1",
    title: str = "Auralis Monofasico",
    include_explanations: bool = True,
) -> dict[str, object]:
    """Generate L/N/PE + IGA + differential + breaker + switch + lamp."""
    cad_text = build_single_phase_lighting_circuit(
        SinglePhaseLightingSpec(
            main_breaker=main_breaker,
            residual_device=residual_device,
            branch_breaker=branch_breaker,
            switch=switch,
            lamp=lamp,
            title=title,
            include_explanations=include_explanations,
        )
    )
    return {
        "validated_in_cadesimu": False,
        "record_count": len(CadDocument.parse(cad_text).records),
        "cad_text": cad_text,
        "next_step": "Open the generated .cad in CADe_SIMU and test Q1, F, Q2, S1 and H1.",
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
