import os
import json
import hashlib
import time

CACHE_DIR = os.path.join(os.path.expanduser('~'), '.contextpack', 'cache')


def _get_cache_key(path: str) -> str:
    """Generate a unique cache key from the repo path."""
    return hashlib.md5(os.path.abspath(path).encode()).hexdigest()


def _get_cache_path(path: str) -> str:
    """Get the cache file path for a given repo."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{_get_cache_key(path)}.json")


def _get_repo_mtime(path: str) -> float:
    """
    Get the most recent modification time of any file in the repo.
    Walks the top 2 levels only for performance.
    """
    latest = 0.0
    try:
        for root, dirs, files in os.walk(path):
            # limit depth to 2 levels for performance
            depth = root.replace(path, '').count(os.sep)
            if depth >= 2:
                dirs[:] = []
                continue
            for f in files:
                try:
                    mtime = os.path.getmtime(os.path.join(root, f))
                    if mtime > latest:
                        latest = mtime
                except OSError:
                    continue
    except OSError:
        pass
    return latest


def get_cached(path: str) -> str | None:
    """
    Return cached context if repo hasn't changed since last run.
    Returns None if no cache or cache is stale.
    """
    cache_path = _get_cache_path(path)
    if not os.path.exists(cache_path):
        return None

    try:
        with open(cache_path, encoding='utf-8') as f:
            cache = json.load(f)

        cached_mtime = cache.get('mtime', 0)
        current_mtime = _get_repo_mtime(path)

        if current_mtime <= cached_mtime:
            return cache.get('context')
    except (OSError, json.JSONDecodeError):
        pass

    return None


def save_cache(path: str, context: str):
    """Save context output to cache."""
    cache_path = _get_cache_path(path)
    try:
        cache = {
            'path': os.path.abspath(path),
            'mtime': _get_repo_mtime(path),
            'cached_at': time.time(),
            'context': context
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
    except OSError:
        pass  # cache failure should never break the tool


def clear_cache(path: str = None):
    """Clear cache for a specific path or all caches."""
    if path:
        cache_path = _get_cache_path(path)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    else:
        if os.path.exists(CACHE_DIR):
            for f in os.listdir(CACHE_DIR):
                os.remove(os.path.join(CACHE_DIR, f))