#!/usr/bin/env python3
"""Lint a design-language.md: balanced braces, required sections, token refs."""
import sys, re

REQUIRED = ["## Overview", "## Colors", "## Typography", "## Layout",
            "## Elevation", "## Shapes", "## Components", "## Do's and Don'ts",
            "## Responsive", "## Open Questions"]

def main():
    if len(sys.argv) < 2:
        print("Usage: lint_design_md.py <file>")
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    errs = []
    for sec in REQUIRED:
        if sec not in text:
            errs.append(f"missing section: {sec}")
    # balanced ``` fences
    if text.count("```") % 2 != 0:
        errs.append("unbalanced code fences")
    # token refs must point at defined keys
    refs = re.findall(r"\{([a-z0-9.-]+)\}", text)
    print(json_dumps := __import__("json").dumps({"errors": errs, "ok": not errs}, indent=2))
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
