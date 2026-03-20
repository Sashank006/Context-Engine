from context_pack.scanner import scan_directory
from context_pack.language_detector import detect_languages, get_primary_language
from context_pack.framework_detector import detect_framework
from context_pack.dependency_parser import parse_dependencies
from context_pack.entry_point_detector import detect_entry_point
from context_pack.file_ranker import rank_files
from context_pack.pattern_detector import detect_patterns
from context_pack.context_assembler import assemble_context
from context_pack.llm_validator import get_api_key, validate_ranking


def analyze(path, max_tokens=2000, llm_provider=None, skip_validation=False):
    d = {}
    files, dep_files = scan_directory(path)
    lang_result = get_primary_language(detect_languages(files))
    d['language'] = lang_result['primary']
    d['mixed'] = lang_result['mixed']
    d['secondary'] = lang_result.get('secondary', {})
    d['framework'] = detect_framework(files, dep_files, lang_result['primary'])
    d['dependencies'] = parse_dependencies(dep_files, lang_result['primary'])
    d['entry_point'] = detect_entry_point(files, lang_result['primary'])
    d['files'] = files
    d['dep_files'] = dep_files
    d['ranked_files'] = rank_files(files, d['entry_point'])
    d['patterns'] = detect_patterns(files, dep_files, path)

    # --- LLM VALIDATION (only when not in deep dive mode) ---
    if llm_provider and not skip_validation:
        api_key = get_api_key(llm_provider)
        if api_key:
            d['ranked_files'] = validate_ranking(d['ranked_files'], llm_provider, api_key)
        else:
            print(f"[Warning] No API key found for {llm_provider}. Set {llm_provider.upper()}_API_KEY env variable. Running without LLM validation.")

    d['context'] = assemble_context(d, max_tokens=max_tokens)
    return d