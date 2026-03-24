import os

SUPPORTED_PROVIDERS = ['gemini', 'openai', 'anthropic']

ENV_KEY_MAP = {
    'gemini': 'GEMINI_API_KEY',
    'openai': 'OPENAI_API_KEY',
    'anthropic': 'ANTHROPIC_API_KEY',
}


def get_api_key(provider: str) -> str | None:
    """Get API key from environment for the given provider."""
    env_var = ENV_KEY_MAP.get(provider)
    if not env_var:
        return None
    return os.environ.get(env_var)


def validate_ranking(ranked_files: list, provider: str, api_key: str) -> list:
    """
    Uses LLM to validate file rankings.
    Takes top ranked files, asks LLM if they are genuinely important.
    Returns re-ordered/filtered list.
    Falls back to original ranking on any error.
    """
    try:
        if provider == 'gemini':
            return _validate_with_gemini(ranked_files, api_key)
        elif provider == 'openai':
            return _validate_with_openai(ranked_files, api_key)
        elif provider == 'anthropic':
            return _validate_with_anthropic(ranked_files, api_key)
        else:
            print(f"[Warning] Unsupported provider: {provider}. Skipping LLM validation.")
            return ranked_files
    except Exception as e:
        err = str(e).lower()
        if '429' in err or 'rate limit' in err or 'quota' in err:
            print("[Warning] LLM rate limit hit. Falling back to static ranking.")
        elif 'network' in err or 'connection' in err or 'timeout' in err or 'unreachable' in err:
            print("[Warning] No internet connection or API unreachable. Falling back to static ranking.")
        elif 'invalid api key' in err or 'unauthorized' in err or '401' in err:
            print("[Warning] Invalid API key. Falling back to static ranking.")
        else:
            print(f"[Warning] LLM validation failed: {e}. Falling back to static ranking.")
        return ranked_files


MAX_PROMPT_CHARS = 12000  # cap total prompt size to avoid massive API calls


def _build_prompt(ranked_files: list) -> str:
    """Build the validation prompt from ranked files. Capped at MAX_PROMPT_CHARS."""
    prompt = (
        "You are a code analysis assistant. Below are files from a codebase ranked by a static analysis tool.\n"
        "For each file, review the snippet and decide if it is genuinely important to understanding the codebase.\n"
        "A file is genuinely important if it defines core logic, entry points, routing, models, or configuration.\n"
        "A file is NOT important if it only contains keyword-rich strings, constants, or utility mappings.\n\n"
        "Return a JSON array of file paths in order of true importance. Drop any files that are not genuinely important.\n"
        "Return ONLY the JSON array, no explanation.\n\n"
        "Files to evaluate:\n\n"
    )

    for fp, score in ranked_files:
        block = f"--- {fp} ---\n"
        try:
            with open(fp, encoding='utf-8') as f:
                lines = f.readlines()[:30]
            block += ''.join(lines)
        except (OSError, UnicodeDecodeError):
            block += "[Could not read file]\n"
        block += "\n"

        if len(prompt) + len(block) > MAX_PROMPT_CHARS:
            break
        prompt += block

    return prompt


def _parse_response(response_text: str, ranked_files: list) -> list:
    """
    Parse LLM response back into ranked_files format.
    Falls back to original ranking if parsing fails.
    """
    import json
    try:
        # strip any accidental markdown fences
        clean = response_text.strip().replace('```json', '').replace('```', '').strip()
        reordered_paths = json.loads(clean)

        # rebuild ranked_files in new order, preserving original scores
        score_map = {fp: score for fp, score in ranked_files}
        reordered = [(fp, score_map.get(fp, 0)) for fp in reordered_paths if fp in score_map]

        # append any files LLM didn't mention at the end (safety net)
        mentioned = set(reordered_paths)
        for fp, score in ranked_files:
            if fp not in mentioned:
                reordered.append((fp, score))

        return reordered
    except Exception:
        return ranked_files


def _validate_with_gemini(ranked_files: list, api_key: str) -> list:
    from google import genai
    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(ranked_files)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return _parse_response(response.text, ranked_files)


def _validate_with_openai(ranked_files: list, api_key: str) -> list:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = _build_prompt(ranked_files)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return _parse_response(response.choices[0].message.content, ranked_files)


def _validate_with_anthropic(ranked_files: list, api_key: str) -> list:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    prompt = _build_prompt(ranked_files)
    response = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=1024,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return _parse_response(response.content[0].text, ranked_files)