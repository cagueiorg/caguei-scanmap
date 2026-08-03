"""Asynchronous TCP connect scanner."""

import asyncio
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

from .models import PortResult, ScanResult
from .services import identify_service

Connector = Callable[[str, int], Awaitable[tuple[asyncio.StreamReader, asyncio.StreamWriter]]]


async def _check_port(
    address: str,
    port: int,
    timeout: float,
    semaphore: asyncio.Semaphore,
    connector: Connector = asyncio.open_connection,
) -> PortResult | None:
    async with semaphore:
        writer: asyncio.StreamWriter | None = None
        try:
            _, writer = await asyncio.wait_for(connector(address, port), timeout=timeout)
            return PortResult(port=port, service=identify_service(port))
        except (TimeoutError, OSError):
            return None
        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()


async def scan_target(
    target: str,
    addresses: list[str],
    ports: list[int],
    authorization: str,
    *,
    timeout: float = 1.0,
    concurrency: int = 100,
) -> ScanResult:
    if timeout <= 0:
        raise ValueError("timeout deve ser maior que zero")
    if not 1 <= concurrency <= 500:
        raise ValueError("concorrência deve estar entre 1 e 500")
    started_at = datetime.now(UTC)
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [
        _check_port(address, port, timeout, semaphore) for address in addresses for port in ports
    ]
    scanned = await asyncio.gather(*tasks)
    open_ports = sorted(
        {result.port: result for result in scanned if result is not None}.values(),
        key=lambda result: result.port,
    )
    return ScanResult(
        target=target,
        addresses=addresses,
        ports=open_ports,
        started_at=started_at,
        finished_at=datetime.now(UTC),
        authorization=authorization,
    )
