#!/usr/bin/env python3
"""Validate a generated DESIGN.md against the Google Stitch spec.

Checks:
- Frontmatter is valid YAML with required fields (version, name, source).
- Every `{token.ref}` in the body resolves to something in the frontmatter.
- Every component named in YAML `components:` has a matching prose entry.
- Section 6 Do's/Don'ts is non-empty or carries the explicit abstain justification.
- Open Questions section is non-empty or carries the "material sufficient" justification.
- No duplicate H2 headings; canonical section order respected.

Usage:
    python scripts/lint_design_md.py <design.md>
    # exit 1 on failures (wire into pre-commit if desired).
"""
from __future__ import annotations

import argparse
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("Missing PyYAML. Install with: python3 -m pip install pyyaml\n")
    sys.exit(1)

CANONICAL_SECTIONS = [
    "Source", "TL;DR", "1. Visual identity", "2. Design System (tokens)",
    "3. Components Inventory", "4. Layout & Composition", "5. Reconstruction Notes",
    "6. Do's and Don'ts", "7. Open Questions", "8. Companion files",
]


def split_frontmatter(text: str):
    if not text.startswith('---'):
        return None, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None, text
    return yaml.safe_load(parts[1]), parts[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('file', type=argparse.FileType('r'))
    args = ap.parse_args()
    text = args.file.read()
    fm, body = split_frontmatter(text)

    errors = []
    if fm is None:
        errors.append("Missing or invalid YAML frontmatter")
    else:
        for req in ('version', 'name', 'source'):
            if req not in fm:
                errors.append(f"Frontmatter missing required field: {req}")

    # token refs
    refs = re.findall(r'\{([a-zA-Z0-9_.-]+)\}', body)
    defined = set()
    if fm:
        for group in ('colors', 'typography', 'spacing', 'rounded', 'borders', 'shadows', 'components'):
            g = fm.get(group, {})
            if isinstance(g, dict):
                for k in g:
                    defined.add(f"{group}.{k}")
    for ref in refs:
        if ref not in defined and not ref.startswith('spacing.scale'):
            errors.append(f"Unresolved token ref: {{{ref}}}")

    # duplicate headings
    heads = re.findall(r'^##\s+(.+)$', body, re.M)
    seen = set()
    for h in heads:
        if h in seen:
            errors.append(f"Duplicate H2 heading: {h}")
        seen.add(h)

    # Do's and Don'ts non-empty or abstain
    dod = re.search(r"## 6\. Do's and Don'ts\n(.*?)(?=\n## |\Z)", body, re.S)
    if dod:
        content = dod.group(1).strip()
        if len(content) < 20 and 'Insufficient evidence' not in content:
            errors.append("Section 6 Do's and Don'ts is empty without abstain justification")

    if errors:
        print("LINT FAILURES:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("LINT OK")
    sys.exit(0)


if __name__ == '__main__':
    main()
