#!/usr/bin/env python
"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: Words package

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""

from setuptools import setup, find_packages

setup(
    name = 'talkofeuropewords',
    description = 'Talk of Europe Creative Camp #2 - Wordcloud project - Scripts for extracting significant words',
    version = '0.1',
    install_requires = ['talkofeuropedb', 'python-dateutil', 'requests', 'textblob', 'ZODB', 'docopt', 'clint', 'unidecode'],
    author = 'Konstantin Tretyakov, Ilya Kuzovkin, Aleksandr Tkachenko',
    license = 'MIT',
    author_email = 'kt@ut.ee',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
          'autodetect_language = talkofeuropewords.scripts.autodetect_language:main',
          'compute_features = talkofeuropewords.scripts.compute_features:main',
          'collect_words = talkofeuropewords.scripts.collect_words:main',
          'extract_significant_features = talkofeuropewords.scripts.extract_significant_features:main',
         ]
    }
)
