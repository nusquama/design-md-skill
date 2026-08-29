# design-md-skill

Hybrid skill that turns **any visual source** into a complete, agent-ready `DESIGN.md`.

## Sources supported

| Source | Method |
|---|---|
| Live website URL | `npx designlang` (Playwright, computed DOM) — deterministic |
| HTML file | CSS variable extraction + computed styles |
| Image / screenshot / mockup | k-means palette + vision LLM + typeface verification |
| Frontend codebase | theme files → CSS vars → component styles |
| Existing tokens / DESIGN.md | merge & enrich, never re-extract |

## Output

- `DESIGN.md` — Google Stitch spec (YAML tokens + prose)
- `design-tokens.json` — W3C DTCG format
- `tokens.css` — CSS custom properties
- `design-a11y.md` — WCAG contrast report (when applicable)
- `design.html` — human-readable style guide mirror (optional)

## Install

```bash
npx skills add nusquama/design-md-skill
```

## Why hybrid

- Sites have real CSS → read it, don't guess it.
- Images have no CSS → infer, then verify, then mark confidence.
- Every token carries a confidence level. Invented values are forbidden.
