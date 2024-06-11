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

with io.open("README.rst", encoding="utf-8") as readme:
    long_description = readme.read()


setup(
        name="git-quotes",
        description="Add beautiful quotes to your commits automatically",
        long_description=long_description,
        url="https://github.com/pwaqo/git-quotes",
        author="Ricardo Ruiz",
        author_email="ricardoruizfdez@gmail.com",
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Version Control :: Git',
            'License :: OSI Approved :: MIT License',
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
