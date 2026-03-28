# ContextPack 🗜️
> LLM-Ready Codebase Context Engine

ContextPack scans any codebase and generates a structured, token-efficient summary you can drop straight into any LLM — so you spend less time explaining your code and more time building.

---

## Demo
![Demo](demo.gif)
Run ContextPack on the [Next.js](https://github.com/vercel/next.js) repository:

```
$ context-pack --path ~/next.js --no-snippets --top 5

=== PROJECT SUMMARY ===
Language: TypeScript
Secondary Languages: JavaScript
Framework: Next.js
Architectural Pattern: REST API, MVC
Entry Point: packages/next/src/server/next.ts
Total Files: 3039
Dependencies: react, react-dom, styled-jsx ... and 4 more
Dev Dependencies: typescript, eslint, jest ... and 189 more

=== KEY FILES ===

> Core — entry/barrel file
--- packages/next/src/client/index.tsx ---

> Server setup
--- packages/next/src/server/base-server.ts ---

> Core — application root
--- packages/next/src/server/app-render/app-render.tsx ---

> Configuration — configuration
--- packages/next/src/server/config.ts ---

> Client-side — main entry point
--- packages/next/src/client/app-index.tsx ---

=== Token estimate: 1823 / 12000 ===
```

---

## Features

- **Two-pass scanner** — fast directory walk that prunes ignored folders before reading any files, then ranks survivors
- **Static analysis engine** — detects language, framework, architectural patterns, entry points, and dependencies with zero LLM cost
- **Smart file ranking** — multi-signal scoring combining filename heuristics, content signals, import graph analysis across 9 languages, and depth penalties
- **File descriptions** — every key file gets a one-line description (heuristic by default, LLM-powered with `--llm`)
- **Token-efficient output** — adaptive 20/80 metadata/snippet split, priority-first assembly, never truncates mid-file
- **Runtime vs dev dependencies** — separates runtime dependencies from dev/build tools, capped at 10/5 for clean display
- **Relative paths** — all file paths shown relative to scanned root, no system paths exposed
- **LLM validation** — optional re-ranking of files using your own API key (Gemini, OpenAI, Anthropic)
- **Deep Dive mode** — RAG-powered conversation loop with query-aware smart snippets, straight to questions, no noise
- **Session memory** — automatically compresses conversation history to stay within token limits
- **GitHub URL support** — clone and scan any public repo in one command with `--url`
- **Cache layer** — results cached by file path + mtime, instant re-runs on unchanged codebases
- **Diff-aware context** — show unstaged changes or diff against any branch with `--diff`
- **Output to file** — save context as `.md` or `.txt` silently, no terminal spam
- **`.contextignore` support** — exclude folders and file patterns per-project, just like `.gitignore`
- **40+ languages supported** — Python, C, C++, JavaScript, TypeScript, Rust, Go, Java, Kotlin, Lua, and more

---

## Requirements

- Python 3.10+
- Windows, macOS, or Linux

---

## Installation

```bash
pip install git+https://github.com/Sashank006/Context-Engine.git
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

### Clean summary — no code snippets
```bash
context-pack --no-snippets
```

### Show only top N key files
```bash
context-pack --top 5
```

### Combine for a tight one-screen summary
```bash
context-pack --no-snippets --top 5
```

### Save output to file (silent — no terminal spam)
```bash
context-pack --output context.md
context-pack --output context.txt
```

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
- Projects deeply embedding a scripting language in C source may show wrong primary language — use `.contextignore` to exclude non-core folders