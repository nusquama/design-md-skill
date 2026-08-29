---
name: design-md-extract
description: >-
  Extract a complete design system from any source — live website URL, HTML file,
  image/screenshot/mockup, frontend codebase, or existing tokens — and emit the
  SAME output pack as designlang (design-language.md, DTCG tokens, Tailwind config,
  shadcn theme, Figma variables, CSS variables, React theme, preview HTML, motion
  tokens, brand voice, prompt pack, grade card, optional brandbook PDF). For
  websites it runs the deterministic extractor `npx designlang`; for images it
  infers tokens via k-means + vision LLM, verifies every font size against the
  chosen typeface, then runs the same emitters. Use when the user says "extract
  the design", "create a design.md", "reverse-engineer this site's style",
  "clone this look", or provides a URL/HTML/image and wants a reusable design
  document.
---

# design-md-extract

Turn any visual source into the **full designlang output pack** — the same files
a `npx designlang <url>` run produces — so any AI agent can rebuild a site,
page, or component with zero invented styles. Every margin, padding, border, font
size, color, and spacing value is captured.

## Hard Constraints

- Always emit the **same file set as designlang** (see Output Pack below). Never
  reduce it to a single DESIGN.md.
- For websites: ALWAYS run `npx designlang` — never re-extract CSS by hand.
- For images: infer, then **verify**, then emit the same files with confidence
  markers.
- Always give every color a descriptive name AND a functional role.
- Never fabricate a value. If data is missing, mark it and still emit the file.
- Never invent a font size from an image without verifying it against the chosen
  typeface's metrics.
- Always run the validation checklist before delivering.
- Keep this SKILL.md under 500 lines. Put long templates in `references/`.

## Input Detection

| Input | Branch |
|---|---|
| URL (`https://...`) | `website` → designlang |
| `.html` / `.htm` file | `html` → designlang (file mode) |
| Image / screenshot / mockup (png, jpg, webp, pdf) | `image` → infer + verify + emit |
| Frontend codebase (folder with `package.json`, `*.css`, components) | `codebase` |
| Existing `DESIGN.md` / `tokens.json` / `tailwind.config.*` | `tokens` (merge/enrich) |

If multiple inputs are given, extract each and merge — later sources override
earlier ones on conflict, listed in a `## Conflicts` note.

---

## Branch A — Website / HTML (deterministic)

Goal: read the **rendered** styles, not just the source. Source CSS lies;
computed styles tell the truth.

1. **Run the extractor**:

```bash
npx designlang <url> --screenshots
# multi-page:
npx designlang <url> --depth 3 --screenshots
# dark mode:
npx designlang <url> --dark --screenshots
# brand book PDF:
npx designlang <url> --pdf
```

If `designlang` is unavailable, install it: `npm install -g designlang`, or fall
back to fetching the HTML, resolving every `<link rel=stylesheet>`, extracting
CSS custom properties, and capturing screenshots at 1440×900 and 375×812 via
Playwright.

2. Read the generated files in `./design-extract-output/`.
3. Spot-check a few components against the screenshot to confirm nothing visual
   was missed.
4. Run `python scripts/lint_design_md.py` and fix every error before delivering.

## Branch B — Image / Screenshot (infer, then verify, then emit)

Goal: infer the system, verify it, then produce the **same output pack** as
designlang. Images are lossy — an 18px font in a screenshot may actually be 16px
or 20px in the real typeface. Never trust a raw pixel measurement alone.

1. Describe the overall atmosphere in 1–2 sentences (density, mood, temperature).
2. **Palette (deterministic):** run
   `python3 scripts/quantize_palette.py <image> --k 12 --no-crop`. Filter out
   pure grays (unless UI surfaces), photographic content colors, and
   near-duplicates (Δhex < 8/channel). Map survivors to semantic names:
   `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`,
   `error`, `success`, `warning`, `info`.
3. **Typography (vision + verification):** identify the typeface by visual
   signature. Pick the closest web font, then **verify**: render sample text at
   the guessed size and compare letter-spacing, x-height, and weight against the
   image. Adjust the size up or down until the rendered text matches. Record the
   final verified size and mark confidence (✅/⚠️/❓). If the font is proprietary,
   emit the Google Fonts fallback as `fontFamily` and document the original in
   prose.
4. **Spacing:** measure gaps against a reference (body font size), snap to a 4px
   or 8px base, record both measured and snapped values.
5. **Radius / borders / shadows:** compare to known scales, pick the closest,
   note confidence.
6. **Emit the same pack** as Branch A: write `*-design-language.md`,
   `*-design-tokens.json`, `*-variables.css`, `*-tailwind.config.js`,
   `*-shadcn-theme.css`, `*-figma-variables.json`, `*-theme.js`,
   `*-preview.html`, `*-motion-tokens.json`, `*-voice.json`, `*-prompts/`,
   `*-grade.html`, `*-grade.svg`. Use the inferred tokens; mark every
   low-confidence value with ⚠️/❓ in the markdown and JSON.
7. Run the same validation checklist as Branch A.

## Branch C — Codebase

1. Detect stack from `package.json` / config files.
2. Read, in priority order: theme/token files → `tailwind.config.*` → global
   CSS / CSS variables → component styles → inline styles.
3. Theme files beat component styles. CSS custom properties are intentional
   tokens — respect them.
4. Emit the same output pack.

## Branch D — Token Mapping (all branches converge here)

Build the canonical token map (consumed by every emitter). Use these groups:

```yaml
---
version: alpha
name: <project or descriptive name>
description: <one line>
source: <url | file | image path>
captured_at: <YYYY-MM-DD>
colors:
  primary: "#..."
  secondary: "#..."
  tertiary: "#..."
  neutral: "#..."
  surface: "#..."
  on-surface: "#..."
  error: "#..."
  success: "#..."
  warning: "#..."
  info: "#..."
typography:
  display: { fontFamily, fontSize, fontWeight, lineHeight, letterSpacing }
  h1: { ... }
  h2: { ... }
  h3: { ... }
  body-lg: { ... }
  body-md: { ... }
  body-sm: { ... }
  label-lg: { ... }
  label-sm: { ... }
  caption: { ... }
spacing:
  base: 16px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  gutter: 24px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
borders:
  thin: 1px
  thick: 2px
shadows:
  sm: "0 1px 2px rgba(0,0,0,0.05)"
  md: "0 4px 12px rgba(0,0,0,0.08)"
  lg: "0 12px 32px rgba(0,0,0,0.12)"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    shadow: "{shadows.sm}"
  input:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    borderWidth: "{borders.thin}"
    rounded: "{rounded.sm}"
    padding: 10px 12px
---
```

Rules:
- Token references use `{path.to.token}` and must point to primitives (except
  inside `components`, where composite refs are allowed).
- Every color token value is a valid CSS color; hex `#RRGGBB` is the default.
- `fontWeight` is numeric. `lineHeight` is unitless (multiplier) when possible.
- `spacing` scale uses named levels: `xs sm md lg xl 2xl 3xl` plus semantic keys
  (`gutter`, `margin`).
- Component variants get their own keys: `button-primary`,
  `button-primary-hover`, `button-primary-active`.
- Every important inference carries a confidence level (✅ high / ⚠️ medium / ❓
  low). In the prose, write the ref then the literal: `{colors.primary}` (#171717).

---

## Output Pack (same as designlang)

Every run writes these files to `./design-extract-output/`:

| File | Purpose |
|------|---------|
| `*-design-language.md` | 19-section markdown — feed any LLM to recreate the design |
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

The `*-design-language.md` is the agent-readable spec (Google Stitch format).
The `*-variables.css` is what the HTML agent imports so every value is a
`var()` — changing `--color-primary` updates the whole site.

## Markdown Body (required sections, in order)

## Overview
2–3 sentences: visual character, intended product, key conventions.

## Colors
List every color as a bullet: `**Name (#hex):** role`. Group: Primary
Foundation, Accent & Interactive, Typography & Text Hierarchy, Functional
States, Surfaces. Include dark-mode variants if detected. Cite confidence per
token.

## Typography
- Font families with character description (geometric vs humanist, serif vs
  sans) + Google Fonts fallback if proprietary.
- Full hierarchy table: Display, H1–H3, Body (lg/md/sm), Label, Caption — each
  with size, weight, line-height, letter-spacing, confidence.
- Rules: max two weights per screen, when to use uppercase labels, number
  styling.

## Layout
- Grid model and max content width.
- Spacing scale and the base unit (4px or 8px).
- Container padding, section gaps, card internal padding.
- Breakpoints.

## Elevation & Depth
Flat (borders/tonal layers) or shadowed. List each shadow level with its CSS
string and which components use it. Note decorative depth (gradients, polarity
flips) separately.

## Shapes
Corner radius language in words + tokens. Border widths.

## Components
For each relevant atom — Buttons, Chips, Inputs, Cards, Lists, Nav, Tooltips,
Checkboxes, Radios — give: variants, sizing, padding, radius, colors, states
(default/hover/active/focus/disabled), transitions.

## Do's and Don'ts
4–8 guardrails, each specific to this design and citing tokens. E.g. "Do use
primary only for the single most important action per screen." "Don't mix
rounded and sharp corners in one view."

## Responsive Behavior
Breakpoints, stacking rules, touch-target minimum (44px), what collapses and how.

## Open Questions
What couldn't be determined and what needs human input. If none, justify why.

## Agent Prompt Guide
A ready-to-paste instruction block the consuming agent can use, e.g.:

> Build a landing page using this design. Use `{colors.primary}` for the hero
> CTA, `{typography.h1}` for the headline, `{spacing.lg}` section padding, and
> `{rounded.lg}` cards. Never invent colors or spacing — every value is defined
> above.

## Conflicts (only if merging sources)
List any value that differed between sources and which one won.

---

## Validation Checklist (run before delivering)

- [ ] All output-pack files present (or explicitly marked TODO).
- [ ] `*-design-language.md` parses; every `{ref}` resolves to a defined
  primitive.
- [ ] Every color has name + hex + role; near-duplicates consolidated.
- [ ] Typography covers Display, H1–H3, Body, Label, Caption with
  size/weight/line-height/tracking + confidence.
- [ ] Spacing scale is complete and monotonic; base unit stated.
- [ ] Radius + border + shadow tokens present (or section marked TODO).
- [ ] At least Buttons, Cards, Inputs documented with states.
- [ ] Do's and Don'ts has ≥4 items; Responsive section present; Open Questions
  present (or justified).
- [ ] Image-sourced sizes were verified against the chosen typeface (Branch B).
- [ ] No fabricated values; every gap is a `TODO`.
- [ ] `python scripts/lint_design_md.py` returns zero errors.
- [ ] Document reads as intent + tokens, not a raw CSS dump.
- [ ] `*-variables.css` uses only `var()` references for global values — no
  hardcoded literals for colors, spacing, radii, or type sizes.

---

## Output

Write the full pack to `./design-extract-output/` (or the path the user gave).
Then show:
1. A one-line summary (colors count, type levels, spacing steps, files emitted).
2. The sections included vs marked TODO.
3. The validation result.

## When NOT to Use

- The user wants a finished website, not a design document → use a build skill.
- The source is a video or 3D model → out of scope.
