import os

DEFAULT_MAX_TOKENS = 2000
CHARS_PER_TOKEN = 4
TOKENS_PER_FILE = 150  # estimated tokens per file snippet

METADATA_RATIO = 0.20
SNIPPET_RATIO = 0.80

MIN_LINES_PER_FILE = 50  # minimum lines per file snippet


def estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
        return len(enc.encode(text))
    except ImportError:
        return len(text) // CHARS_PER_TOKEN


def get_important_file_count(total_files: int, max_tokens: int = DEFAULT_MAX_TOKENS) -> int:
    """
    Return 25% of total files, but capped so each file gets at least MIN_LINES_PER_FILE lines.
    Ensures we never try to show more files than the budget supports.
    """
    raw_count = max(5, total_files // 4)
    # each file needs at minimum MIN_LINES_PER_FILE * ~40 chars
    min_chars_per_file = MIN_LINES_PER_FILE * 40
    snippet_budget = int(max_tokens * CHARS_PER_TOKEN * SNIPPET_RATIO)
    max_supported = max(1, snippet_budget // min_chars_per_file)
    return min(raw_count, max_supported)


def get_dynamic_budget(important_count: int, user_budget: int) -> int:
    """
    Calculate token budget dynamically based on important file count.
    User can override with --budget flag.
    If user set a custom budget, respect it.
    Otherwise calculate based on file count.
    """
    if user_budget != DEFAULT_MAX_TOKENS:
        return user_budget  # user explicitly set budget, respect it

    calculated = important_count * TOKENS_PER_FILE
    # clamp between 2000 and 12000
    return max(2000, min(calculated, 12000))


def build_metadata_block(analysis: dict, metadata_char_budget: int) -> str:
    lines = []
    lines.append("=== PROJECT SUMMARY ===")
    lines.append(f"Language: {analysis['language']}")
    secondary = analysis.get('secondary', {})
    if secondary:
        lines.append(f"Secondary Languages: {', '.join(secondary.keys())}")
    lines.append(f"Framework: {analysis['framework']}")
    lines.append(f"Architectural Pattern: {', '.join(analysis['patterns'])}")
    ep = analysis['entry_point']
    if ep and analysis.get('path'):
        try:
            ep = os.path.relpath(os.path.normpath(ep), os.path.normpath(analysis['path']))
        except ValueError:
            pass
    lines.append(f"Entry Point: {ep}")
    lines.append(f"Total Files: {len(analysis['files'])}")

    all_deps = analysis.get('dependencies', [])
    runtime_deps = [d['name'] for d in all_deps if not d.get('dev', False)]
    dev_deps = [d['name'] for d in all_deps if d.get('dev', False)]

    if runtime_deps:
        shown = runtime_deps[:10]
        dep_line = f"Dependencies: {', '.join(shown)}"
        if len(runtime_deps) > 10:
            dep_line += f" ... and {len(runtime_deps) - 10} more"
        lines.append(dep_line)

    if dev_deps:
        shown = dev_deps[:5]
        dev_line = f"Dev Dependencies: {', '.join(shown)}"
        if len(dev_deps) > 5:
            dev_line += f" ... and {len(dev_deps) - 5} more"
        lines.append(dev_line)

    return '\n'.join(lines)


MINIFIED_INDICATORS = ['compiled', 'dist', 'bundle', 'min.js', 'min.ts']

def build_file_snippet(filepath: str, char_budget: int) -> str:
    """
    Returns a clean snippet for a single file within char_budget.
    Converts char budget to lines, with a minimum floor of MIN_LINES_PER_FILE.
    Returns None if file can't be read or is minified/compiled.
    """
    # skip compiled/minified files
    fp_lower = filepath.replace("\\", "/").lower()
    if any(indicator in fp_lower for indicator in MINIFIED_INDICATORS):
        return None

    lines_allowed = max(MIN_LINES_PER_FILE, char_budget // 40)
    try:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()[:lines_allowed]
        # skip if first line is suspiciously long (minified)
        if lines and len(lines[0]) > 500:
            return None
        snippet = ''.join(lines).strip()
        return f"\n--- {filepath} ---\n{snippet}"
    except (OSError, UnicodeDecodeError):
        return None


def assemble_context(analysis: dict, max_tokens: int = DEFAULT_MAX_TOKENS, no_snippets: bool = False, top: int = None) -> str:
    total_files = len(analysis['files'])
    ranked = analysis.get('ranked_files', [])

    # --- DYNAMIC BUDGET ---
    # first pass: estimate budget with rough file count
    rough_count = max(5, total_files // 4)
    effective_tokens = get_dynamic_budget(rough_count, max_tokens)
    # second pass: refine important count based on actual budget
    important_count = get_important_file_count(total_files, effective_tokens)
    max_chars = effective_tokens * CHARS_PER_TOKEN
    metadata_budget = int(max_chars * METADATA_RATIO)
    snippet_budget = int(max_chars * SNIPPET_RATIO)

    sections = []

    # --- PRIORITY 1: Metadata ---
    metadata = build_metadata_block(analysis, metadata_budget)
    # hard enforce metadata budget — truncate if it overflows
    if len(metadata) > metadata_budget:
        metadata = metadata[:metadata_budget] + '\n... (metadata truncated)'
    sections.append(metadata)

    # --- PRIORITY 2: File snippets ---
    snippets_header = "\n\n=== KEY FILES ==="
    sections.append(snippets_header)
    remaining_snippet_budget = snippet_budget - len(snippets_header)

    if not ranked:
        sections.append("\n[No files available to display]")

    # iterate top 25% of ranked files, add as many as budget allows
    cap = top if top is not None else 25
    files_to_show = ranked[:min(important_count, cap)]
    per_file_budget = remaining_snippet_budget // max(len(files_to_show), 1)

    file_descriptions = analysis.get('file_descriptions', {})
    # get base path for relative path display
    base_path = analysis.get('path', '')

    # if no_snippets, just show filename + description
    if no_snippets:
        for fp, _ in files_to_show:
            try:
                display_fp = os.path.relpath(fp, base_path) if base_path else fp
            except ValueError:
                display_fp = fp
            description = file_descriptions.get(fp, '')
            if description:
                sections.append(f"\n> {description}\n--- {display_fp} ---")
            else:
                sections.append(f"\n--- {display_fp} ---")
        sections.append(f"\n=== Token estimate: {estimate_tokens(metadata)} / {max_tokens} ===")
        return '\n'.join(sections)

    for fp, _ in files_to_show:
        snippet = build_file_snippet(fp, per_file_budget)
        if snippet is None:
            continue
        # add description above snippet
        description = file_descriptions.get(fp, '')
        if description:
            desc_line = f"\n> {description}"
            snippet = desc_line + snippet
        # make path relative for display
        display_fp = fp
        if base_path:
            try:
                display_fp = os.path.relpath(fp, base_path)
            except ValueError:
                display_fp = fp
        snippet = snippet.replace(fp, display_fp)
        if len(snippet) > remaining_snippet_budget:
            sections.append("\n[Token budget reached — use Deep Dive for remaining files]")
            break
        sections.append(snippet)
        remaining_snippet_budget -= len(snippet)

    # --- ASSEMBLE ---
    full_output = '\n'.join(sections)
    token_count = estimate_tokens(full_output)
    full_output += f"\n\n=== Token estimate: {token_count} / {effective_tokens} ==="

    return full_output