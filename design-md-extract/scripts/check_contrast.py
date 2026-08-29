#!/usr/bin/env python3
"""WCAG 2.1 contrast checker for extracted color pairs.

Usage:
    python scripts/check_contrast.py --pair "#111827,#FFFFFF" --pair "#3B82F6,#FFFFFF"
"""
from __future__ import annotations

import argparse
import sys


def hex_to_rgb(h: str):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def rel_luminance(rgb):
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = rel_luminance(a), rel_luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--pair', action='append', required=True, help='hex1,hex2')
    args = ap.parse_args()
    print("| Pair | Ratio | AA normal | AA large | AAA normal | AAA large |")
    print("|---|---|---|---|---|---|")
    for p in args.pair:
        a, b = p.split(',')
        r = contrast(hex_to_rgb(a), hex_to_rgb(b))
        aa_n = '✅' if r >= 4.5 else '❌'
        aa_l = '✅' if r >= 3 else '❌'
        aaa_n = '✅' if r >= 7 else '❌'
        aaa_l = '✅' if r >= 4.5 else '❌'
        print(f"| {a} on {b} | {r:.2f}:1 | {aa_n} | {aa_l} | {aaa_n} | {aaa_l} |")


if __name__ == '__main__':
    main()
