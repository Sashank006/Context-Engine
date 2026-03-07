from context_pack.analyzer import analyze

def test_basic():
    result = analyze(".")
    
    assert result['language'] == 'Python', f"Expected Python, got {result['language']}"
    assert result['framework'] == 'Typer', f"Expected Typer, got {result['framework']}"
    assert result['entry_point'] != 'Unknown', f"Entry point not found"
    assert len(result['dependencies']) > 0, "No dependencies found"
    assert len(result['files']) > 0, "No files found"
    
    print("All tests passed!")

test_basic()