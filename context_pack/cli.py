import typer
from rich.console import Console
from rich.table import Table
from context_pack.analyzer import analyze

app = typer.Typer()
console = Console()

@app.command()
def scan(path: str = "."):
    """Scan a directory and list code files."""
    console.print(f"[blue]Scanning: {path}[/blue]")
    
    result = analyze(path)
    
    console.print(f"[green]Found {len(result['files'])} files[/green]\n")
    
    table = Table(title="Code Files")
    table.add_column("File", style="cyan")
    
    for f in result['files'][:20]:
        table.add_row(f)
    
    if len(result['files']) > 20:
        table.add_row(f"... and {len(result['files']) - 20} more")
    
    console.print(table)
    console.print(f"\n[yellow]Language: {result['language']}[/yellow]")
    console.print(f"[yellow]Mixed: {result['mixed']}[/yellow]")
    console.print(f"[yellow]Framework: {result['framework']}[/yellow]")
    console.print(f"[yellow]Entry Point: {result['entry_point']}[/yellow]")
    console.print(f"[yellow]Dependencies: {', '.join([d['name'] for d in result['dependencies']])}[/yellow]")
    console.print(f"[yellow]Patterns: {', '.join(result['patterns'])}[/yellow]")
    console.print(f"\n[yellow]Top Files:[/yellow]")
    for fp, score in result['ranked_files'][:3]:
        console.print(f"  [cyan]{fp}[/cyan] — score: {score}")
    
    
if __name__ == "__main__":
    app()