#!/usr/bin/env python3
"""Extract CSS custom properties (--*) from a stylesheet or HTML file."""
import sys, re, json

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_colors.py <file>")
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    props = re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);", text)
    print(json.dumps({k.strip(): v.strip() for k, v in props}, indent=2))

if __name__ == "__main__":
    main()
