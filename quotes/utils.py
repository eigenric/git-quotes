
def format_help():
    """Formats the help string."""

    additional_help = """
Usage Examples:
   Create a new project using Python 3.6, specifically:
   $ {1}

   Install all dependencies for a project (including dev):
   $ {2}

   Create a lockfile containing pre-releases:
   $ {6}

   Show a graph of your installed dependencies:
   $ {4}

   Check your installed dependencies for security vulnerabilities:
   $ {7}

   Install a local setup.py into your virtual environment/Pipfile:
   $ {5}

   Use a lower-level pip command:
   $ {8}

Commands:""".format(
        crayons.red('pipenv --three'),
        crayons.red('pipenv --python 3.6'),
        crayons.red('pipenv install --dev'),
        crayons.red('pipenv lock'),
        crayons.red('pipenv graph'),
        crayons.red('pipenv install -e .'),
        crayons.red('pipenv lock --pre'),
        crayons.red('pipenv check'),
        crayons.red('pipenv run pip freeze'),
    )
    help = help.replace('Commands:', additional_help)
    return help
