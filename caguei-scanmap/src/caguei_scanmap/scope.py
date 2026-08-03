"""Mandatory target authorization checks."""

import ipaddress
import socket
from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import ScopeConfig


class ScopeError(ValueError):
    """Raised when a target is not explicitly authorized."""


def load_scope(path: Path) -> ScopeConfig:
    if not path.is_file():
        raise ScopeError(f"arquivo de escopo não encontrado: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        scope = ScopeConfig.model_validate(data)
        for network in scope.allowed_networks:
            ipaddress.ip_network(network, strict=False)
    except (OSError, yaml.YAMLError, ValidationError, ValueError) as exc:
        raise ScopeError(f"arquivo de escopo inválido: {exc}") from exc
    if not scope.allowed_networks and not scope.allowed_hosts:
        raise ScopeError("o escopo precisa autorizar ao menos uma rede ou host")
    return scope


async def resolve_target(target: str) -> list[str]:
    try:
        direct = ipaddress.ip_address(target)
        return [str(direct)]
    except ValueError:
        pass
    loop = __import__("asyncio").get_running_loop()
    try:
        records = await loop.getaddrinfo(target, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ScopeError(f"não foi possível resolver {target!r}") from exc
    return sorted({record[4][0] for record in records})


async def authorize_target(target: str, scope: ScopeConfig) -> list[str]:
    addresses = await resolve_target(target)
    networks = [ipaddress.ip_network(item, strict=False) for item in scope.allowed_networks]
    hostname_allowed = target.rstrip(".").lower() in {
        host.rstrip(".").lower() for host in scope.allowed_hosts
    }
    unauthorized = [
        address
        for address in addresses
        if not hostname_allowed
        and not any(ipaddress.ip_address(address) in network for network in networks)
    ]
    if unauthorized:
        raise ScopeError(
            f"Scope Guard bloqueou {target!r}; endereços fora do escopo: " + ", ".join(unauthorized)
        )
    return addresses
