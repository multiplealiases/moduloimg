#!/usr/bin/env python3
import itertools
import argparse
import io
import struct
from multiprocessing import Pool
from PIL import Image

parser = argparse.ArgumentParser(
    prog="moduloimg-24bit",
    description="Plots f(n, m) % c in the form of 24-bit RGB images"
)

parser.add_argument("expression", type=str)
parser.add_argument("constant", type=int)
parser.add_argument("-r", "--resolution", type=int, help="Resolution of the output image")
parser.add_argument("filename", type=str)
parser.add_argument("-n", type=int, help="offset of the horizontal axis (+ is left)")
parser.add_argument("-m", type=int, help="offset of the vertical axis (+ is down)")
args = parser.parse_args()

def e(n, m):
    return eval(expression)

args.resolution = args.resolution or args.constant
args.n = args.n or 0
args.m = args.m or 0

expression = f"({args.expression}) % {args.constant}"
start = itertools.product(range(1 + args.m, args.resolution + 1 + args.m), range(1 + args.n, args.resolution + 1 + args.n))
with Pool() as pool:
    mapped = pool.starmap(e, start)
packed = [struct.pack('<I', i) for i in mapped]
byted = b''.join(packed)
b = io.BytesIO(bytes(byted)).read()

image = Image.frombytes("RGBX", (args.resolution, args.resolution), b, "raw")
image.convert('RGB').save(args.filename)
