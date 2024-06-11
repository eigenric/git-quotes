import os
import filecmp
import sys
import crayons
import click

from shutil import copyfile
from .groups import GitQuotesGroup, format_help
from .utils import (on_git_repo, get_repo_path, create_git_repository,
                    is_active)

# Original files
dir_path = os.path.dirname(os.path.realpath(__file__))
original_hook = os.path.join(dir_path, 'hooks/prepare-commit-msg')
original_quotes = os.path.join(dir_path, 'hooks/quotes.json')


if on_git_repo():
    repo_path = get_repo_path()
else:
    repo_path = os.getcwd()

hooks_folder = os.path.join(repo_path, '.git/hooks')
copy_hook = os.path.join(hooks_folder, 'prepare-commit-msg')
sample_hook = os.path.join(hooks_folder, 'prepare-commit-msg-quotes')
copy_quotes = os.path.join(hooks_folder, 'quotes.json')

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
        # Exceptions for commands with global options
        if ctx.invoked_subcommand in ['on', 'off']:
                return
        elif not on_git_repo():
            click.secho("\nThere is no repository here!", fg="cyan")
            sys.exit(0)


@cli.command(short_help="Activate git-quotes in a repository")
@click.option('--force', is_flag=True)
@click.option("--default", is_flag=True)
@click.pass_context
def on(ctx, force, default):
    """Activate git-quotes in a repository"""

    if default:
        global_path = os.path.expanduser("~/.git-templates/hooks")
        ghook = os.path.join(global_path, "prepare-commit-msg")
        gsample = os.path.join(global_path, "prepare-commit-msg-quotes")
        gquotes = os.path.join(global_path, "quotes.json")

        if os.path.exists(global_path):

            is_ghook_file = os.path.isfile(ghook)
            is_gsample_file = os.path.isfile(gsample)

            installed = (
              (is_ghook_file and filecmp.cmp(original_hook, ghook)) or
              (is_gsample_file and filecmp.cmp(original_hook, gsample))
            )

            if installed:
                click.secho("\nGit-quotes is already activated by default",
                            fg="green")
                sys.exit(0)
        else:
            click.secho("Creating git-templates folder...", fg="green")
            os.makedirs(global_path)

        copyfile(original_hook, ghook)
        copyfile(original_quotes, gquotes)

        # Execution permissions
        if os.name == 'posix' and os.path.exists(ghook):
            os.chmod(ghook, int('755', 8))

        click.secho("\nGit-quotes activated by default for new repositories",
                    fg="green")
        sys.exit(0)

    # Create repo with on --force or show help
    if not on_git_repo():
        if not force:
            click.secho("\nThere is no repository here!\n", fg="cyan")

            option = str(crayons.green('--force', bold=True))
            msg = "{}{}".format(str(crayons.green("Use ")), option)
            msg = "{}{}".format(msg, str(crayons.green(" to create one\n")))

            option2 = str(crayons.green('--default', bold=True))
            msg2 = "{}{}".format(str(crayons.green("Use ")), option2)
            msg2 = "{}{}".format(
                msg2, str(crayons.green(" to activate git-quotes by default"))
                               )
            click.secho("{}{}".format(msg, msg2))
            sys.exit(0)
        else:
            click.secho("Creating git repository here...", fg='green')
            msg = create_git_repository(os.getcwd())
            click.secho("> {}".format(msg), fg='cyan')

    if is_active(copy_hook):
        click.secho("\nGit-quotes is active!", fg="green")
        return

    # Activate
    if os.path.isfile(sample_hook):
        os.rename(sample_hook, copy_hook)
    else:
        copyfile(original_hook, copy_hook)
        copyfile(original_quotes, copy_quotes)

    # Execution permissions
    if os.name == 'posix' and os.path.exists(copy_hook):
        os.chmod(copy_hook, int('755', 8))

    click.secho("\nGit-quotes has been activated successfully :)", fg="green")

    if force:
        ctx.invoke(refresh)


@cli.command(short_help="Refresh hook if it changed")
def refresh():
    """Refresh hook if it changed"""

    if is_active(copy_hook):
        click.secho("Git-quotes is active\n", fg="green")
        if not filecmp.cmp(original_hook, copy_hook):  # Change
            click.secho("Hook has changed, copying...", fg="green")
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
@click.option("--default", is_flag=True)
def off(default):
    """Disable git-quotes in a repository"""

    if default:
        global_path = os.path.expanduser("~/.git-templates/hooks")
        ghook = os.path.join(global_path, "prepare-commit-msg")
        gquotes = os.path.join(global_path, "quotes.json")

        if os.path.exists(ghook):
            os.remove(ghook)
        if os.path.exists(gquotes):
            os.remove(gquotes)

            click.secho("\nGit quotes is now disabled by default",
                        fg="green")
        else:
            click.secho("\nGit quotes is already disabled by default",
                        fg="green")
    else:
        if not on_git_repo():
            click.secho("\nThere is no repository here!\n", fg="cyan")

        if is_active(copy_hook):
            os.rename(copy_hook, sample_hook)
            click.secho("\nGit-quotes has been disabled! :(", fg="cyan")
        else:
            click.secho("\nGit-quotes was already unactive! :()", fg="cyan")

        option = str(crayons.green('--default', bold=True))
        msg = "{}{}".format(str(crayons.green("\nUse ")), option)
        msg = "{}{}".format(
            msg, str(crayons.green(" to disable git-quotes by default"))
                           )
        click.secho(msg)


@cli.command(short_help="Toggle git-quotes status")
@click.pass_context
def toggle(ctx):
    """Toggle git-quotes status"""

    if not is_active(copy_hook):
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

    if is_active(copy_hook):
        click.secho("\nGit-quotes is active! :D", fg="green")
    else:
        click.secho("\nGit-quotes is unactive! :@", fg="cyan")
