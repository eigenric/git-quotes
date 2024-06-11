import io
import re

from setuptools import setup, find_packages

with io.open('quotes/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
        name="git-quotes",
        description="Add beautiful quotes to your commits automatically",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/eigenric/git-quotes",
        author="Ricardo Ruiz Fernández de Albas",
        author_email="ricardoruizfdez@gmail.com",
        license='MIT',
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Version Control :: Git',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
        ],
        python_requires=">=3.8, <3.13",
        version=version,
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
