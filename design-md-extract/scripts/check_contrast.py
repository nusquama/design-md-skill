#!/usr/bin/env python3
"""WCAG contrast check for key text/surface pairs."""
import sys, json

def lum(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055)**2.4
    g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055)**2.4
    b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055)**2.4
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast(a, b):
    la, lb = lum(a), lum(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)

def main():
    if len(sys.argv) < 3:
        print("Usage: check_contrast.py <fg-hex> <bg-hex>")
        sys.exit(1)
    fg, bg = sys.argv[1], sys.argv[2]
    c = contrast(fg, bg)
    print(json.dumps({"fg": fg, "bg": bg, "ratio": round(c, 2),
                      "AA": c >= 4.5, "AAA": c >= 7.0}, indent=2))

if __name__ == "__main__":
    main()
