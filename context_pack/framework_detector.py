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

FRAMEWORK_SIGNATURES = {
    'Flask': {'dependencies': ['flask'], 'files': []},
    'Django': {'dependencies': ['django'], 'files': ['manage.py']},
    'FastAPI': {'dependencies': ['fastapi'], 'files': []},
    'React': {'dependencies': ['react'], 'files': []},
    'Next.js': {'dependencies': ['next'], 'files': ['next.config.js']},
    'Express': {'dependencies': ['express'], 'files': []},
    'Vue': {'dependencies': ['vue'], 'files': []},
    'Angular': {'dependencies': ['@angular/core'], 'files': ['angular.json']},
    'Spring': {'dependencies': ['spring-boot'], 'files': []},
    'Rails': {'dependencies': ['rails'], 'files': []},
    'Laravel': {'dependencies': ['laravel/framework'], 'files': []},
    'Svelte': {'dependencies': ['svelte'], 'files': ['svelte.config.js']},
    'NestJS': {'dependencies': ['@nestjs/core'], 'files': []},
    'Gin': {'dependencies': ['gin-gonic/gin'], 'files': []},
    'Fiber': {'dependencies': ['gofiber/fiber'], 'files': []},
    'Typer': {'dependencies': ['typer'], 'files': []},
    'Click': {'dependencies': ['click'], 'files': []},
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