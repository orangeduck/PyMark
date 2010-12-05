import argparse
import sys
import PyMark.Compiler

"""
This is mainly just a hook into the command line for args and setting up of the main compiler object.

All the real work happens in PyMark.Compiler, in the Compiler class.
"""

parser = argparse.ArgumentParser(description='Compile .py files using PyMark')
parser.add_argument('modules', metavar='M', nargs='*',help='A list of modules to compile')
parser.add_argument('-c','--constants',action="store_true",help='When given a list of modules to compile, PyMark will not by default recompile the constants file, as it would produce a file only containing constants of those modules chosen to be recompiled. This argument allows you to force the program to recompile the constants file.')
parser.add_argument('-w','--wipe',action="store_true",help='When given a list of modules to compile, PyMark will not by default clear the "Compiled" directory first. This argument allows you to force the program to clear it of existing .pm files before compile.')

args = parser.parse_args(sys.argv[1::])

compiler = PyMark.Compiler.Compiler()
compiler.run(args)
