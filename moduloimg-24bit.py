#!/usr/bin/env python3
import itertools
import argparse
import io
import struct
from PIL import Image

parser = argparse.ArgumentParser(
    prog="moduloimg-24bit",
    description="Plots f(n, m) % c in the form of 24-bit RGB images"
)

parser.add_argument("expression", type=str)
parser.add_argument("constant", type=int)
parser.add_argument("--resolution", type=int)
parser.add_argument("filename", type=str)
args = parser.parse_args()

args.resolution = args.resolution or args.constant

expression = f"({args.expression}) % {args.constant}"
start = itertools.product(range(1, args.resolution + 1), range(1, args.resolution + 1))

mapped = [eval(expression) for (n, m) in start]
packed = [struct.pack('<I', i) for i in mapped]
byted = b''.join(packed)
b = io.BytesIO(bytes(byted)).read()

image = Image.frombytes("RGBX", (args.resolution, args.resolution), b, "raw")
image.convert('RGB').save(args.filename)
