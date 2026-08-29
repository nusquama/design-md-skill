# design-md-skill

Hybrid skill that turns **any visual source** into the **same output pack as designlang** — adapted for images.

## Sources supported

| Source | Method |
|---|---|
| Live website URL / HTML | `npx designlang` (Playwright, computed DOM) — deterministic |
| Image / screenshot / mockup | k-means palette + vision LLM + typeface verification, then same emitters |
| Frontend codebase | theme files → CSS vars → component styles |
| Existing tokens / DESIGN.md | merge & enrich, never re-extract |

## Output pack (same as designlang)

Every run writes these files to `./design-extract-output/`:

| File | What it is |
|---|---|
| `*-design-language.md` | 19-section AI-optimized markdown — feed any LLM to recreate the design |
| `*-design-tokens.json` | W3C DTCG tokens (primitive + semantic + composite) |
| `*-tailwind.config.js` | Drop-in Tailwind theme |
| `*-shadcn-theme.css` | shadcn/ui globals.css variables |
| `*-figma-variables.json` | Figma Variables import (light + dark) |
| `*-variables.css` | CSS custom properties |
| `*-theme.js` | React / CSS-in-JS theme object |
| `*-preview.html` | Visual report: swatches, type scale, shadows, a11y score |
| `*-motion-tokens.json` | Durations, easings, springs |
| `*-voice.json` | Brand voice — tone, CTA verbs |
| `*-prompts/` | Paste-ready prompts for v0 / Lovable / Cursor / Claude Artifacts |
| `*-grade.html` | Shareable Design Report Card (letter grade + evidence) |
| `*-grade.svg` | Shields.io-style design-score badge |
| `brandbook.pdf` | 13-chapter brand book (optional, `--pdf`) |

## Install

```bash
npx skills add nusquama/design-md-skill
```

## Why hybrid

- Sites have real CSS → run designlang, don't guess it.
- Images have no CSS → infer, verify, mark confidence, then emit the **same files**.
- Every token carries a confidence level. Invented values are forbidden.
