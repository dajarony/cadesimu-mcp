from cadesimu_mcp.codec import CadDocument, CadFormatError


SAMPLE = (
    "CADe_SIMU"
    "*0*9999#-X##A#B#######*0*0*0*0*0*0*0*0*10*20*0*0"
    "#*1*4000##########*0*0*0*0*0*0*0*0*10*20*10*40"
    "#$$$*fixture"
)


def test_roundtrip_is_exact() -> None:
    doc = CadDocument.parse(SAMPLE)
    assert doc.dumps() == SAMPLE
    assert len(doc.records) == 2


def test_extracts_basic_record_metadata() -> None:
    doc = CadDocument.parse(SAMPLE)
    first = doc.records[0]
    wire = doc.records[1]

    assert first.index == 0
    assert first.type_code == 9999
    assert first.reference == "-X"
    assert first.terminals == ("A", "B")
    assert (first.x, first.y) == (10, 20)
    assert (wire.x, wire.y, wire.x2, wire.y2) == (10, 20, 10, 40)


def test_rejects_non_cadesimu_text() -> None:
    try:
        CadDocument.parse("not a CADe_SIMU file")
    except CadFormatError:
        pass
    else:
        raise AssertionError("expected CadFormatError")
