from __future__ import unicode_literals

import os
import filecmp
import random
import json
import subprocess
import sys
import crayons
import click

from shutil import copyfile
from .groups import GitQuotesGroup, format_help
from .utils import on_git_repo, get_repo_path, create_git_repository

# Original files
dir_path = os.path.dirname(os.path.realpath(__file__))
original_hook = os.path.join(dir_path, 'hooks/prepare-commit-msg')
original_quotes = os.path.join(dir_path, 'hooks/quotes.json')

# Copied files, repository dependent
if on_git_repo():
    repo_path = get_repo_path()
else:
    repo_path = os.getcwd()

hooks_folder = os.path.join(repo_path, '.git/hooks')
copy_hook = os.path.join(hooks_folder, 'prepare-commit-msg')
sample_hook = os.path.join(hooks_folder, 'prepare-commit-msg-quotes')
copy_quotes = os.path.join(hooks_folder, 'quotes.json')

def is_active():
    """Check if git-quotes is on. (prepare-commit-msg in hooks folder)"""

    return os.path.isfile(copy_hook)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(
    cls=GitQuotesGroup,
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """Add beautiful quotes to your commits!"""

    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))
    else:
        if ctx.invoked_subcommand == 'on':
            return
        elif not on_git_repo():
            click.secho("\nThere is no repository here!", fg="cyan")
            sys.exit(0)

@cli.command(short_help="Activate git-quotes in a repository")
@click.option('--force', is_flag=True)
def on(force):
    """Activate git-quotes in a repository"""

    if not on_git_repo():
        if not force:
            click.secho("\nThere is no repository here!...", fg='cyan')
            option = str(crayons.green('--force', bold=True))
            msg = "{}{}".format(str(crayons.green("Use ")), option)
            msg = "{}{}".format(msg, str(crayons.green(" to create one")))
            click.secho(msg)
            sys.exit(0)
        else:
            click.secho("Creating git repository here...", fg='green')
            msg = create_git_repository(os.getcwd())
            click.secho("> {}".format(msg), fg='cyan')


    if is_active():
        click.secho("\nGit-quotes was already active!", fg="green")
        return

    if os.path.isfile(sample_hook):
        os.rename(sample_hook, copy_hook)
    else:
        copyfile(original_hook, copy_hook)
        copyfile(original_quotes, copy_quotes)

    # Execution permissions
    if os.name is 'posix' and os.path.exists(copy_hook):
        os.chmod(copy_hook, int('755', 8))

    click.secho("\nGit-quotes has been activated successfully :)", fg="green")

@cli.command(short_help="Refresh hook if it changed")
def refresh():
    """Refresh hook if it changed"""

    if is_active():
        click.secho("Git-quotes is active\n", fg="green")
        if not filecmp.cmp(original_hook, copy_hook): # Change
            click.secho("Hook has changed, copying..!", fg="green")
            click.secho("Done!", fg="green")
            copyfile(original_hook, copy_hook)
        else:
            click.secho("No hook has changed!", fg="green")
    else:
        click.secho("Git-quotes is unactive\n", fg="cyan")
        if not filecmp.cmp(original_hook, sample_hook):
            click.secho("Hook has changed, copying...", fg="green")
            click.secho("Done!", fg="green")
            copyfile(original_hook, sample_hook)
        else:
            click.secho("No hook has changed!", fg="green")

@cli.command(short_help="Disable git-quotes in a repository")
def off():
    """Disable git-quotes in a repository"""

    if is_active():
        os.rename(copy_hook, sample_hook)
        click.secho("\nGit-quotes has been desactivated! :(", fg="cyan")
    else:
        click.secho("\nGit-quotes was already unactive! :()", fg="cyan")

@cli.command(short_help="Toggle git-quotes status")
@click.pass_context
def toggle(ctx):
    """Toggle git-quotes status"""

    if not is_active():
        ctx.forward(on)
    else:
        ctx.forward(off)

@cli.command(short_help="Show git-quotes status")
@click.option('--repo', is_flag=True)
def status(repo):
    """Show git-quotes status"""

    if repo:
        repo_name = str(crayons.green(repo_path.split('/')[-1], bold=True))
        click.secho("You are in {}".format(repo_name), fg='green')

    if is_active():
        click.secho("\nGit-quotes is active! :D", fg="green")
    else:
        click.secho("\nGit-quotes is unactive! :@", fg="cyan")
