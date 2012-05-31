
from distutils.core import setup

setup(name='PyMark',
      version='0.7.1',
      description='Python Flavoured Markup',
      author='Daniel Holden',
      author_email='contact@daniel-holden.com',
      url='https://github.com/orangeduck/PyMark',
      license="BSD",
      py_modules=['pymark'],
      scripts=['scripts/pymark'],
      data_files=[("Lib/pymark/doc", ["README.md", "LICENSE.md"]),
                  ("Lib/pymark/parsers", [
                   "parsers/PyMark.c",
                   "parsers/pymark.clj",
                   "parsers/PyMark.cpp",
                   "parsers/PyMark.h",
                   "parsers/PyMark.hpp",
                   "parsers/PyMark.hs",
                   "parsers/PyMarkObject.java"])]
    )
