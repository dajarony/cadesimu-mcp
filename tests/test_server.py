import asyncio

from cadesimu_mcp import server


def test_mcp_server_bootstraps() -> None:
    assert server.mcp is not None


def test_expected_mcp_tools_are_registered() -> None:
    tools = asyncio.run(server.mcp.list_tools())
    names = {tool.name for tool in tools}

    assert {
        "inspect_cad_text",
        "roundtrip_cad_text",
        "known_type_codes",
        "validation_status",
        "generate_three_phase_power_circuit",
        "generate_direct_starter_with_control",
        "generate_direct_starter_reference_clone",
        "generate_single_phase_lighting_circuit",
    } <= names
