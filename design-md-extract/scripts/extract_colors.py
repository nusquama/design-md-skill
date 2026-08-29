#!/usr/bin/env python3
"""Extract dominant colors from a local image via Pillow quantization.

Usage:
    python scripts/extract_colors.py <image-path> [--top 8]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("Missing Pillow. Install with: python3 -m pip install Pillow\n")
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('image', type=Path)
    ap.add_argument('--top', type=int, default=8)
    args = ap.parse_args()

    if not args.image.exists():
        sys.stderr.write(f"File not found: {args.image}\n")
        sys.exit(1)

    img = Image.open(args.image).convert('RGB')
    # quantize to a small palette then count
    pal = img.quantize(colors=args.top, method=Image.Quantize.MEDIANCUT)
    palette = pal.getpalette()
    counts = pal.getcolors()
    total = sum(c for c, _ in counts)
    ranked = sorted(((c, palette[i*3:i*3+3]) for c, i in counts), key=lambda x: -x[0])
    print(f"# Top {len(ranked)} colors from {args.image.name}")
    for c, (r, g, b) in ranked:
        print(f"#{r:02x}{g:02x}{b:02x}  {c/total*100:5.1f}%")


if __name__ == '__main__':
    main()
