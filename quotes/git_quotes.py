from __future__ import unicode_literals

import click
import os
import filecmp
import json
import random

from shutil import copyfile
from .groups import GitQuotesGroup, format_help

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

dir_path = os.path.dirname(os.path.realpath(__file__))
original_hook = os.path.join(dir_path, 'hooks/prepare-commit-msg')
original_quotes = os.path.join(dir_path, 'hooks/quotes.json')

hooks_folder = os.path.join(os.getcwd(), '.git/hooks')
copy_hook = os.path.join(hooks_folder, 'prepare-commit-msg')
sample_hook = os.path.join(hooks_folder, 'prepare-commit-msg-quotes')
copy_quotes = os.path.join(hooks_folder, 'quotes.json')

def is_active():
    return os.path.isfile(copy_hook)

@click.group(
    cls=GitQuotesGroup,
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """Add beautiful quotes to your commits!"""

    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))
    elif not os.path.isdir(hooks_folder): # There is not repo!
        click.secho("\nThere's no Git repository here!", fg="cyan")
        ctx.exit()

@cli.command(short_help="Activate git-quotes in a repository")
def on():
    """Activate git-quotes in a repository"""

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
def status():
    """Show git-quotes status"""

    if is_active():
        click.secho("\nGit-quotes is active! :D", fg="green")
    else:
        click.secho("\nGit-quotes is unactive! :@", fg="cyan")
