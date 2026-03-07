import os
import re

IMPORTANCE_SCORES = {
    'main': 30,
    'app': 25,
    'core': 25,
    'api': 20,
    'server': 20,
    'index': 20,
    'cli': 15,
    'config': 15,
    'settings': 15,
    'routes': 15,
    'models': 15,
    'database': 15,
    'db': 15,
    'auth': 10,
    'utils': 5,
    'helpers': 5,
    'constants': 5,
    'test': -20,
    'tests': -20,
    'spec': -15,
    'mock': -15,
    'fixture': -10,
    'migrations': -10,
    'seed': -10,
}

CONTENT_SIGNALS = {
    'route': 8,
    'router': 8,
    'app.get': 8,
    'app.post': 8,
    'model': 6,
    'schema': 6,
    'if __name__': 10,
    'app.run': 10,
    'listen': 7,
}

UTILITY_KEYWORDS = ['utils', 'helpers', 'constants', 'colors', 'types', 'enums']
TEST_KEYWORDS = ['test', 'tests', 'spec', 'mock']


def build_import_map(file_paths):
    import_counts = {fp: 0 for fp in file_paths}
    test_only = {fp: True for fp in file_paths}

    for fp in file_paths:
        is_test_file = any(kw in fp.lower() for kw in TEST_KEYWORDS)
        try:
            with open(fp, encoding='utf-8') as f:
                lines = f.readlines()[:20]
            for line in lines:
                line = line.strip()
                if not line.startswith('import') and not line.startswith('from'):
                    continue
                match = re.search(r'(?:from|import)\s+([\w.]+)', line)
                if not match:
                    continue
                module = match.group(1).replace('.', os.sep)
                for target_fp in file_paths:
                    normalized_target = os.path.splitext(target_fp)[0].replace('.\\', '').replace('./', '').replace(os.sep, '.')
                    if module.replace(os.sep, '.') == normalized_target:
                        filename = os.path.basename(target_fp).lower()
                        if any(kw in filename for kw in UTILITY_KEYWORDS):
                            import_counts[target_fp] = min(import_counts[target_fp] + 1, 2)
                        else:
                            import_counts[target_fp] += 1
                        if not is_test_file:
                            test_only[target_fp] = False
        except (OSError, UnicodeDecodeError):
            continue

    return import_counts, test_only


def get_usage_multiplier(import_count, is_test_only):
    if is_test_only:
        base = 0.7
    elif import_count == 0:
        base = 0.5
    elif import_count <= 2:
        base = 1.0
    elif import_count <= 5:
        base = 1.3
    else:
        base = 1.5
    return base


def score_file(fp, entry_point, import_count, is_test_only):
    score = 0
    filename = os.path.basename(fp).lower()
    is_entry = os.path.abspath(fp) == os.path.abspath(entry_point)

    # name scoring
    for keyword, points in IMPORTANCE_SCORES.items():
        if keyword in filename:
            score += points

    # entry point bonus
    if is_entry:
        score += 40

    # depth penalty
    depth = fp.replace('\\', '/').count('/')
    score -= depth * 3

    # content scoring
    try:
        with open(fp, encoding='utf-8') as f:
            lines = f.readlines()
        sample = lines[:50] + lines[-20:]
        content = ''.join(sample).lower()
        for signal, points in CONTENT_SIGNALS.items():
            if signal in content:
                score += points
    except (OSError, UnicodeDecodeError):
        pass

    # usage multiplier — entry point always gets at least 1.0
    multiplier = get_usage_multiplier(import_count, is_test_only)
    if is_entry:
        multiplier = max(multiplier, 1.0)

    score = score * multiplier
    return score


def rank_files(file_paths, entry_point):
    import_counts, test_only = build_import_map(file_paths)
    scored = []
    for fp in file_paths:
        score = score_file(
            fp,
            entry_point,
            import_counts.get(fp, 0),
            test_only.get(fp, True)
        )
        scored.append((fp, round(score)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored