from cadesimu_mcp import server


def test_mcp_server_bootstraps() -> None:
    assert server.mcp is not None
