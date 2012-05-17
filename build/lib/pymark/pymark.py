#!/usr/bin/env python

import os
import sys
import imp
import argparse

import pymark.packer

parser = argparse.ArgumentParser(description='Create PyMark binaries')
parser.add_argument('input', metavar='<input.py>', nargs=1, help='Input Python file')
parser.add_argument('output', metavar='<output.pmk>', nargs=1, help='Output Binary file')

args = parser.parse_args()

module = imp.load_source('__pymark__', args.input[0])
module_object = os.path.splitext(os.path.basename(args.input[0]))[0]

output_file = args.output[0]
output_object = module.__dict__[module_object]
packer.pack_file(output_file, output_object)
