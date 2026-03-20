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


# languages that don't count as "real" secondary languages for mixed detection
NON_PROGRAMMING_LANGUAGES = {'HTML', 'CSS', 'Shell', 'VimScript'}

def get_primary_language(counts):
    if not counts:
        return {"primary": "Unknown", "mixed": False, "all": {}}
    total = sum(counts.values())
    primary = max(counts, key=counts.get)

    # only count real programming languages for mixed detection
    programming_counts = {
        lang: count for lang, count in counts.items()
        if lang not in NON_PROGRAMMING_LANGUAGES
    }
    programming_total = sum(programming_counts.values())

    # find all secondary languages above 20% threshold
    secondary = {
        lang: count for lang, count in programming_counts.items()
        if lang != primary and programming_total > 0 and count / programming_total > 0.2
    }

    mixed = len(secondary) > 0
    return {"primary": primary, "mixed": mixed, "secondary": secondary, "all": counts}