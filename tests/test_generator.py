from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.generator import (
    DirectStarterSpec,
    PowerCircuitSpec,
    build_direct_starter_with_control,
    build_three_phase_power_circuit,
)


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


def test_explanatory_labels_do_not_gain_visible_hashes() -> None:
    cad_text = build_three_phase_power_circuit(
        PowerCircuitSpec(
            protection="QF1",
            contactor="KM1",
            overload="FR1",
            motor="M1",
            include_explanations=True,
        )
    )
    doc = CadDocument.parse(cad_text)

    assert doc.dumps() == cad_text
    assert len(doc.records) == 23
    assert [record.type_code for record in doc.records[5:11]] == [8] * 6
    assert "ARRANQUE DIRECTO*6*8" in cad_text
    assert "ARRANQUE DIRECTO#*6*8" not in cad_text
    assert "QF1: proteccion del motor" in cad_text


def test_full_direct_starter_contains_control_and_self_hold() -> None:
    cad_text = build_direct_starter_with_control(DirectStarterSpec())
    doc = CadDocument.parse(cad_text)
    codes = [record.type_code for record in doc.records]

    assert doc.dumps() == cad_text
    assert 3000 in codes
    assert 3001 in codes
    assert 6010 in codes
    assert 8018 in codes
    assert 8001 in codes
    assert 8000 in codes
    assert 7000 in codes
    assert 9000 in codes
    assert codes.count(4001) >= 3
    assert "S0: pulsador PARO normalmente cerrado" in cad_text
    assert "S1: pulsador MARCHA normalmente abierto" in cad_text


def test_references_reject_delimiters() -> None:
    try:
        build_three_phase_power_circuit(PowerCircuitSpec(contactor="K#1"))
    except ValueError as exc:
        assert "cannot contain" in str(exc)
    else:
        raise AssertionError("invalid CADe_SIMU reference was accepted")
