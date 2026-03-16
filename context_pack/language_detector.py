import os

EXTENSION_MAP = {
    # Python
    '.py': 'Python',
    # JavaScript / TypeScript
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'JavaScript',
    '.tsx': 'TypeScript',
    '.mjs': 'JavaScript',
    '.cjs': 'JavaScript',
    # Java
    '.java': 'Java',
    # C / C++
    '.c': 'C',
    '.h': 'C',
    '.cc': 'C++',
    '.cpp': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++',
    # C#
    '.cs': 'C#',
    # Go
    '.go': 'Go',
    # Rust
    '.rs': 'Rust',
    # Ruby
    '.rb': 'Ruby',
    '.erb': 'Ruby',
    # PHP
    '.php': 'PHP',
    # Swift
    '.swift': 'Swift',
    # Kotlin
    '.kt': 'Kotlin',
    '.kts': 'Kotlin',
    # Lua
    '.lua': 'Lua',
    # Shell
    '.sh': 'Shell',
    '.bash': 'Shell',
    '.zsh': 'Shell',
    # Vim
    '.vim': 'VimScript',
    '.nvim': 'VimScript',
    # Scala
    '.scala': 'Scala',
    # Haskell
    '.hs': 'Haskell',
    # Elixir
    '.ex': 'Elixir',
    '.exs': 'Elixir',
    # Dart
    '.dart': 'Dart',
    # R
    '.r': 'R',
    '.R': 'R',
    # MATLAB
    '.m': 'MATLAB',
    # HTML / CSS (front end projects)
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'CSS',
    '.sass': 'CSS',
}


def detect_languages(file_paths):
    language_counts = {}
    for i in file_paths:
        ext = os.path.splitext(i)[1]
        lang = EXTENSION_MAP.get(ext)
        if lang is None:
            continue
        if lang in language_counts:
            language_counts[lang] += 1
        else:
            language_counts[lang] = 1
    return language_counts


def get_primary_language(counts):
    if not counts:
        return {"primary": "Unknown", "mixed": False, "all": {}}
    total = sum(counts.values())
    primary = max(counts, key=counts.get)
    mixed = any(count / total > 0.2 for lang, count in counts.items() if lang != primary)
    return {"primary": primary, "mixed": mixed, "all": counts}