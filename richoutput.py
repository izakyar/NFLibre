from rich.console import Console
console = Console()

YAY_STYLE = "bold green"
FAIL_STYLE = "bold red"
WARN_STYLE = "bold yellow"
INFO_STYLE = "bold blue"

def done(msg: str) -> None:
    console.log(f"[{YAY_STYLE}]{msg}[/]")
    return None

def emer(msg: str) -> None:
    console.log(f"[{FAIL_STYLE}]{msg}[/]")
    return None

def warn(msg: str) -> None:
    console.log(f"[{WARN_STYLE}]{msg}[/]")
    return None

def info(msg: str) -> None:
    console.log(f"[{INFO_STYLE}]{msg}[/]")
    return None
