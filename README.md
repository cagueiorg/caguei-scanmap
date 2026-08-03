# Caguei ScanMap

> **Não confie. Mapeie.**  
> Network Scanner & Asset Mapper defensivo, por [caguei.org](https://caguei.org).

Caguei ScanMap é uma ferramenta de linha de comando para inventário e auditoria autorizada de
rede. Ela oferece scan TCP connect assíncrono, seleção de portas e intervalos, identificação
básica por portas conhecidas, apresentação no terminal e exportação JSON.

O **Scope Guard é obrigatório**: nenhum pacote de scan é iniciado antes de o alvo ser validado
contra um arquivo local de autorização.

## Limites éticos

Use somente em ativos próprios ou com autorização expressa. O projeto deliberadamente não
inclui evasão, stealth, exploração, bypass, força bruta, scans de vulnerabilidade ou técnicas
ofensivas avançadas. A identificação de serviços é apenas uma associação conservadora entre
porta conhecida e nome comum; não realiza captura agressiva de banners.

## Requisitos e instalação

- Python 3.12 ou superior
- Linux, macOS ou Windows

```bash
git clone https://github.com/SEU-USUARIO/caguei-scanmap.git
cd caguei-scanmap
python -m venv .venv
```

Ative o ambiente virtual e instale:

```bash
python -m pip install -e .
caguei-scanmap --help
```

Para desenvolvimento:

```bash
python -m pip install -e ".[dev]"
```

## Configure o Scope Guard

Copie o exemplo sem versionar sua autorização real:

```bash
cp scope.example.yaml scope.yaml
```

Edite `scope.yaml`:

```yaml
authorization: "Ticket SEC-2026-001"
allowed_networks:
  - "192.168.56.0/24"
allowed_hosts:
  - "scanme.internal.example"
```

`authorization` deve identificar a aprovação, ordem de serviço ou ticket. `allowed_networks`
aceita IPv4/IPv6 em CIDR. `allowed_hosts` aceita nomes DNS exatos. Para nomes autorizados por
rede, todos os endereços resolvidos precisam pertencer a uma rede permitida.

## Uso

Scan das portas padrão (`22,80,443`):

```bash
caguei-scanmap scan 192.168.56.10 --scope scope.yaml
```

Portas, listas e intervalos:

```bash
caguei-scanmap scan 192.168.56.10 --ports 22,80,443,8000-8010 --scope scope.yaml
```

Exportação JSON e ajustes operacionais:

```bash
caguei-scanmap scan 192.168.56.10 \
  --ports 1-1024 \
  --timeout 0.8 \
  --concurrency 100 \
  --scope scope.yaml \
  --output scan-results.json
```

A concorrência é limitada a 500. Comece baixo em equipamentos frágeis ou redes críticas.
Portas fechadas ou sem resposta não aparecem na tabela; o JSON registra alvo, endereços,
portas abertas, serviços estimados, horários e referência da autorização.

## Desenvolvimento e qualidade

```bash
ruff check .
ruff format --check .
pytest
```

O workflow em `.github/workflows/ci.yml` executa lint, formatação e testes em Python 3.12 e
3.13 para pushes e pull requests.

## Estrutura

```text
src/caguei_scanmap/  CLI, Scope Guard, scanner, modelos e serviços
tests/                testes unitários sem varredura externa
.github/workflows/   integração contínua
scope.example.yaml   modelo seguro de autorização
```

## Contribuição e segurança

Antes de contribuir, preserve o Scope Guard e os limites defensivos. Consulte [SECURITY.md](SECURITY.md)
para uso responsável e relato privado de vulnerabilidades.

Licença MIT. Consulte [LICENSE](LICENSE).
