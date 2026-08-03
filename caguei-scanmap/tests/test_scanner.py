import asyncio

import pytest

from caguei_scanmap.scanner import _check_port, scan_target


class FakeWriter:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        return None


@pytest.mark.asyncio
async def test_check_port_returns_open_service() -> None:
    writer = FakeWriter()

    async def connector(host: str, port: int):
        assert (host, port) == ("127.0.0.1", 443)
        return asyncio.StreamReader(), writer

    result = await _check_port("127.0.0.1", 443, 0.1, asyncio.Semaphore(1), connector)
    assert result is not None
    assert result.service == "https"
    assert writer.closed


@pytest.mark.asyncio
async def test_scan_rejects_excessive_concurrency() -> None:
    with pytest.raises(ValueError, match="concorrência"):
        await scan_target("localhost", ["127.0.0.1"], [80], "test", concurrency=501)
