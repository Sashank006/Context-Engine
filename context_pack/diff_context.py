import subprocess
import os


def get_diff(path: str, target: str = None) -> dict | None:
    """
    Run git diff and return structured result.
    target: None = unstaged changes, 'HEAD' = since last commit, or branch name
    Returns dict with changed files and diff summary, or None on failure.
    """
    try:
        # check git is installed
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
        except FileNotFoundError:
            print("[Error] Git is not installed or not in PATH. Cannot run --diff.")
            return None

        # check if path is a git repo
        check = subprocess.run(
            ['git', '-C', path, 'rev-parse', '--is-inside-work-tree'],
            capture_output=True, text=True
        )
        if check.returncode != 0:
            print(f"[Error] {path} is not a git repository. Cannot run --diff.")
            return None

        # build git diff command
        cmd = ['git', '-C', path, 'diff']
        if target:
            cmd.append(target)

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[Error] git diff failed: {result.stderr.strip()}")
            return None

        diff_output = result.stdout
        if not diff_output.strip():
            label = "unstaged changes" if not target else f"diff with {target}"
            return {'files': [], 'diff': '', 'message': f'No {label} found.'}

        # parse changed files from diff output
        changed_files = []
        for line in diff_output.split('\n'):
            if line.startswith('diff --git'):
                # extract file path from "diff --git a/path b/path"
                parts = line.split(' b/')
                if len(parts) > 1:
                    changed_files.append(parts[1].strip())

        return {
            'files': changed_files,
            'diff': diff_output,
            'message': None
        }

    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def format_diff_output(diff_result: dict, ranked_files: list) -> str:
    """
    Format diff result into a clean summary.
    Highlights which changed files are important according to our ranker.
    """
    if diff_result.get('message'):
        return f"=== DIFF SUMMARY ===\n{diff_result['message']}"

    changed = diff_result['files']
    ranked_paths = [os.path.basename(fp) for fp, _ in ranked_files]

    # check which changed files are important
    important_changed = [f for f in changed if os.path.basename(f) in ranked_paths]
    other_changed = [f for f in changed if os.path.basename(f) not in ranked_paths]

    lines = ["=== WHAT CHANGED ==="]
    lines.append(f"Total files changed: {len(changed)}")

    if important_changed:
        lines.append("\nKey files modified (high importance):")
        for f in important_changed:
            lines.append(f"  * {f}")

    if other_changed:
        lines.append("\nOther files modified:")
        for f in other_changed[:10]:  # cap at 10 to avoid noise
            lines.append(f"  - {f}")
        if len(other_changed) > 10:
            lines.append(f"  ... and {len(other_changed) - 10} more")

    # include raw diff truncated to 2000 chars
    raw_diff = diff_result['diff']
    if len(raw_diff) > 2000:
        raw_diff = raw_diff[:2000] + '\n... [diff truncated, use Deep Dive for full details]'

    lines.append(f"\n=== RAW DIFF ===\n{raw_diff}")

    return '\n'.join(lines)