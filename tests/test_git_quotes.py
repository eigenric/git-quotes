# test_git_quotes.py

import click
import os
import pytest
import json
import random

from click.testing import CliRunner

from quotes.utils import create_git_repository
from quotes.git_quotes import (
    on,
    off,
    toggle,
    refresh,
    status
)

def test_create_git_repository():
    assert os.path.isdir(".git")

def test_get_quote():

    # Load quotes file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    quotes_file = os.path.join(dir_path, '..', 'quotes', 'hooks', 'quotes.json')
    with open(quotes_file, "r", encoding='utf-8') as fquotes:
        quotes = json.load(fquotes)

    # Get random quote
    quote = random.choice(quotes)

    # Quotes is not empty and is in file.
    assert len(quote) > 0 and (quote in quotes)

def test_activate_git_quotes():
    runner = CliRunner()
    result = runner.invoke(on, ["--force"])

    assert result.exit_code == 0

    # Checks if hook is copied into repository
    assert os.path.isfile(os.path.join(".", '.git', 'hooks', 'prepare-commit-msg'))


def test_deactivate_git_quotes():
    runner = CliRunner()
    result = runner.invoke(off)

    assert result.exit_code == 0

    # Checks if hook is missing
    assert not os.path.isfile(os.path.join('.git', 'hooks', 'prepare-commit-msg'))

def test_toggle_git_quotes():
    runner = CliRunner()
    result_status = runner.invoke(status)

    assert result_status.exit_code == 0

    if result_status == "\nGit-quotes is unactive! :@\n":
        result_toggle_act= runner.invoke(toggle)
        assert result_toggle_act.exit_code == 0
        assert result_toggle_act.output in ["\nGit-quotes has been activated successfully :)\n", "\nGit-quotes is active!\n"]
    elif result_status == "\nGit-quotes is active!\n":
        result_toggle_disable = runner.invoke(toggle)
        assert result_toggle_disable.exit_code == 0
        msg = "\nGit-quotes has been disabled! :(\n\nUse --default to disable git-quotes by default\n"
        assert result_toggle_disable.output == msg

def test_refresh_git_quotes():
    runner = CliRunner()

    result_status = runner.invoke(status)
    result_refresh = runner.invoke(refresh)

    assert result_status.exit_code == 0
    assert result_refresh.exit_code == 0

    if result_status.output == "\nGit-quotes is active! :)\n":
        assert result_refresh.output == "\nGit-quotes is active\n\nNo hook has changed!\n"
        assert os.path.isfile(os.path.join('.git', 'hooks', 'prepare-commit-msg'))
    elif result_status.output == "\nGit-quotes is unactive! :@\n":
        assert result_refresh.output == "Git-quotes is unactive\n\nNo hook has changed!\n"
        assert os.path.isfile(os.path.join('.git', 'hooks', 'prepare-commit-msg-quotes'))

def test_check_git_quotes_status():

    runner = CliRunner()

    # Checks if status off when deactivated
    result = runner.invoke(on)
    assert result.output in ["\nGit-quotes has been activated successfully :)\n", "\nGit-quotes is active!\n"]

    result = runner.invoke(off)

    msg = "\nGit-quotes has been disabled! :(\n\nUse --default to disable git-quotes by default\n"
    assert result.output == msg