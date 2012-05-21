#!/usr/bin/env python

import os
import sys
import imp
import argparse

import pymark.packer

parser = argparse.ArgumentParser(description='Create PyMark binaries')
parser.add_argument('module', nargs=1, help='Input Python file')
parser.add_argument('output', nargs=1, help='Output PyMark file')

args = parser.parse_args()

module = imp.load_source('__pymark__', args.module[0])
module_object = os.path.splitext(os.path.basename(args.module[0]))[0]

output_dict = module.__dict__
del output_dict["__builtins__"]

pymark.packer.pack_file(args.output[0], output_dict)


