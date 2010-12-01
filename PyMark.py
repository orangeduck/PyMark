import argparse
import sys
from PyMark.Compiler import *

"""
This is mainly just a hook into the command line for args and setting up of the main compiler object.

All the real work happens in PyMark.Compiler, in the Compiler class.
"""

parser = argparse.ArgumentParser(description='Compile .py files using PyMark')
parser.add_argument('modules', metavar='M', nargs='*',help='A list of modules to compile')
parser.add_argument('-c','--constants',action="store_true",help='When given a list of modules to compile, PyMark will not by default recompile the constants file, as it would produce a file only containing constants of those modules chosen to be recompiled. This argument allows you to force the program to recompile the constants file.')

args = parser.parse_args(sys.argv[1::])

compiler = Compiler()
compiler.run(args)
