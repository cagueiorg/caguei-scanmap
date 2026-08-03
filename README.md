# Caguei ScanMap

```text
   ██████╗ █████╗  ██████╗ ██╗   ██╗███████╗██╗
  ██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔════╝██║
  ██║     ███████║██║  ███╗██║   ██║█████╗  ██║
  ██║     ██╔══██║██║   ██║██║   ██║██╔══╝  ██║
  ╚██████╗██║  ██║╚██████╔╝╚██████╔╝███████╗██║
   ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝

        ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ███╗ █████╗ ██████╗
        ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗ ████║██╔══██╗██╔══██╗
        ███████╗██║     ███████║██╔██╗ ██║██╔████╔██║███████║██████╔╝
        ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝
        ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚═╝ ██║██║  ██║██║
        ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

                    Não confie. Mapeie.
                       by caguei.org
```

> **Não confie. Mapeie. — Don't trust. Map it.**  
> A defensive Network Scanner & Asset Mapper by [caguei.org](https://caguei.org).

Caguei ScanMap is a command-line tool for authorized network inventory and auditing. It
provides asynchronous TCP connect scanning, individual port and range selection, basic
well-known service identification, rich terminal output, and JSON exports.

The **Scope Guard is mandatory**: no scan connection is attempted until the target has been
validated against a local authorization file.

## Ethical boundaries

Use this tool only on assets you own or have explicit permission to audit. The project
deliberately excludes evasion, stealth, exploitation, bypass, brute force, vulnerability
scanning, and advanced offensive techniques. Service identification is a conservative mapping
of well-known ports to common service names; it does not perform aggressive banner grabbing.

## Requirements and installation

- Python 3.12 or newer
- Linux, macOS ou Windows

```bash
git clone https://github.com/cagueiorg/caguei-scanmap.git
cd caguei-scanmap
python -m venv .venv
```

Activate the virtual environment and install the project:

```bash
python -m pip install -e .
caguei-scanmap --help
```

For development:

```bash
python -m pip install -e ".[dev]"
```

## Configure the Scope Guard

Copy the example without committing your real authorization file:

```bash
cp scope.example.yaml scope.yaml
```

Edit `scope.yaml`:

```yaml
authorization: "Ticket SEC-2026-001"
allowed_networks:
  - "192.168.56.0/24"
allowed_hosts:
  - "scanme.internal.example"
```

`authorization` should identify the approval, work order, or ticket. `allowed_networks` accepts
IPv4 and IPv6 CIDR ranges. `allowed_hosts` accepts exact DNS names. When a hostname is
authorized through a network, every resolved address must belong to an allowed network.

## Usage

Scan the default ports (`22,80,443`):

```bash
caguei-scanmap scan 192.168.56.10 --scope scope.yaml
```

Select individual ports, lists, and ranges:

```bash
caguei-scanmap scan 192.168.56.10 --ports 22,80,443,8000-8010 --scope scope.yaml
```

Export JSON and adjust operational limits:

```bash
caguei-scanmap scan 192.168.56.10 \
  --ports 1-1024 \
  --timeout 0.8 \
  --concurrency 100 \
  --scope scope.yaml \
  --output scan-results.json
```

Concurrency is capped at 500. Start with a low value when auditing fragile devices or critical
networks. Closed or unresponsive ports are omitted from the table. The JSON report records the
target, resolved addresses, open ports, estimated services, timestamps, and authorization
reference.

## Development and quality

```bash
ruff check .
ruff format --check .
pytest
```

The workflow at `.github/workflows/ci.yml` runs linting, formatting checks, and tests on Python
3.12 and 3.13 for every push and pull request.

## Project structure

```text
src/caguei_scanmap/  CLI, Scope Guard, scanner, models, and services
tests/                unit tests with no external network scanning
.github/workflows/   continuous integration
scope.example.yaml   safe authorization template
```

## Contributing and security

Contributions must preserve the Scope Guard and the project's defensive boundaries. Read
[SECURITY.md](SECURITY.md) for responsible-use requirements and private vulnerability
reporting instructions.

Released under the MIT License. See [LICENSE](LICENSE).
