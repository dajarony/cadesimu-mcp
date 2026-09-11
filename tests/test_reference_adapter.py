from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.model import DirectStarterSpec
from cadesimu_mcp.reference_adapter import build_direct_starter_reference_clone
from cadesimu_mcp.reference_templates import DIRECT_STARTER_REFERENCE


def test_default_reference_clone_is_exact_template() -> None:
    cad_text = build_direct_starter_reference_clone(
        DirectStarterSpec(
            protection="Q1",
            contactor="K1",
            overload="F1",
            motor="M",
            stop_button="S0",
            start_button="S1",
            include_explanations=False,
        )
    )
    assert cad_text == DIRECT_STARTER_REFERENCE


def test_reference_clone_only_renames_component_markers() -> None:
    cad_text = build_direct_starter_reference_clone(
        DirectStarterSpec(
            protection="QF1",
            contactor="KM1",
            overload="FR1",
            motor="M1",
            stop_button="STOP",
            start_button="START",
            include_explanations=False,
        )
    )

    assert "#-QF1#" in cad_text
    assert "#-KM1#" in cad_text
    assert "#-FR1#" in cad_text
    assert "#-M1#" in cad_text
    assert "#-STOP#" in cad_text
    assert "#-START#" in cad_text
    assert CadDocument.parse(cad_text).dumps() == cad_text


def test_reference_clone_preserves_wire_and_junction_counts() -> None:
    reference = CadDocument.parse(DIRECT_STARTER_REFERENCE).summary()
    clone = CadDocument.parse(
        build_direct_starter_reference_clone(
            DirectStarterSpec(
                protection="QF1",
                contactor="KM1",
                overload="FR1",
                motor="M1",
                stop_button="S0",
                start_button="S1",
                include_explanations=False,
            )
        )
    ).summary()

    reference_types = [record["type_code"] for record in reference]
    clone_types = [record["type_code"] for record in clone]
    assert clone_types == reference_types
