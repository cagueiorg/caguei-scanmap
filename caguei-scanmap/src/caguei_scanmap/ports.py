"""Safe parsing of TCP port selections."""


def parse_ports(value: str) -> list[int]:
    """Parse comma-separated ports and inclusive ranges."""
    ports: set[int] = set()
    if not value.strip():
        raise ValueError("a seleção de portas não pode estar vazia")
    for raw_part in value.split(","):
        part = raw_part.strip()
        try:
            if "-" in part:
                start_text, end_text = part.split("-", maxsplit=1)
                start, end = int(start_text), int(end_text)
                if start > end:
                    raise ValueError("intervalo invertido")
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part))
        except ValueError as exc:
            raise ValueError(f"seleção de porta inválida: {part!r}") from exc
    if not ports or min(ports) < 1 or max(ports) > 65535:
        raise ValueError("portas devem estar entre 1 e 65535")
    return sorted(ports)
