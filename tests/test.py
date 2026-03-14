import pytest
from context_pack.analyzer import analyze
from context_pack.context_assembler import (
    estimate_tokens,
    get_snippet_config,
    build_metadata_block,
    assemble_context,
)
from context_pack.llm_validator import _parse_response


# ─── Integration Test ────────────────────────────────────────────────────────

def test_basic():
    result = analyze(".")
    assert result['language'] == 'Python', f"Expected Python, got {result['language']}"
    assert result['framework'] == 'Typer', f"Expected Typer, got {result['framework']}"
    assert result['entry_point'] != 'Unknown', "Entry point not found"
    assert len(result['dependencies']) > 0, "No dependencies found"
    assert len(result['files']) > 0, "No files found"


# ─── estimate_tokens ─────────────────────────────────────────────────────────

def test_estimate_tokens_basic():
    # 4 chars = 1 token
    assert estimate_tokens("abcd") == 1

def test_estimate_tokens_empty():
    assert estimate_tokens("") == 0

def test_estimate_tokens_large():
    text = "a" * 400
    assert estimate_tokens(text) == 100


# ─── get_snippet_config ───────────────────────────────────────────────────────

def test_snippet_config_small():
    num_files, lines = get_snippet_config(5)
    assert num_files == 3
    assert lines == 50

def test_snippet_config_medium():
    num_files, lines = get_snippet_config(30)
    assert num_files == 5
    assert lines == 30

def test_snippet_config_large():
    num_files, lines = get_snippet_config(100)
    assert num_files == 7
    assert lines == 20

def test_snippet_config_boundary_low():
    # exactly 20 files should hit medium tier
    num_files, lines = get_snippet_config(20)
    assert num_files == 5
    assert lines == 30

def test_snippet_config_boundary_high():
    # exactly 50 files should hit large tier
    num_files, lines = get_snippet_config(50)
    assert num_files == 7
    assert lines == 20


# ─── build_metadata_block ────────────────────────────────────────────────────

def test_metadata_stays_within_budget():
    analysis = {
        'language': 'Python',
        'mixed': False,
        'framework': 'Typer',
        'patterns': ['CLI Tool'],
        'entry_point': 'cli.py',
        'files': ['a.py', 'b.py'],
        'dependencies': [{'name': 'typer'}, {'name': 'rich'}],
    }
    budget = 500
    result = build_metadata_block(analysis, budget)
    assert len(result) <= budget

def test_metadata_truncates_long_deps():
    # 50 dependencies should get truncated
    analysis = {
        'language': 'Python',
        'mixed': False,
        'framework': 'Django',
        'patterns': ['REST API'],
        'entry_point': 'manage.py',
        'files': ['a.py'],
        'dependencies': [{'name': f'dep{i}'} for i in range(50)],
    }
    result = build_metadata_block(analysis, 300)
    assert 'truncated' in result

def test_metadata_contains_key_fields():
    analysis = {
        'language': 'Python',
        'mixed': False,
        'framework': 'Flask',
        'patterns': ['REST API'],
        'entry_point': 'app.py',
        'files': ['app.py'],
        'dependencies': [],
    }
    result = build_metadata_block(analysis, 1000)
    assert 'Python' in result
    assert 'Flask' in result
    assert 'app.py' in result
    assert 'REST API' in result


# ─── assemble_context ────────────────────────────────────────────────────────

def test_assemble_context_respects_token_budget():
    result = analyze(".")
    context = assemble_context(result, max_tokens=2000)
    # token estimate line is at the bottom, extract it
    assert 'Token estimate:' in context
    token_line = [l for l in context.split('\n') if 'Token estimate:' in l][0]
    used = int(token_line.split(':')[1].strip().split('/')[0].strip())
    assert used <= 2000

def test_assemble_context_empty_ranked_files():
    analysis = {
        'language': 'Python',
        'mixed': False,
        'framework': 'None',
        'patterns': ['General Project'],
        'entry_point': 'Unknown',
        'files': ['a.py'],
        'dependencies': [],
        'ranked_files': [],
    }
    context = assemble_context(analysis)
    assert 'No files available to display' in context


# ─── _parse_response (llm_validator) ─────────────────────────────────────────

def test_parse_response_valid():
    ranked_files = [('./a.py', 10), ('./b.py', 5)]
    response = '["./b.py", "./a.py"]'
    result = _parse_response(response, ranked_files)
    assert result[0][0] == './b.py'
    assert result[1][0] == './a.py'

def test_parse_response_invalid_json_fallback():
    ranked_files = [('./a.py', 10), ('./b.py', 5)]
    result = _parse_response("this is not json", ranked_files)
    # should fall back to original ranking
    assert result == ranked_files

def test_parse_response_strips_markdown_fences():
    ranked_files = [('./a.py', 10), ('./b.py', 5)]
    response = '```json\n["./a.py"]\n```'
    result = _parse_response(response, ranked_files)
    assert result[0][0] == './a.py'

def test_parse_response_unknown_files_appended():
    # LLM returns only one file, the other should be appended at end
    ranked_files = [('./a.py', 10), ('./b.py', 5)]
    response = '["./a.py"]'
    result = _parse_response(response, ranked_files)
    assert result[0][0] == './a.py'
    assert result[1][0] == './b.py'  # appended as safety net