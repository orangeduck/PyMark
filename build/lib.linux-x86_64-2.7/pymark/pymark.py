#!/usr/bin/env python

import os
import sys
import argparse

import packer

parser = argparse.ArgumentParser(description='Create PyMark binaries')
parser.add_argument('input', metavar='<input.py>', nargs=1, help='Input Python file')
parser.add_argument('output', metavar='<output.pm>', nargs=1, help='Output Binary file')

args = parser.parse_args()

input_path, input_file = os.path.split(args.input[0])
input_file = os.path.splitext(input_file)[0]

sys.path.append(input_path)

module = __import__(input_file, globals(), locals(), [], -1)

output_file = args.output[0]
output_obj = module.__dict__[input_file]
packer.pack_file(output_file, output_object)
