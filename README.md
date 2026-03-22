# ContextPack 🗜️
> LLM-Ready Codebase Context Engine

ContextPack scans any codebase and generates a structured, token-efficient summary you can drop straight into any LLM — so you spend less time explaining your code and more time building.

---

## Demo

Run ContextPack on the [Gemini CLI](https://github.com/google-gemini/gemini-cli) repository (1600+ files, TypeScript codebase):

```
$ context-pack --url https://github.com/google-gemini/gemini-cli

Cloning https://github.com/google-gemini/gemini-cli...
Cloned successfully.
Scanning: /tmp/contextpack_xyz
Found 853 files

=== PROJECT SUMMARY ===
Language: TypeScript
Secondary Languages: Rust
Framework: Ink
Architectural Pattern: Microservice, CLI Tool, MVC
Entry Point: packages/cli/index.ts
Total Files: 853
Dependencies: ink, latest-version, node-fetch-native, simple-git
Dev Dependencies: eslint, vitest, typescript-eslint, esbuild ...

=== KEY FILES ===

> Entry/barrel file
--- packages/cli/index.ts ---
...

> Core — cli interface
--- packages/core/src/agents/cli-help-agent.ts ---
...

=== Token estimate: 7297 / 12000 ===
```

---

## Features

- **Two-pass scanner** — fast directory walk that prunes ignored folders before reading any files, then ranks survivors
- **Static analysis engine** — detects language, framework, architectural patterns, entry points, and dependencies with zero LLM cost
- **Smart file ranking** — multi-signal scoring combining filename heuristics, content signals, import graph analysis across 9 languages, and depth penalties
- **File descriptions** — every key file gets a one-line description (heuristic by default, LLM-powered with `--llm`)
- **Token-efficient output** — adaptive 20/80 metadata/snippet split, priority-first assembly, never truncates mid-file, capped at 25 key files
- **Runtime vs dev dependencies** — separates runtime dependencies from dev/build tools in the summary
- **LLM validation** — optional re-ranking of files using your own API key (Gemini, OpenAI, Anthropic)
- **Deep Dive mode** — RAG-powered conversation loop with query-aware smart snippets, ask questions about any codebase interactively
- **Session memory** — automatically compresses conversation history to stay within token limits
- **GitHub URL support** — clone and scan any public repo in one command with `--url`
- **Cache layer** — results cached by file path + mtime, instant re-runs on unchanged codebases
- **Diff-aware context** — show unstaged changes or diff against any branch with `--diff`
- **Output to file** — save context as `.md` or `.txt` for sharing or reuse
- **`.contextignore` support** — exclude folders and file patterns per-project, just like `.gitignore`
- **40+ languages supported** — Python, C, C++, JavaScript, TypeScript, Rust, Go, Java, Kotlin, Lua, and more

---

## Requirements

- Python 3.10+
- Windows, macOS, or Linux

---

## Installation

### From PyPI (recommended)
```bash
pip install context-pack
```

### From source
```bash
git clone https://github.com/Sashank006/Context-Engine.git
cd Context-Engine

python -m venv venv
source venv/bin/activate        # Mac/Linux
source venv/Scripts/activate    # Windows

pip install -e .
```

---

## Usage

### Basic scan (current directory)
```bash
context-pack
```

### Scan a specific path
```bash
context-pack --path /path/to/repo
```

### Clone and scan a GitHub repo
```bash
context-pack --url https://github.com/org/repo
```

### Save output to file
```bash
context-pack --output context.md
context-pack --output context.txt
```
> `.md` output renders with tables and syntax-highlighted code blocks. View in VS Code (`Ctrl+Shift+V`), GitHub, or any markdown renderer.

### Set custom token budget
```bash
context-pack --budget 4000
```

### LLM-powered file ranking + descriptions
```bash
export GEMINI_API_KEY=your_key_here
context-pack --llm gemini
```
> Also supports `--llm openai` and `--llm anthropic`

### Deep Dive mode — ask questions about the codebase
```bash
context-pack --llm gemini --deep-dive
```

### Diff-aware context
```bash
context-pack --diff                    # show unstaged changes
context-pack --diff-target HEAD        # diff since last commit
context-pack --diff-target main        # diff against branch
```

### Cache management
```bash
context-pack --clear-cache             # clear cache for current path
```

### Ignore folders with `.contextignore`
Create a `.contextignore` file in the project root:
```
# ignore specific folders
runtime
contrib

# ignore file patterns
*.generated.ts
*.pb.go
```

---

## Supported Languages

Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Lua, Shell, VimScript, Scala, Haskell, Elixir, Dart, R, HTML, CSS and more.

---

## How It Works

ContextPack runs a strict separation-of-concerns pipeline:

```
scan (two-pass) → detect language → detect framework → parse dependencies
                → detect entry point → rank files → detect patterns
                → generate descriptions → assemble context (token-budgeted)
```

**Pass 1** — walks the full directory tree collecting only folder names and file counts, pruning ignored subtrees instantly with no file reads.

**Pass 2** — walks only approved folders, collecting code files while skipping test files, config files, minified files, and generated code.

LLM is an optional enhancement layer — the static engine works standalone.

---

## Known Limitations

- File ranking is heuristic-based — self-referential files may score incorrectly without LLM validation
- Pattern detection uses keyword matching, not structural analysis
- Token estimation uses `tiktoken` (cl100k_base encoding) — accurate for GPT models, approximate for others
- Monorepos with multiple entry points return only the first detected entry point — full monorepo support planned
- Projects deeply embedding a scripting language in C source (e.g. Neovim embeds Lua in `src/`) may show wrong primary language — use `.contextignore` to exclude non-core folders