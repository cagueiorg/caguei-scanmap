"""Validated domain models."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ScopeConfig(BaseModel):
    authorization: str = Field(min_length=1)
    allowed_networks: list[str] = Field(default_factory=list)
    allowed_hosts: list[str] = Field(default_factory=list)


class PortResult(BaseModel):
    port: int = Field(ge=1, le=65535)
    state: str = "open"
    service: str = "unknown"


class ScanResult(BaseModel):
    target: str
    addresses: list[str]
    ports: list[PortResult]
    started_at: datetime
    finished_at: datetime
    authorization: str


class ScanReport(BaseModel):
    tool: str = "Caguei ScanMap"
    version: str = "0.1.0"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    results: list[ScanResult]
