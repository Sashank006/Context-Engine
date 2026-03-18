import os
import json

LANGUAGE_DEP_FILES = {
    'Python': ['requirements.txt', 'Pipfile', 'pyproject.toml'],
    'JavaScript': ['package.json'],
    'TypeScript': ['package.json'],
    'Go': ['go.mod'],
    'Ruby': ['Gemfile'],
    'Java': ['pom.xml', 'build.gradle'],
    'Kotlin': ['build.gradle', 'build.gradle.kts'],
    'Swift': ['Package.swift', 'Podfile'],
    'Rust': ['Cargo.toml'],
    'PHP': ['composer.json'],
    'C#': ['packages.config', '.csproj'],
    'C++': ['CMakeLists.txt', 'conanfile.txt'],
    'Scala': ['build.sbt'],
    'Elixir': ['mix.exs'],
    'Haskell': ['package.yaml', 'cabal.project'],
    'Dart': ['pubspec.yaml'],
    'R': ['DESCRIPTION'],
    'Julia': ['Project.toml'],
    'Perl': ['cpanfile'],
    'Lua': ['rockspec'],
}

# ORDER MATTERS — more specific frameworks must come before generic ones
# e.g. Next.js before React, NestJS before Express, FastAPI before Flask
FRAMEWORK_SIGNATURES = {
    # JavaScript/TypeScript — specific before generic
    'Next.js': {'dependencies': ['next'], 'files': ['next.config.js', 'next.config.mjs', 'next.config.ts']},
    'NestJS': {'dependencies': ['@nestjs/core'], 'files': []},
    'Angular': {'dependencies': ['@angular/core'], 'files': ['angular.json']},
    'Svelte': {'dependencies': ['svelte'], 'files': ['svelte.config.js']},
    'Vue': {'dependencies': ['vue'], 'files': []},
    'React': {'dependencies': ['react'], 'files': []},
    'Express': {'dependencies': ['express'], 'files': []},
    # Python — specific before generic
    'FastAPI': {'dependencies': ['fastapi'], 'files': []},
    'Django': {'dependencies': ['django'], 'files': ['manage.py']},
    'Flask': {'dependencies': ['flask'], 'files': []},
    'Typer': {'dependencies': ['typer'], 'files': []},
    'Click': {'dependencies': ['click'], 'files': []},
    # Other languages
    'Spring': {'dependencies': ['spring-boot'], 'files': []},
    'Rails': {'dependencies': ['rails'], 'files': []},
    'Laravel': {'dependencies': ['laravel/framework'], 'files': []},
    'Gin': {'dependencies': ['gin-gonic/gin'], 'files': []},
    'Fiber': {'dependencies': ['gofiber/fiber'], 'files': []},
}


def detect_framework(file_paths, dep_files, primary_language):
    targets = LANGUAGE_DEP_FILES.get(primary_language, [])
    dep_content = ""
    for dep_file in dep_files:
        if any(target in dep_file for target in targets):
            try:
                with open(dep_file, encoding='utf-8') as f:
                    dep_content += f.read().lower()
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue

    for frame, signals in FRAMEWORK_SIGNATURES.items():
        for keyword in signals['dependencies']:
            if keyword in dep_content:
                return frame
        for special_file in signals['files']:
            if any(special_file in fp for fp in file_paths):
                return frame

    return "Unknown"