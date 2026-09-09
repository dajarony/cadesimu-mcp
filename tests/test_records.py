from cadesimu_mcp.codec import CadDocument
from cadesimu_mcp.model import Annotation
from cadesimu_mcp.records import (
    contactor_coil,
    junction,
    normalize_reference,
    pushbutton_nc,
    text_label,
    wire,
)
from cadesimu_mcp.writer import serialize_records


def test_record_factories_create_expected_types() -> None:
    records = [
        pushbutton_nc(0, "S0", 10, 20),
        contactor_coil(1, "KM1", 10, 40),
        wire(2, 10, 30, 10, 40, 1),
        junction(3, 10, 40, 1),
        text_label(4, Annotation("PARO NC", 30, 20)),
    ]
    doc = CadDocument.parse(serialize_records(records, "records"))
    assert [record.type_code for record in doc.records] == [8001, 9000, 4000, 4001, 8]
    assert doc.records[0].reference == "-S0"
    assert doc.records[1].reference == "-KM1"


def test_reference_normalization_rejects_cad_delimiters() -> None:
    for value in ("K#1", "K*1", ""):
        try:
            normalize_reference(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid reference accepted: {value!r}")
