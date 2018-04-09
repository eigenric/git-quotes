import click
import os

from shutil import copyfile

dir_path = os.path.dirname(os.path.realpath(__file__))
original_hook = os.path.join(dir_path, 'hooks/prepare-commit-msg')
original_quotes = os.path.join(dir_path, 'hooks/quotes.json')

hooks_folder = os.path.join(os.getcwd(), '.git/hooks')
copy_hook = os.path.join(hooks_folder, 'prepare-commit-msg')
sample_hook = os.path.join(hooks_folder, 'prepare-commit-msg-quotes')
copy_quotes = os.path.join(hooks_folder, 'quotes.json')

@click.group()
def cli():
    """Add beautiful quotes to your commits!"""

@cli.command(short_help="Activate git-quotes in a repository")
def activate():
    """Activate git-quotes in a repository"""

    # Activate a repository with global templates in it
    if os.path.isfile(sample_hook):
        os.rename(sample_hook, copy_hook)
    else:
        copyfile(original_hook, copy_hook)
        copyfile(original_quotes, copy_quotes)

    # Execution permissions
    if os.name is 'posix' and os.path.exists(copy_hook):
        os.chmod(copy_hook, int('755', 8))

    click.secho("git-quotes has been activated successfully :)", fg="green")

@cli.command(short_help="Deactivate git-quotes in a repository")
def deactivate():
    """Deactivate git-quotes in a repository"""

    if os.path.isfile(copy_hook):
        os.rename(copy_hook, sample_hook)
        click.secho("git-quotes has been desactivated :(", fg="red")
    else:
        click.secho("git-quotes has already unactive :()", fg="red")
