#!/usr/bin/env python3
import itertools
import argparse
import io
from PIL import Image

parser = argparse.ArgumentParser(
    prog="moduloimg",
    description="Plots f(n, m) % c in the form of 8-bit grayscale images"
)
parser.add_argument("expression", type=str)
parser.add_argument("constant", type=int)
parser.add_argument("filename", type=str)
args = parser.parse_args()

expression = f"({args.expression}) % {args.constant}"
start = itertools.product(range(1, args.constant + 1), range(1, args.constant + 1))

mapped = [eval(expression) for (n, m) in start]

b = io.BytesIO(bytearray(mapped)).read()

image = Image.frombytes("L", (args.constant, args.constant), b, "raw")
image.save(args.filename)
