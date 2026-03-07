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