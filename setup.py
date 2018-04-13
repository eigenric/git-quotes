from setuptools import setup, find_packages

setup(
        name="git-quotes",
        version="0.1",
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'click',
            'crayons',
        ],
        entry_points='''
            [console_scripts]
            git-quotes=quotes.git_quotes:cli
        ''',
        data_files=[
            ('hooks', ['quotes/hooks/prepare-commit-msg']),
            ('hooks', ['quotes/hooks/quotes.json'])
        ]
)
