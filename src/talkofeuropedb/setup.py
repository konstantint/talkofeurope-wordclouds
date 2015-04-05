#! /usr/bin/env python
"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: DB package

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""
from setuptools import setup, find_packages

setup(
    name='talkofeuropedb',
    description='Talk of Europe Creative Camp #2 - Wordcloud project - Scripts for downloading TalkOfEurope data and converting them into relational form',
    version='0.1',
    author='Konstantin Tretyakov, Ilya Kuzovkin, Aleksandr Tkachenko',
    license='MIT',
    author_email='kt@ut.ee',
    packages=find_packages(),
    install_requires=['docopt', 'SQLAlchemy', 'rdflib', 'requests', 'clint'],
    entry_points={
        'console_scripts': [
          'test_config = talkofeuropedb.config:test_config',
          'get_ttl = talkofeuropedb.scripts.get_ttl:main',
          'ttl2csv = talkofeuropedb.scripts.ttl2csv:main',
          'csv2db = talkofeuropedb.scripts.csv2db:main',
         ]
    }
)
