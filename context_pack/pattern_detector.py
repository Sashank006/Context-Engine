import os

PATTERNS = {
    'Microservice': {
        'files': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'],
        'folders': ['kubernetes', 'k8s', 'helm'],
        'dependencies': []
    },
    'REST API': {
        'files': [],
        'folders': ['routes', 'endpoints', 'controllers', 'serializers'],
        'dependencies': ['fastapi', 'flask-restful', 'djangorestframework', 'express']
    },
    'CLI Tool': {
        'files': [],
        'folders': ['commands', 'cmd'],
        'dependencies': ['typer', 'click', 'argparse']
    },
    'MVC': {
        'files': [],
        'folders': ['models', 'views', 'controllers', 'templates'],
        'dependencies': ['django', 'rails', 'laravel']
    },
    'Pipeline': {
        'files': [],
        'folders': ['pipeline', 'stages', 'steps', 'processors'],
        'dependencies': ['airflow', 'prefect', 'luigi']
    },
    'Task Queue': {
        'files': [],
        'folders': ['tasks', 'workers', 'jobs'],
        'dependencies': ['celery', 'redis', 'dramatiq', 'rq']
    },
    'Machine Learning': {
        'files': ['train.py', 'predict.py', 'model.pkl', 'model.pt', 'model.h5'],
        'folders': ['models', 'checkpoints', 'experiments', 'notebooks'],
        'dependencies': ['tensorflow', 'torch', 'sklearn', 'scikit-learn', 'keras', 'xgboost']
    },
    'Data Science': {
        'files': [],
        'folders': ['notebooks', 'data', 'analysis', 'reports'],
        'dependencies': ['numpy', 'pandas', 'matplotlib', 'seaborn', 'plotly', 'scipy']
    },
}


def detect_patterns(file_paths, dep_files, path="."):
    detected = []

    # read all dependency file contents
    dep_content = ""
    for dep_file in dep_files:
        try:
            with open(dep_file, encoding='utf-8') as f:
                dep_content += f.read().lower()
        except (OSError, UnicodeDecodeError):
            pass

    # get folder names and filenames in codebase
    filenames = [os.path.basename(fp).lower() for fp in file_paths]
    folders = set()
    for fp in file_paths:
        parts = fp.replace('\\', '/').split('/')
        for part in parts[:-1]:
            folders.add(part.lower())

    # check root for infrastructure files
    try:
        root_files = [f.lower() for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except (OSError, PermissionError):
        root_files = []

    for pattern, signals in PATTERNS.items():
        matched = False

        for f in signals['files']:
            if f.lower() in root_files or f.lower() in filenames:
                matched = True
                break

        if not matched:
            for folder in signals['folders']:
                if folder in folders:
                    matched = True
                    break

        if not matched:
            for dep in signals['dependencies']:
                if dep in dep_content:
                    matched = True
                    break

        if matched:
            detected.append(pattern)

    return detected if detected else ['General Project']