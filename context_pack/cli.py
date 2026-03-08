import typer
from rich.console import Console
from rich.table import Table
from context_pack.analyzer import analyze
from typing import Optional

app = typer.Typer()
console = Console()

@app.command()
def scan(
    path: str = ".",
    budget: int = typer.Option(2000, "--budget", "-b", help="Max token budget for context output (default: 2000)"),
    llm: Optional[str] = typer.Option(None, "--llm", help="LLM provider for validation: gemini, openai, anthropic")
):
    """Scan a directory and generate LLM-ready context."""
    console.print(f"[blue]Scanning: {path}[/blue]")
    if budget != 2000:
        console.print(f"[yellow]Token budget set to: {budget}[/yellow]")
    if llm:
        console.print(f"[yellow]LLM validation enabled: {llm}[/yellow]")

    result = analyze(path, max_tokens=budget, llm_provider=llm)

    table = Table(title="Code Files")
    table.add_column("File", style="cyan")

    for f in result['files'][:20]:
        table.add_row(f)

    if len(result['files']) > 20:
        table.add_row(f"... and {len(result['files']) - 20} more")

    console.print(f"[green]Found {len(result['files'])} files[/green]\n")
    console.print(table)
    console.print(result['context'])

if __name__ == "__main__":
    app()