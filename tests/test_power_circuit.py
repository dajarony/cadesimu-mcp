from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.components import CadType
from cadesimu_mcp.generator import PowerCircuitSpec, build_three_phase_power_circuit
from cadesimu_mcp.layout import PowerLayout


def test_generated_power_circuit_roundtrips() -> None:
    cad_text = build_three_phase_power_circuit()
    doc = CadDocument.parse(cad_text)

    assert doc.dumps() == cad_text
    assert len(doc.records) == 17
    assert [record.type_code for record in doc.records[:5]] == [3004, 6009, 2001, 6007, 1000]
    assert [record.type_code for record in doc.records[5:]] == [int(CadType.WIRE)] * 12


def test_generated_references_and_positions() -> None:
    cad_text = build_three_phase_power_circuit(
        PowerCircuitSpec(
            protection="QF1",
            contactor="KM1",
            overload="FR1",
            motor="M1",
            title="Power test",
        ),
        PowerLayout(x=90, y=60),
    )
    doc = CadDocument.parse(cad_text)

    assert doc.records[1].reference == "-QF1"
    assert doc.records[2].reference == "-KM1"
    assert doc.records[3].reference == "-FR1"
    assert doc.records[4].reference == "-M1"
    assert (doc.records[0].x, doc.records[0].y) == (90, 60)
    assert (doc.records[4].x, doc.records[4].y) == (90, 138)


def test_explanatory_labels_are_optional_and_have_no_visible_hash_separator() -> None:
    cad_text = build_three_phase_power_circuit(PowerCircuitSpec(include_explanations=True))
    doc = CadDocument.parse(cad_text)
    text_records = [record for record in doc.records if record.type_code == int(CadType.FREE_TEXT)]

    assert doc.dumps() == cad_text
    assert len(text_records) == 6
    assert "FUERZA*" in cad_text
    assert "FUERZA#*" not in cad_text
