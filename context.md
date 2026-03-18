# ContextPack — Project Summary

## Metadata

| Field | Value |
|-------|-------|
| Language | Python |
| Framework | Typer |
| Architectural Pattern | CLI Tool |
| Entry Point | .\context_pack\cli.py |
| Total Files | 18 |
| Dependencies | typer, rich, google-genai, openai, anthropic, tiktoken |

## Key Files

### `.\context_pack\file_ranker.py`
```python
import os
import re

IMPORTANCE_SCORES = {
    'main': 30,
    'app': 25,
    'core': 25,
    'api': 20,
    'server': 20,
    'index': 20,
    'cli': 15,
    'config': 15,
    'settings': 15,
    'routes': 15,
    'models': 15,
    'database': 15,
    'db': 15,
    'auth': 10,
    'utils': 5,
    'helpers': 5,
    'constants': 5,
    'test': -20,
    'tests': -20,
    'spec': -15,
    'mock': -15,
    'fixture': -10,
    'migrations': -10,
    'seed': -10,
}

CONTENT_SIGNALS = {
    'route': 8,
    'router': 8,
    'app.get': 8,
    'app.post': 8,
    'model': 6,
    'schema': 6,
    'if __name__': 10,
    'app.run': 10,
    'listen': 7,
}

UTILITY_KEYWORDS = ['utils', 'helpers', 'constants', 'colors', 'types', 'enums']
TEST_KEYWORDS = ['test', 'tests', 'spec', 'mock']


def build_import_map(file_paths):
    import_counts = {fp: 0 for fp in file_paths}
    test_only = {fp: True for fp in file_paths}

```

### `.\context_pack\cli.py`
```python
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

```

### `.\context_pack\__main__.py`
```python
from context_pack.cli import app

if __name__ == "__main__":
    app()

```

### `.\context_pack\entry_point_detector.py`
```python
import os

CONTENT_SIGNALS = {
    'Python': ['if __name__ == "__main__"'],
    'JavaScript': ['app.listen(', 'server.listen(', 'createServer('],
    'TypeScript': ['app.listen(', 'server.listen('],
    'Go': ['func main()'],
    'Ruby': ['Sinatra::Application', 'Rails.application'],
    'Java': ['public static void main'],
    'Kotlin': ['fun main('],
    'Rust': ['fn main()'],
    'Swift': ['@main', 'UIApplicationMain'],
    'PHP': ['<?php'],
    'C#': ['static void Main(', 'static async Task Main('],
    'C++': ['int main('],
    'C': ['int main(', 'void main('],
    'Lua': ['require(', 'dofile('],
    'Shell': ['#!/bin/bash', '#!/bin/sh'],
}

ENTRY_POINT_FILENAMES = {
    'Python': ['main.py', 'app.py', 'run.py', 'manage.py', 'server.py', 'wsgi.py', 'asgi.py'],
    'JavaScript': ['index.js', 'app.js', 'server.js', 'main.js'],
    'TypeScript': ['index.ts', 'app.ts', 'server.ts', 'main.ts'],
    'Go': ['main.go'],
    'Ruby': ['app.rb', 'main.rb', 'config.ru', 'Rakefile'],
    'Java': ['Main.java', 'App.java', 'Application.java'],
    'Kotlin': ['Main.kt', 'App.kt', 'Application.kt'],
    'Swift': ['main.swift', 'App.swift'],
    'Rust': ['main.rs'],
    'PHP': ['index.php', 'app.php', 'main.php'],
    'C#': ['Program.cs', 'Main.cs', 'Startup.cs'],
    'C++': ['main.cpp', 'app.cpp'],
    'C': ['main.c', 'app.c'],
    'Scala': ['Main.scala', 'App.scala'],
    'Elixir': ['mix.exs', 'application.ex'],
    'Haskell': ['Main.hs', 'app.hs'],
    'Dart': ['main.dart'],
    'R': ['main.R', 'app.R', 'run.R'],
    'Lua': ['main.lua', 'app.lua'],
    'Shell': ['main.sh', 'run.sh', 'start.sh'],
}

def detect_entry_point(file_paths, primary_language):
    signals = CONTENT_SIGNALS.get(primary_language, [])
    # skip header files — they declare but never define entry points
    skip_extensions = {'.h', '.hpp', '.hh'}
    for fp in file_paths:
        if os.path.splitext(fp)[1] in skip_extensions:
            continue

```


> [Token budget reached — use Deep Dive for remaining files]

---
_Token estimate: 1410 / 2000_