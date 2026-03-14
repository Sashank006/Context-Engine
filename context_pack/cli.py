import typer
from rich.console import Console
from rich.table import Table
from context_pack.analyzer import analyze
from context_pack.llm_validator import get_api_key
from context_pack.deep_dive import start_deep_dive
from typing import Optional

app = typer.Typer()
console = Console()

@app.command()
def scan(
    path: str = ".",
    budget: int = typer.Option(2000, "--budget", "-b", help="Max token budget for context output (default: 2000)"),
    llm: Optional[str] = typer.Option(None, "--llm", help="LLM provider: gemini, openai, anthropic"),
    deep_dive: bool = typer.Option(False, "--deep-dive", "-d", help="Start interactive Deep Dive mode after analysis")
):
    """Scan a directory and generate LLM-ready context."""
    console.print(f"[blue]Scanning: {path}[/blue]")
    if budget != 2000:
        console.print(f"[yellow]Token budget set to: {budget}[/yellow]")
    if llm and not deep_dive:
        console.print(f"[yellow]LLM validation enabled: {llm}[/yellow]")

    # skip validation if deep dive is active — saves API calls
    result = analyze(path, max_tokens=budget, llm_provider=llm, skip_validation=deep_dive)

    table = Table(title="Code Files")
    table.add_column("File", style="cyan")

    for f in result['files'][:20]:
        table.add_row(f)

    if len(result['files']) > 20:
        table.add_row(f"... and {len(result['files']) - 20} more")

    console.print(f"[green]Found {len(result['files'])} files[/green]\n")
    console.print(table)
    console.print(result['context'])

    # --- DEEP DIVE MODE ---
    if deep_dive:
        if not llm:
            console.print("[red]Deep Dive requires --llm. Example: --llm gemini[/red]")
            return
        api_key = get_api_key(llm)
        if not api_key:
            console.print(f"[red]No API key found for {llm}. Set {llm.upper()}_API_KEY environment variable.[/red]")
            return
        start_deep_dive(result["context"], llm, api_key, result["ranked_files"])

if __name__ == "__main__":
    app()