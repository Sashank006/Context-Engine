import os
EXTENSION_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'JavaScript',
    '.tsx': 'TypeScript',
    '.java': 'Java',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.rs': 'Rust',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
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