import os

MAX_FILES = 500

def scan_directory(path="."):
    """Walk directory and find code files and dependency files."""
    
    # validate path
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
    if not os.path.isdir(path):
        raise ValueError(f"Path is not a directory: {path}")

    code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.rs', '.php', '.cs', '.cpp']
    ignore_folders = ['venv', '__pycache__', '.git', 'node_modules']
    dependency_files = [
        'requirements.txt', 'Pipfile', 'pyproject.toml',
        'package.json', 'go.mod', 'Cargo.toml',
        'pom.xml', 'build.gradle', 'composer.json',
        'pubspec.yaml', 'mix.exs', 'Package.swift',
    ]

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

    # check for dependency files in root only
    found_dependency_files = []
    for dep_file in dependency_files:
        full_path = os.path.join(path, dep_file)
        if os.path.exists(full_path):
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