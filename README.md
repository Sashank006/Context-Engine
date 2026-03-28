# ContextPack 🗜️

> A static analysis engine that maps any codebase into a ranked, token-budgeted context — offline, zero LLM cost, under 10 seconds.

---

## How It Works

```
scan (two-pass) → detect language/framework → parse dependencies
               → detect entry points → rank files (import graph + heuristics)
               → detect patterns → assemble context (token-budgeted)
```

**Pass 1** — walks the full directory tree collecting only folder names and file counts. Prunes ignored subtrees instantly with zero file reads.

**Pass 2** — walks only approved folders. Scores every code file using a multi-signal ranking function: filename heuristics, content signals, import graph traversal across 9 languages, and depth penalties. Assembles output within a strict token budget using a 20/80 metadata/snippet split.

LLM is an optional enhancement layer — the static engine is the core.

---

## Why It Exists

Pasting a codebase into an LLM doesn't work past ~20 files — you hit the token limit before you've explained anything. Grep tools require you to already know what to search for. Manual skimming doesn't scale and misses import relationships.

ContextPack solves the **cold start problem**: before you know what questions to ask, it tells you where to look.

---

## Demo

![Demo](demo.gif)

Run on the [Next.js](https://github.com/vercel/next.js) repository (3039 files):

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

## Engine Capabilities

| Component | What it does |
|---|---|
| **Two-pass scanner** | Prunes ignored folders before reading any files — fast on large repos |
| **Import graph** | Traces import/require relationships across 9 languages to weight file importance |
| **File ranker** | Multi-signal scoring: filename heuristics + content signals + import depth + path depth |
| **Language detector** | Primary + secondary language detection across 40+ language configs |
| **Framework detector** | Runtime deps only, priority-ordered, 10+ frameworks |
| **Pattern detector** | Identifies REST API, MVC, CLI Tool, Microservice patterns via keyword signals |
| **Token assembler** | Adaptive 20/80 metadata/snippet split — never truncates mid-file |
| **LLM layer** | Optional re-ranking + descriptions via Gemini/OpenAI/Anthropic — bring your own key |
| **Deep Dive** | RAG conversation loop with query-aware smart snippets and session compression |

---

## Known Limitations

- File ranking is heuristic-based — self-referential files may score incorrectly without `--llm`
- Pattern detection uses keyword matching, not structural analysis
- Token estimation uses `tiktoken` (cl100k_base) — accurate for GPT models, approximate for others
- Monorepos with multiple entry points return only the first detected entry point
- Projects embedding a scripting language in C source may show wrong primary language — use `.contextignore` to exclude non-core folders

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