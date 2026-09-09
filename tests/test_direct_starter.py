from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.components import CadType
from cadesimu_mcp.generator import DirectStarterSpec, build_direct_starter_with_control


def test_full_direct_starter_contains_control_and_self_hold() -> None:
    cad_text = build_direct_starter_with_control(DirectStarterSpec())
    doc = CadDocument.parse(cad_text)
    codes = [record.type_code for record in doc.records]

    assert doc.dumps() == cad_text
    for expected in (3000, 3001, 6010, 8018, 8001, 8000, 7000, 9000):
        assert expected in codes
    assert codes.count(int(CadType.JUNCTION)) >= 3


def test_control_references_match_power_references() -> None:
    spec = DirectStarterSpec(
        protection="QF7",
        contactor="KM7",
        overload="FR7",
        motor="M7",
        stop_button="S7STOP",
        start_button="S7START",
        include_explanations=False,
    )
    doc = CadDocument.parse(build_direct_starter_with_control(spec))
    refs = [record.reference for record in doc.records if record.reference]

    assert refs.count("-QF7") == 2
    assert refs.count("-KM7") == 3
    assert refs.count("-FR7") == 2
    assert "-M7" in refs
    assert "-S7STOP" in refs
    assert "-S7START" in refs


def test_coil_is_emitted_before_self_hold_auxiliary_contact() -> None:
    """CADe_SIMU momentary START depends on the observed device scan order."""
    doc = CadDocument.parse(
        build_direct_starter_with_control(DirectStarterSpec(include_explanations=False))
    )
    km1_records = [record for record in doc.records if record.reference == "-KM1"]

    coil = next(record for record in km1_records if record.type_code == 9000)
    auxiliary = next(record for record in km1_records if record.type_code == 7000)
    assert coil.index < auxiliary.index


def test_annotations_are_aligned_with_control_component_rows() -> None:
    doc = CadDocument.parse(build_direct_starter_with_control(DirectStarterSpec()))
    texts = [record for record in doc.records if record.type_code == int(CadType.FREE_TEXT)]
    raws = [record.raw for record in texts]

    assert any("S0 11-12 - PARO NC" in raw for raw in raws)
    assert any("S1 13-14 - MARCHA NO" in raw for raw in raws)
    assert any("KM1 aux 13-14 - automantenimiento" in raw for raw in raws)
    assert any("KM1 A1-A2 - bobina del contactor" in raw for raw in raws)

    stop_label = next(record for record in texts if "S0 11-12" in record.raw)
    start_label = next(record for record in texts if "S1 13-14" in record.raw)
    coil_label = next(record for record in texts if "KM1 A1-A2" in record.raw)
    assert stop_label.y == 101
    assert start_label.y == 119
    assert coil_label.y == 137
