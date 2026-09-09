from cadesimu_mcp.validation import VALIDATION_STATUS


def test_validation_state_tracks_manual_simulation_gate() -> None:
    assert VALIDATION_STATUS.power_layout_opened is True
    assert VALIDATION_STATUS.annotations_rendered is True
    assert VALIDATION_STATUS.control_layout_opened is True
    assert VALIDATION_STATUS.control_simulation_passed is False
