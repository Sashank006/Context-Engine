import json
import re

def parse_dependencies(dep_files, primary_language):
    dependencies = []
    for dep_file in dep_files:
        if 'requirements.txt' in dep_file:
            try:
                with open(dep_file, encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or line.startswith('-') or line.startswith('git+'):
                            continue
                        # handle all version specifiers: ==, >=, <=, ~=, !=, >
                        match = re.split(r'[><=!~]+', line)
                        name = match[0].split('[')[0].strip()
                        version = match[1].strip() if len(match) > 1 else "unknown"
                        if name:
                            dependencies.append({"name": name, "version": version})
            except (OSError, UnicodeDecodeError):
                continue

        elif 'package.json' in dep_file:
            try:
                with open(dep_file, encoding='utf-8') as f:
                    data = json.load(f)
                    for section in ['dependencies', 'devDependencies']:
                        for name, version in data.get(section, {}).items():
                            dependencies.append({"name": name, "version": version})
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue

    return dependencies