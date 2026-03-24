import os

# heuristic descriptions based on folder and filename patterns
FOLDER_HINTS = {
    'server': 'Server-side',
    'client': 'Client-side',
    'lib': 'Library/utility',
    'shared': 'Shared',
    'utils': 'Utility',
    'helpers': 'Helper',
    'components': 'UI component',
    'pages': 'Page',
    'api': 'API',
    'routes': 'Routing',
    'models': 'Data model',
    'middleware': 'Middleware',
    'config': 'Configuration',
    'hooks': 'React hook',
    'context': 'React context',
    'store': 'State management',
    'services': 'Service layer',
    'controllers': 'Controller',
    'core': 'Core',
    'auth': 'Authentication',
    'db': 'Database',
    'database': 'Database',
}

FILE_HINTS = {
    'index': 'Entry/barrel file',
    'main': 'Main entry point',
    'app': 'Application root',
    'server': 'Server setup',
    'client': 'Client setup',
    'router': 'Routing logic',
    'config': 'Configuration',
    'utils': 'Utility functions',
    'helpers': 'Helper functions',
    'types': 'Type definitions',
    'constants': 'Constants',
    'middleware': 'Middleware',
    'auth': 'Authentication logic',
    'db': 'Database logic',
    'cli': 'CLI interface',
    'analyzer': 'Analysis logic',
    'scanner': 'File scanning',
    'ranker': 'File ranking',
    'detector': 'Detection logic',
    'assembler': 'Output assembly',
    'validator': 'Validation logic',
    'describer': 'Description generation',
    'cache': 'Caching logic',
    'parser': 'Parsing logic',
    'dispatcher': 'Event dispatching',
    'handler': 'Request/event handler',
    'manager': 'Resource management',
    'store': 'State store',
    'context': 'Context provider',
    'hook': 'React hook',
    'reducer': 'State reducer',
    'action': 'State action',
    'selector': 'State selector',
    'test': 'Test file',
    'spec': 'Test specification',
    'mock': 'Mock/stub',
}


def get_heuristic_description(filepath: str) -> str:
    """Generate a simple heuristic description from filepath."""
    normalized = filepath.replace('\\', '/').lower()
    parts = normalized.split('/')
    filename = os.path.splitext(parts[-1])[0].lower()

    # check folder hints
    folder_desc = None
    for part in reversed(parts[:-1]):
        if part in FOLDER_HINTS:
            folder_desc = FOLDER_HINTS[part]
            break

    # check file hints
    file_desc = None
    for key, desc in FILE_HINTS.items():
        if key in filename:
            file_desc = desc
            break

    if folder_desc and file_desc:
        return f"{folder_desc} — {file_desc.lower()}"
    elif folder_desc:
        return f"{folder_desc} logic"
    elif file_desc:
        return file_desc
    else:
        return "Source file"


def generate_descriptions(ranked_files: list, llm_provider: str = None, api_key: str = None) -> dict:
    """
    Generate descriptions for ranked files.
    Uses LLM if provider and key are available, otherwise falls back to heuristics.
    Returns dict of {filepath: description}
    """
    descriptions = {}

    if llm_provider and api_key:
        try:
            descriptions = _generate_llm_descriptions(ranked_files, llm_provider, api_key)
        except Exception as e:
            err = str(e).lower()
            if '429' in err or 'rate limit' in err or 'quota' in err:
                print("[Warning] LLM rate limit hit. Using heuristic descriptions.")
            elif 'network' in err or 'connection' in err or 'timeout' in err or 'unreachable' in err:
                print("[Warning] No internet connection. Using heuristic descriptions.")
            elif 'invalid api key' in err or 'unauthorized' in err or '401' in err:
                print("[Warning] Invalid API key. Using heuristic descriptions.")
            else:
                print(f"[Warning] LLM descriptions failed: {e}. Using heuristic descriptions.")
            descriptions = {}

    # fill in any missing with heuristics (also used as full fallback)
    for fp, _ in ranked_files:
        if fp not in descriptions:
            descriptions[fp] = get_heuristic_description(fp)

    return descriptions


def _build_description_prompt(ranked_files: list) -> str:
    prompt = (
        "You are a code documentation assistant.\n"
        "For each file below, write a single sentence (max 15 words) describing what the file does.\n"
        "Focus on the file's role in the codebase, not its implementation details.\n"
        "Return ONLY a JSON object mapping filepath to description.\n"
        "Example: {\"src/server/base-server.ts\": \"Core HTTP server abstraction handling request/response lifecycle.\"}\n\n"
        "Files to describe:\n"
    )
    for fp, _ in ranked_files:
        prompt += f"- {fp}\n"
        try:
            with open(fp, encoding='utf-8') as f:
                first_lines = ''.join(f.readlines()[:10])
            prompt += f"  First lines:\n  {first_lines[:300]}\n\n"
        except (OSError, UnicodeDecodeError):
            prompt += "  [Could not read file]\n\n"
    return prompt


def _parse_description_response(response_text: str, ranked_files: list) -> dict:
    """Parse LLM response into descriptions dict. Falls back to empty on failure."""
    import json
    try:
        clean = response_text.strip().replace('```json', '').replace('```', '').strip()
        raw = json.loads(clean)
        # normalize keys to match our file paths
        result = {}
        fp_map = {os.path.basename(fp): fp for fp, _ in ranked_files}
        for key, desc in raw.items():
            # try exact match first
            if any(fp == key for fp, _ in ranked_files):
                result[key] = desc
            # try basename match
            elif os.path.basename(key) in fp_map:
                result[fp_map[os.path.basename(key)]] = desc
        return result
    except Exception:
        return {}


def _generate_llm_descriptions(ranked_files: list, provider: str, api_key: str) -> dict:
    """Call LLM to generate file descriptions."""
    prompt = _build_description_prompt(ranked_files)
    history = [{"role": "user", "content": prompt}]
    response = None

    if provider == 'gemini':
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        resp = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        response = resp.text

    elif provider == 'openai':
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        response = resp.choices[0].message.content

    elif provider == 'anthropic':
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=1024,
            messages=[{'role': 'user', 'content': prompt}]
        )
        response = resp.content[0].text

    if response is None:
        return {}

    return _parse_description_response(response, ranked_files)