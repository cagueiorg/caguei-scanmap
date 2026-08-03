"""Conservative service labels based on well-known TCP ports."""

SERVICES = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "domain",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    445: "microsoft-ds",
    587: "submission",
    993: "imaps",
    995: "pop3s",
    3306: "mysql",
    3389: "ms-wbt-server",
    5432: "postgresql",
    6379: "redis",
    8080: "http-alt",
    8443: "https-alt",
}


def identify_service(port: int) -> str:
    return SERVICES.get(port, "unknown")
