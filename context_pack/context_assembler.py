import os

DEFAULT_MAX_TOKENS = 2000
CHARS_PER_TOKEN = 4

METADATA_RATIO = 0.20
SNIPPET_RATIO = 0.80


def estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
        return len(enc.encode(text))
    except ImportError:
        # fallback to char/4 approximation if tiktoken not installed
        return len(text) // CHARS_PER_TOKEN


def get_snippet_config(file_count: int) -> tuple[int, int]:
    """
    Adaptive snippet config based on codebase size.
    Returns (num_files, lines_per_file)
    """
    if file_count < 20:
        return 3, 50
    elif file_count < 50:
        return 5, 30
    else:
        return 7, 20


def build_metadata_block(analysis: dict, metadata_char_budget: int) -> str:
    lines = []
    lines.append("=== PROJECT SUMMARY ===")
    lines.append(f"Language: {analysis['language']}")
    if analysis.get('mixed'):
        lines.append("Mixed codebase: Yes")
    lines.append(f"Framework: {analysis['framework']}")
    lines.append(f"Architectural Pattern: {', '.join(analysis['patterns'])}")
    lines.append(f"Entry Point: {analysis['entry_point']}")
    lines.append(f"Total Files: {len(analysis['files'])}")

    deps = [d['name'] for d in analysis.get('dependencies', [])]
    if deps:
        dep_line = f"Dependencies: {', '.join(deps)}"
        # if deps push us over metadata budget, truncate the list
        base = '\n'.join(lines)
        if len(base) + len(dep_line) > metadata_char_budget:
            dep_line = f"Dependencies: {', '.join(deps[:10])} ... (truncated)"
        lines.append(dep_line)

    return '\n'.join(lines)


def build_file_snippet(filepath: str, max_lines: int) -> str:
    """
    Returns a clean snippet for a single file.
    Returns None if file can't be read.
    """
    try:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
        snippet = ''.join(lines).strip()
        return f"\n--- {filepath} ---\n{snippet}"
    except (OSError, UnicodeDecodeError):
        return None


def assemble_context(analysis: dict, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    max_chars = max_tokens * CHARS_PER_TOKEN
    metadata_budget = int(max_chars * METADATA_RATIO)
    snippet_budget = int(max_chars * SNIPPET_RATIO)

    sections = []

    # --- PRIORITY 1: Metadata (capped at 20% of budget) ---
    metadata = build_metadata_block(analysis, metadata_budget)
    sections.append(metadata)

    # --- PRIORITY 2: File snippets (get 80% of budget) ---
    file_count = len(analysis['files'])
    num_files, lines_per_file = get_snippet_config(file_count)
    ranked = analysis.get('ranked_files', [])

    snippets_header = "\n\n=== KEY FILES ==="
    sections.append(snippets_header)
    remaining_snippet_budget = snippet_budget - len(snippets_header)


    if not ranked:
        sections.append("\n[No files available to display]")
    for fp, _ in ranked[:num_files]:
        snippet = build_file_snippet(fp, lines_per_file)
        if snippet is None:
            continue
        # Only include if the full snippet fits — no half files
        if len(snippet) > remaining_snippet_budget:
            sections.append("\n[Token budget reached — use Deep Dive for remaining files]")
            break
        sections.append(snippet)
        remaining_snippet_budget -= len(snippet)

    # --- ASSEMBLE ---
    full_output = '\n'.join(sections)
    token_count = estimate_tokens(full_output)
    full_output += f"\n\n=== Token estimate: {token_count} / {max_tokens} ==="

    return full_output