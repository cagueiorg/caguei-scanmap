"""Command-line interface."""

import asyncio
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .models import ScanReport, ScanResult
from .ports import parse_ports
from .scanner import scan_target
from .scope import ScopeError, authorize_target, load_scope

app = typer.Typer(
    name="caguei-scanmap",
    help="Caguei ScanMap — Não confie. Mapeie. Auditoria defensiva autorizada.",
    no_args_is_help=True,
)
console = Console()
error_console = Console(stderr=True)


def _render(result: ScanResult) -> None:
    table = Table(title=f"{result.target} ({', '.join(result.addresses)})")
    table.add_column("Porta", justify="right", style="cyan")
    table.add_column("Estado", style="green")
    table.add_column("Serviço")
    for item in result.ports:
        table.add_row(str(item.port), item.state, item.service)
    console.print(table)
    console.print(f"[bold]{len(result.ports)}[/bold] porta(s) aberta(s).")


@app.command()
def scan(
    target: Annotated[str, typer.Argument(help="IP ou hostname autorizado")],
    ports: Annotated[
        str, typer.Option("--ports", "-p", help="Portas, listas ou intervalos")
    ] = "22,80,443",
    scope_file: Annotated[Path, typer.Option("--scope", help="Arquivo YAML de autorização")] = Path(
        "scope.yaml"
    ),
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Exportar relatório JSON")
    ] = None,
    timeout: Annotated[float, typer.Option(help="Timeout por conexão, em segundos")] = 1.0,
    concurrency: Annotated[int, typer.Option(help="Máximo de conexões simultâneas (1–500)")] = 100,
) -> None:
    """Executa scan TCP connect somente após validação pelo Scope Guard."""
    console.print("[bold cyan]Caguei ScanMap[/bold cyan] — Não confie. Mapeie.")
    console.print("[dim]Network auditing tool by caguei.org · ambientes autorizados somente[/dim]")
    try:
        scope = load_scope(scope_file)
        selected_ports = parse_ports(ports)
        addresses = asyncio.run(authorize_target(target, scope))
        console.print(
            f"[green]Scope Guard aprovado[/green] · {scope.authorization} · "
            f"{len(selected_ports)} porta(s)"
        )
        result = asyncio.run(
            scan_target(
                target,
                addresses,
                selected_ports,
                scope.authorization,
                timeout=timeout,
                concurrency=concurrency,
            )
        )
    except (ScopeError, ValueError) as exc:
        error_console.print(f"[bold red]Bloqueado:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc
    _render(result)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        report = ScanReport(results=[result])
        output.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"Relatório salvo em [bold]{output}[/bold]")


def version_callback(value: bool) -> None:
    if value:
        console.print(f"Caguei ScanMap {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Caguei ScanMap — Não confie. Mapeie."""


if __name__ == "__main__":
    app()
