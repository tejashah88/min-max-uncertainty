import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'min-max-uncertainty',
    version = '1.0.0',
    author = 'Tejas Shah',
    author_email = 'tejashah88@gmail.com',
    description = 'A min/max uncertainty calculator and data cruncher, mainly used for my physics labs.',
    long_description=read('README.md'),
    license = 'MIT',
    keywords = 'uncertainty error propagation physics chemstry science data labs',
    url = 'https://github.com/tejashah88/min-max-uncertainty',
    py_modules=['minmax'],
    install_requires=['sympy', 'terminaltables']
)