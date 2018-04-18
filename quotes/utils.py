import subprocess
import os


def execute_success(command):
    """Returns output if no excepcion ocurred, False otherwise"""

    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT)
        return output.decode('unicode_escape').strip('\n')
    except Exception:
        return False


def is_active(copy_hook):
    """Check if git-quotes is on. (prepare-commit-msg in hooks folder)"""

    return os.path.isfile(copy_hook)


def on_git_repo():
    return bool(execute_success(['git', 'rev-parse', '--is-inside-work-tree']))


def get_repo_path():
    return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel']
    ).decode('unicode_escape').strip()


def create_git_repository(directory):
    proc = subprocess.Popen(
            ['git', 'init'],
            stdout=subprocess.PIPE,
            bufsize=1,
            cwd=directory
    )
    proc.wait()
    return str(proc.stdout.read().decode('unicode_escape'))
