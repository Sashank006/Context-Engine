import os

CONTENT_SIGNALS = {
    'Python': ['if __name__ == "__main__"'],
    'JavaScript': ['app.listen(', 'server.listen(', 'createServer('],
    'TypeScript': ['app.listen(', 'server.listen('],
    'Go': ['func main()'],
    'Ruby': ['Sinatra::Application', 'Rails.application'],
    'Java': ['public static void main'],
    'Kotlin': ['fun main('],
    'Rust': ['fn main()'],
    'Swift': ['@main', 'UIApplicationMain'],
    'PHP': ['<?php'],
    'C#': ['static void Main(', 'static async Task Main('],
    'C++': ['int main('],
}

ENTRY_POINT_FILENAMES = {
    'Python': ['main.py', 'app.py', 'run.py', 'manage.py', 'server.py', 'wsgi.py', 'asgi.py'],
    'JavaScript': ['index.js', 'app.js', 'server.js', 'main.js'],
    'TypeScript': ['index.ts', 'app.ts', 'server.ts', 'main.ts'],
    'Go': ['main.go'],
    'Ruby': ['app.rb', 'main.rb', 'config.ru', 'Rakefile'],
    'Java': ['Main.java', 'App.java', 'Application.java'],
    'Kotlin': ['Main.kt', 'App.kt', 'Application.kt'],
    'Swift': ['main.swift', 'App.swift'],
    'Rust': ['main.rs'],
    'PHP': ['index.php', 'app.php', 'main.php'],
    'C#': ['Program.cs', 'Main.cs', 'Startup.cs'],
    'C++': ['main.cpp', 'app.cpp'],
    'Scala': ['Main.scala', 'App.scala'],
    'Elixir': ['mix.exs', 'application.ex'],
    'Haskell': ['Main.hs', 'app.hs'],
    'Dart': ['main.dart'],
    'R': ['main.R', 'app.R', 'run.R'],
    'Julia': ['main.jl', 'app.jl'],
    'Perl': ['main.pl', 'app.pl', 'index.pl'],
    'Lua': ['main.lua', 'app.lua'],
}

def detect_entry_point(file_paths, primary_language):
    signals = CONTENT_SIGNALS.get(primary_language, [])
    for fp in file_paths:
        if os.path.getsize(fp) > 2_000_000:
            continue
        try:
            with open(fp, encoding='utf-8') as f:
                content = f.read()
            for signal in signals:
                if signal in content:
                    return fp
        except (OSError, UnicodeDecodeError):
            continue
    
    candidates = ENTRY_POINT_FILENAMES.get(primary_language, [])
    for fp in file_paths:
        for candidate in candidates:
            if fp.endswith(candidate):
                return fp
    
    return "Unknown"
    