import os

MAX_TOKENS = 2000
# rough approximation: 1 token ~ 4 characters
CHARS_PER_TOKEN = 4
MAX_CHARS = MAX_TOKENS * CHARS_PER_TOKEN

LINES_PER_FILE = 50


def estimate_tokens(text):
    return len(text) // CHARS_PER_TOKEN


def assemble_context(analysis_result):
    sections = []

    # --- METADATA BLOCK ---
    meta = []
    meta.append(f"Language: {analysis_result['language']}")
    if analysis_result.get('mixed'):
        meta.append(f"Mixed codebase: Yes")
    meta.append(f"Framework: {analysis_result['framework']}")
    meta.append(f"Entry Point: {analysis_result['entry_point']}")
    meta.append(f"Patterns: {', '.join(analysis_result['patterns'])}")

    deps = [d['name'] for d in analysis_result['dependencies']]
    if deps:
        meta.append(f"Dependencies: {', '.join(deps)}")

    meta.append(f"Total Files: {len(analysis_result['files'])}")

    sections.append("=== PROJECT SUMMARY ===")
    sections.append('\n'.join(meta))

    # --- TOP RANKED FILES ---
    sections.append("\n=== KEY FILES ===")
    ranked = analysis_result.get('ranked_files', [])

    for fp, score in ranked[:5]:
        sections.append(f"\n--- {fp} (score: {score}) ---")
        try:
            with open(fp, encoding='utf-8') as f:
                lines = f.readlines()[:LINES_PER_FILE]
            sections.append(''.join(lines))
        except (OSError, UnicodeDecodeError):
            sections.append("[Could not read file]")

    # --- ASSEMBLE ---
    full_output = '\n'.join(sections)

    # --- TRUNCATE FROM BOTTOM IF OVER LIMIT ---
    if len(full_output) > MAX_CHARS:
        full_output = full_output[:MAX_CHARS]
        full_output += "\n\n[...truncated to fit token limit]"

    token_count = estimate_tokens(full_output)
    full_output += f"\n\n=== Token estimate: {token_count} / {MAX_TOKENS} ==="

    return full_output