#!/usr/bin/env python
"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: Webapp package

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""
from setuptools import setup, find_packages

setup(
    name='talkofeuropeweb',
    description="Talk of Europe Creative Camp #2 - Wordcloud project - Visualization webapp",
    version='0.1',
    author='Konstantin Tretyakov, Ilya Kuzovkin, Aleksandr Tkachenko',
    license='MIT',
    author_email='kt@ut.ee',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=[
      "Flask", "Flask-SQLAlchemy", "Flask-Login", "Flask-WTF", "Flask-Mail", "Flask-Babel", "Flask-Admin", "docopt"
    ],
    entry_points={"console_scripts": ["talkofeurope-web = talkofeuropeweb:main"],
                  "paste.app_factory": ["main=talkofeuropeweb.main:app_factory"]
                  },
)
