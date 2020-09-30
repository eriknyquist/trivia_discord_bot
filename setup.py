import unittest
import os
from setuptools import setup

from trivia_discord_bot import __version__

HERE = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(HERE, "README.rst")

with open(README, 'r') as f:
    long_description = f.read()

setup(
    name='trivia_discord_bot',
    version=__version__,
    description=('A discord bot for group trivia questions'),
    long_description=long_description,
    url='http://github.com/eriknyquist/trivia_discord_bot',
    author='Erik Nyquist',
    author_email='eknyquist@gmail.com',
    license='Apache 2.0',
    packages=['trivia_discord_bot'],
    include_package_data=True,
    zip_safe=False
)
