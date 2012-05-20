#!/usr/bin/env python

from distutils.core import setup

setup(name='PyMark',
      version='0.6.7',
      description='Python Flavoured Markup',
      author='Daniel Holden',
      author_email='contact@daniel-holden.com',
      url='https://github.com/orangeduck/PyMark',
      packages=['pymark'],
      package_data={'pymark': ['parsers/*']},
      scripts=['scripts/pymark'],
      license="BSD",
      data_files=[("doc", ["README.md", "LICENSE.md"])]
    )
