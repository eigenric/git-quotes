from __future__ import unicode_literals

import io
import json
import random
import os
import textwrap
import click
import crayons

dir_path = os.path.dirname(os.path.realpath(__file__))
original_quotes = os.path.join(dir_path, 'hooks/quotes.json')


class GitQuotesGroup(click.Group):
    """Custom Group class provides formatted main help"""

    def invoke(self, ctx):

        # Pass subcommand args to context!
        ctx.obj = tuple(ctx.args)
        super(GitQuotesGroup, self).invoke(ctx)

    def get_help_option(self, ctx):
        """Override for showing formatted main help via --help and -h"""

        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    # legit main help
                    click.echo(format_help(ctx.get_help()))
                else:
                    # legit sub-command help
                    click.echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return click.Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help='Show this message and exit.',
        )


def format_help(help):
    """Formats the help string."""

    help = help.replace('Usage:', str(crayons.white('Usage:', bold=True)))
    help = help.replace('Options:', str(crayons.white('Options:', bold=True)))
    help = help.replace('Commands:',
                        str(crayons.white('Commands:', bold=True))
                        )

    help = help.replace(
        'Add beautiful quotes to your commits!',
        str(crayons.white('Add beautiful quotes to your commits!', bold=True))
                        )

    help = help.replace(
        'git-quotes',
        str(crayons.blue('git-quotes', bold=True))
                       )

    help = help.replace('  on', str(crayons.green('  on', bold=True)))
    help = help.replace('  off', str(crayons.red('  off', bold=True)))
    help = help.replace('  toggle', str(crayons.yellow('  toggle', bold=True)))
    help = help.replace(
        '  status',
        str(crayons.magenta('  status', bold=True))
                        )

    help = help.replace('  refresh',
                        str(crayons.blue('  refresh', bold=True))
                        )

    with io.open(original_quotes, "r", encoding="utf-8") as qfile:
        quotes = json.load(qfile)
    quote = random.choice(quotes)

    # Avoid large quotes
    while len(quote['text']+quote['autor']) > 150:
        quote = random.choice(quotes)

    quote = '{} ~ {}'.format(
            quote['text'],
            str(crayons.blue(quote['autor'], bold=True))
    )
    quote = '\n'.join(textwrap.wrap(quote, width=79))
    help = "{}\n\n{}".format(help, str(crayons.cyan(quote, bold=True)))

    return help
