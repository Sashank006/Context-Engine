import os
from context_pack.language_detector import EXTENSION_MAP

MAX_FILES = 3000

def scan_directory(path="."):
    """Walk directory and find code files and dependency files."""
    
    # validate path
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
    if not os.path.isdir(path):
        raise ValueError(f"Path is not a directory: {path}")

    ignore_folders = set(['venv', '__pycache__', '.git', 'node_modules', '.idea', '.vscode', 'dist', 'build', 'target', 'runtime', 'vendor', 'examples', 'docs', 'assets', 'static', 'migrations', 'fixtures', 'third_party', 'contrib', 'scripts', 'tools', 'ci', '.github', 'cmake', 'bin', 'obj', 'out', 'coverage', 'gen', 'generated', 'autoconf', 'autom4te.cache'])

    # load .contextignore if present in scanned path
    contextignore_path = os.path.join(path, '.contextignore')
    if os.path.exists(contextignore_path):
        try:
            with open(contextignore_path, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_folders.add(line.strip('/'))
            print(f"[info] Loaded .contextignore from {contextignore_path}")
        except (OSError, UnicodeDecodeError):
            pass
    dependency_files = [
        'requirements.txt', 'Pipfile', 'pyproject.toml',
        'package.json', 'go.mod', 'Cargo.toml',
        'pom.xml', 'build.gradle', 'composer.json',
        'pubspec.yaml', 'mix.exs', 'Package.swift',
    ]

    code_extensions = set(EXTENSION_MAP.keys())  # single source of truth
    code_files = []
    warned = False

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                code_files.append(os.path.join(root, file))
                if len(code_files) >= MAX_FILES and not warned:
                    print(f"[warning] Large codebase detected — limiting to {MAX_FILES} files for performance.")
                    warned = True
                if len(code_files) >= MAX_FILES:
                    break
        if len(code_files) >= MAX_FILES:
            break

    # check for dependency files in root and one level deep
    found_dependency_files = []
    search_dirs = [path] + [os.path.join(path, d) for d in os.listdir(path) 
                            if os.path.isdir(os.path.join(path, d))]
    for search_dir in search_dirs:
        for dep_file in dependency_files:
            full_path = os.path.join(search_dir, dep_file)
            if os.path.exists(full_path) and full_path not in found_dependency_files:
                found_dependency_files.append(full_path)

    return code_files, found_dependency_files


if __name__ == "__main__":
    files, deps = scan_directory(".")
    print(f"Found {len(files)} code files:")
    for f in files:
        print(f"  - {f}")
    print(f"\nFound {len(deps)} dependency files:")
    for d in deps:
        print(f"  - {d}")