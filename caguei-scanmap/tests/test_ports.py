import pytest

from caguei_scanmap.ports import parse_ports


def test_parse_ports_combines_lists_ranges_and_duplicates() -> None:
    assert parse_ports("443, 80-82,80") == [80, 81, 82, 443]


@pytest.mark.parametrize("value", ["", "0", "65536", "90-80", "abc"])
def test_parse_ports_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        parse_ports(value)
