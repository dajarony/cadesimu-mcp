from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.components import CadType
from cadesimu_mcp.generator import SinglePhaseLightingSpec, build_single_phase_lighting_circuit


def test_single_phase_lighting_contains_expected_components() -> None:
    cad_text = build_single_phase_lighting_circuit(SinglePhaseLightingSpec())
    doc = CadDocument.parse(cad_text)
    codes = [record.type_code for record in doc.records]

    assert doc.dumps() == cad_text
    for expected in (
        CadType.SUPPLY_OR_TERMINAL_VARIANT,
        CadType.TWO_POLE_RCD,
        CadType.TWO_POLE_BREAKER,
        CadType.MAINTAINED_SWITCH_NO,
        CadType.INDICATOR_LAMP,
        CadType.PHASE_WIRE,
        CadType.NEUTRAL_WIRE,
        CadType.PE_WIRE,
    ):
        assert int(expected) in codes
    assert codes.count(int(CadType.TWO_POLE_BREAKER)) == 2


def test_single_phase_lighting_references_are_customizable() -> None:
    spec = SinglePhaseLightingSpec(
        main_breaker="Q10",
        residual_device="ID10",
        branch_breaker="Q11",
        switch="S10",
        lamp="H10",
        include_explanations=False,
    )
    doc = CadDocument.parse(build_single_phase_lighting_circuit(spec))
    refs = {record.reference for record in doc.records if record.reference}

    assert {"-Q10", "-ID10", "-Q11", "-S10", "-H10"} <= refs


def test_single_phase_lighting_annotations_are_aligned() -> None:
    doc = CadDocument.parse(build_single_phase_lighting_circuit(SinglePhaseLightingSpec()))
    texts = [record.raw for record in doc.records if record.type_code == int(CadType.FREE_TEXT)]

    assert any("ACOMETIDA (ALIM) - L N PE" in raw for raw in texts)
    assert any("INT MAG (IGA)" in raw for raw in texts)
    assert any("INT DIFERENCIAL (ID)" in raw for raw in texts)
    assert any("INT MAGN (INT AUTOMATICO)" in raw for raw in texts)
    assert any("INTERRUPTOR (NA)" in raw for raw in texts)
    assert any("BOMBILLA" in raw for raw in texts)
