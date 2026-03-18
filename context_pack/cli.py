import typer
import os
import tempfile
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from context_pack.analyzer import analyze
from context_pack.llm_validator import get_api_key
from context_pack.deep_dive import start_deep_dive
from typing import Optional
from context_pack.cache import get_cached, save_cache, clear_cache
from context_pack.diff_context import get_diff, format_diff_output

app = typer.Typer()
console = Console()


def clone_repo(url: str) -> str | None:
    """Clone a GitHub repo to a temp directory. Returns the temp path or None on failure."""
    tmp_dir = tempfile.mkdtemp(prefix='contextpack_')
    console.print(f"[blue]Cloning {url}...[/blue]")
    try:
        subprocess.run(
            ['git', 'clone', '--depth=1', url, tmp_dir],
            check=True,
            capture_output=True
        )
        console.print(f"[green]Cloned successfully.[/green]")
        return tmp_dir
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to clone repo: {e.stderr.decode().strip()}[/red]")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None


def format_as_markdown(context: str) -> str:
    """Convert raw context output into clean markdown with tables and code blocks."""
    lines = context.split('\n')
    md = []
    i = 0

    md.append("# ContextPack — Project Summary\n")

    while i < len(lines):
        line = lines[i]

        # metadata section
        if line.strip() == '=== PROJECT SUMMARY ===':
            md.append("## Metadata\n")
            md.append("| Field | Value |")
            md.append("|-------|-------|")
            i += 1
            while i < len(lines) and not lines[i].startswith('==='):
                meta_line = lines[i].strip()
                if ': ' in meta_line:
                    key, val = meta_line.split(': ', 1)
                    md.append(f"| {key} | {val} |")
                i += 1
            md.append("")

        # key files section
        elif line.strip() == '=== KEY FILES ===':
            md.append("## Key Files\n")
            i += 1

        # file header
        elif line.startswith('--- ') and line.endswith(' ---'):
            filepath = line[4:-4].strip()
            ext = os.path.splitext(filepath)[1].lstrip('.')
            lang_map = {
                'py': 'python', 'js': 'javascript', 'ts': 'typescript',
                'c': 'c', 'cpp': 'cpp', 'h': 'c', 'java': 'java',
                'go': 'go', 'rs': 'rust', 'rb': 'ruby', 'lua': 'lua',
                'sh': 'bash', 'cs': 'csharp', 'kt': 'kotlin',
            }
            lang = lang_map.get(ext, '')
            md.append(f"### `{filepath}`")
            md.append(f"```{lang}")
            i += 1
            # collect code lines until next file or section
            while i < len(lines):
                next_line = lines[i]
                if (next_line.startswith('--- ') and next_line.endswith(' ---')) or next_line.startswith('===') or 'Token budget reached' in next_line:
                    break
                md.append(next_line)
                i += 1
            md.append("```\n")

        # token estimate line
        elif line.startswith('=== Token estimate'):
            md.append(f"\n---\n_{line.strip('=').strip()}_")
            i += 1

        # token budget message
        elif 'Token budget reached' in line:
            md.append(f"\n> {line.strip()}")
            i += 1

        else:
            i += 1

    return '\n'.join(md)


def save_output(context: str, output_path: str):
    """Save context to .md or .txt file."""
    ext = os.path.splitext(output_path)[1].lower()

    if ext == '.md':
        content = format_as_markdown(context)
    else:
        content = context

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[green]Context saved to: {output_path}[/green]")
    except OSError as e:
        console.print(f"[red]Could not save file: {e}[/red]")


@app.command()
def scan(
    path: str = ".",
    url: Optional[str] = typer.Option(None, "--url", "-u", help="GitHub URL to clone and analyze"),
    budget: int = typer.Option(2000, "--budget", "-b", help="Max token budget for context output (default: 2000)"),
    llm: Optional[str] = typer.Option(None, "--llm", help="LLM provider: gemini, openai, anthropic"),
    deep_dive: bool = typer.Option(False, "--deep-dive", "-d", help="Start interactive Deep Dive mode after analysis"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Save context to file e.g. context.md or context.txt"),
    clear_cache_flag: bool = typer.Option(False, "--clear-cache", help="Clear cached result for this path and re-analyze"),
    show_diff: bool = typer.Option(False, "--diff", help="Show unstaged changes"),
    diff_target: Optional[str] = typer.Option(None, "--diff-target", help="Diff against a commit or branch e.g. HEAD or main")
):
    """Scan a directory or GitHub URL and generate LLM-ready context."""

    tmp_dir = None

    # --- GITHUB URL MODE ---
    if url:
        tmp_dir = clone_repo(url)
        if tmp_dir is None:
            return
        path = tmp_dir

    # --- CACHE CHECK ---
    if clear_cache_flag:
        clear_cache(path)
        console.print(f"[yellow]Cache cleared for: {path}[/yellow]")
        return

    cached = get_cached(path)
    if cached:
        console.print(f"[green]Using cached result (repo unchanged). Use --clear-cache to force re-analysis.[/green]")
        console.print(cached)
        if output:
            save_output(cached, output)
        return

    # --- DIFF MODE ---
    if show_diff or diff_target:
        console.print(f"[blue]Running diff on: {path}[/blue]")
        result = analyze(path, max_tokens=budget)
        diff_result = get_diff(path, target=diff_target if diff_target else None)
        if diff_result is None:
            console.print("[red]Could not run git diff. Is this a git repository?[/red]")
            return
        output_text = format_diff_output(diff_result, result['ranked_files'])
        console.print(output_text)
        if output:
            save_output(output_text, output)
        return

    console.print(f"[blue]Scanning: {path}[/blue]")
    if budget != 2000:
        console.print(f"[yellow]Token budget set to: {budget}[/yellow]")
    if llm and not deep_dive:
        console.print(f"[yellow]LLM validation enabled: {llm}[/yellow]")

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

    # --- SAVE TO CACHE ---
    save_cache(path, result['context'])

    # --- SAVE OUTPUT ---
    if output:
        save_output(result['context'], output)

    # --- DEEP DIVE MODE ---
    if deep_dive:
        if not llm:
            console.print("[red]Deep Dive requires --llm. Example: --llm gemini[/red]")
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            return
        api_key = get_api_key(llm)
        if not api_key:
            console.print(f"[red]No API key found for {llm}. Set {llm.upper()}_API_KEY environment variable.[/red]")
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            return
        start_deep_dive(result["context"], llm, api_key, result["ranked_files"])

    # --- CLEANUP TEMP DIR ---
    if tmp_dir:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        console.print(f"[blue]Cleaned up temp directory.[/blue]")

if __name__ == "__main__":
    app()