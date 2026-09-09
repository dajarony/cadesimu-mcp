from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.generator import PowerCircuitSpec, build_three_phase_power_circuit


def test_generated_power_circuit_roundtrips() -> None:
    cad_text = build_three_phase_power_circuit()
    doc = CadDocument.parse(cad_text)

    assert doc.dumps() == cad_text
    assert len(doc.records) == 17
    assert [record.type_code for record in doc.records[:5]] == [3004, 6009, 2001, 6007, 1000]
    assert [record.type_code for record in doc.records[5:]] == [4000] * 12


def test_generated_references_and_positions() -> None:
    cad_text = build_three_phase_power_circuit(
        PowerCircuitSpec(
            protection="QF1",
            contactor="KM1",
            overload="FR1",
            motor="M1",
            title="Power test",
            x=90,
            y=60,
        )
    )
    doc = CadDocument.parse(cad_text)

    assert doc.records[1].reference == "-QF1"
    assert doc.records[2].reference == "-KM1"
    assert doc.records[3].reference == "-FR1"
    assert doc.records[4].reference == "-M1"
    assert (doc.records[0].x, doc.records[0].y) == (90, 60)
    assert (doc.records[4].x, doc.records[4].y) == (90, 138)


def test_references_reject_delimiters() -> None:
    try:
        build_three_phase_power_circuit(PowerCircuitSpec(contactor="K#1"))
    except ValueError as exc:
        assert "cannot contain" in str(exc)
    else:
        raise AssertionError("invalid CADe_SIMU reference was accepted")
