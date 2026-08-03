import pytest

from caguei_scanmap.models import ScopeConfig
from caguei_scanmap.scope import ScopeError, authorize_target


@pytest.mark.asyncio
async def test_allows_ip_inside_network() -> None:
    scope = ScopeConfig(authorization="test", allowed_networks=["127.0.0.0/8"])
    assert await authorize_target("127.0.0.1", scope) == ["127.0.0.1"]


@pytest.mark.asyncio
async def test_blocks_ip_outside_network() -> None:
    scope = ScopeConfig(authorization="test", allowed_networks=["10.0.0.0/8"])
    with pytest.raises(ScopeError, match="Scope Guard bloqueou"):
        await authorize_target("192.0.2.10", scope)


@pytest.mark.asyncio
async def test_explicit_hostname_is_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_resolve(_: str) -> list[str]:
        return ["203.0.113.5"]

    monkeypatch.setattr("caguei_scanmap.scope.resolve_target", fake_resolve)
    scope = ScopeConfig(authorization="test", allowed_hosts=["asset.example"])
    assert await authorize_target("ASSET.EXAMPLE", scope) == ["203.0.113.5"]
