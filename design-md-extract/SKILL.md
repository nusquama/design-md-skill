---
name: design-md-extract
description: >-
  Extract a complete, agent-ready DESIGN.md from any source: live website URL,
  HTML file, image/screenshot/mockup, frontend codebase, or existing tokens.
  For websites it runs a deterministic extractor (designlang) on the rendered
  DOM; for images it infers tokens via k-means + vision LLM and verifies every
  font size against the chosen typeface. Output follows the Google Stitch
  DESIGN.md spec plus W3C DTCG tokens, CSS variables, and an optional HTML
  style-guide mirror. Use when the user says "extract the design", "create a
  design.md", "reverse-engineer this site's style", "clone this look", or
  provides a URL/HTML/image and wants a reusable design document.
---

# design-md-extract

Turn any visual source into a **DESIGN.md** — a self-contained design system
document that any AI agent can read to rebuild a site, page, or component with
zero invented styles. Every margin, padding, border, font size, color, and
spacing value is captured so the consuming agent never has to guess.

## Hard Constraints

- Always write the output file as `DESIGN.md` (or the path the user gives).
- Always include the YAML frontmatter with typed tokens; never emit prose-only.
- Always emit exact hex values for every color, never color names alone.
- Always give every color a descriptive name AND a functional role.
- Always resolve token references (show both `{colors.primary}` and the hex).
- Always preserve original token names exactly, including typos — note them, don't "fix" them.
- Never fabricate a value. If data is missing, mark the section `> TODO: [what is missing]`.
- Never invent a font size from an image without verifying it against the chosen typeface's metrics.
- Always run the validation checklist (and the lint script when available) before delivering.
- Always confirm with the user (summary + missing sections) before writing the final file, unless they said "just do it" / "auto".
- Keep this SKILL.md under 500 lines. Put long examples and templates in `references/`.

## What a DESIGN.md Is

A DESIGN.md has two parts:

1. **YAML frontmatter** (between `---` lines) — machine-readable tokens: colors, typography, spacing, rounded, components. Agents and tools parse this.
2. **Markdown body** — human-readable rationale: atmosphere, do's and don'ts, component guidance. Agents read this for intent.

Official spec: https://github.com/google-labs-code/design.md/blob/main/docs/spec.md
Community examples: https://github.com/voltagent/awesome-design-md

## Input Detection

Decide the source type, then follow the matching branch:

| Input | Branch |
|---|---|
| URL (`https://...`) | `website` |
| `.html` / `.htm` file | `html` |
| Image / screenshot / mockup (png, jpg, webp, pdf) | `image` |
| Frontend codebase (folder with `package.json`, `*.css`, components) | `codebase` |
| Existing `DESIGN.md` / `tokens.json` / `tailwind.config.*` | `tokens` (merge/enrich, don't re-extract) |

If multiple inputs are given, extract each and merge — later sources override earlier ones on conflict, and conflicts are listed in a `## Conflicts` note.

---

## Branch A — Website / HTML (deterministic)

Goal: read the **rendered** styles, not just the source. Source CSS lies; computed styles tell the truth.

1. **Run the extractor** on the provided URL (preferred) or HTML file:

```bash
npx designlang <url> --screenshots
# multi-page:
npx designlang <url> --depth 3 --screenshots
# dark mode:
npx designlang <url> --dark --screenshots
```

If `designlang` is unavailable, fall back to the agent's own tools: fetch the HTML, resolve every `<link rel=stylesheet>`, extract CSS custom properties (`--*`) with `python scripts/extract_css_vars.py`, and capture a screenshot at 1440×900 (and 375×812) via Playwright only when the raw HTML is empty (SPA without SSR).

2. Read the generated `*-design-language.md`, `*-design-tokens.json`, and `*-variables.css`.
3. Map the extracted tokens into the schema (Branch D). Tokens coming from CSS variables get ✅ high confidence by default.
4. Spot-check a few components against the screenshot to confirm the extractor didn't miss visual-only details (e.g. a shadow the CSS didn't declare).
5. Run `npx @google/design.md lint DESIGN.md` (or `python scripts/lint_design_md.py`) and fix every error before delivering.

## Branch B — Image / Screenshot (infer, then verify)

Goal: infer the system, then **verify** it. Images are lossy — an 18px font in a screenshot may actually be 16px or 20px in the real typeface. Never trust a raw pixel measurement alone.

1. Describe the overall atmosphere in 1–2 sentences (density, mood, temperature).
2. **Palette (deterministic):** run `python3 scripts/quantize_palette.py <image> --k 12 --no-crop`. Filter out pure grays (unless UI surfaces), photographic content colors, and near-duplicates (Δhex < 8/channel). Map survivors to semantic names: `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`, `success`, `warning`, `info`.
3. **Typography (vision + verification):** identify the typeface by visual signature. Pick the closest web font, then **verify**: render sample text at the guessed size and compare letter-spacing, x-height, and weight against the image. Adjust the size up or down until the rendered text matches. Record the final verified size and mark confidence (✅/⚠️/❓). If the font is proprietary, emit the Google Fonts fallback as `fontFamily` and document the original in prose.
4. **Spacing:** measure gaps against a reference (body font size), snap to a 4px or 8px base, record both measured and snapped values.
5. **Radius / borders / shadows:** compare to known scales, pick the closest, note confidence.
6. Run the same validation checklist as Branch A. Mark low-confidence values with `> TODO: verify`.

## Branch C — Codebase

1. Detect stack from `package.json` / config files.
2. Read, in priority order: theme/token files → `tailwind.config.*` → global CSS / CSS variables → component styles → inline styles.
3. Theme files beat component styles. CSS custom properties are intentional tokens — respect them.
4. Map into the token schema.

## Branch D — Token Mapping (all branches converge here)

Build the YAML frontmatter. Use these groups:

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
  display:
    fontFamily: <font>
    fontSize: <px>
    fontWeight: <number>
    lineHeight: <number or dimension>
    letterSpacing: <dimension>
  h1: { fontFamily, fontSize, fontWeight, lineHeight, letterSpacing }
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
    fontFamily: "{typography.label-lg.fontFamily}"
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
- Token references use `{path.to.token}` and must point to primitives (except inside `components`, where composite refs are allowed).
- Every color token value is a valid CSS color; hex `#RRGGBB` is the default.
- `fontWeight` is numeric. `lineHeight` is unitless (multiplier) when possible.
- `spacing` scale uses named levels: `xs sm md lg xl 2xl 3xl` plus semantic keys (`gutter`, `margin`).
- Component variants get their own keys: `button-primary`, `button-primary-hover`, `button-primary-active`.
- Every important inference carries a confidence level (✅ high / ⚠️ medium / ❓ low). In the prose, write the ref then the literal: `{colors.primary}` (#171717).

---

## Companion outputs (always emit when data allows)

1. **`design-tokens.json`** — W3C DTCG format (`$value` / `$type` / `$description` / `$extensions.confidence`). This is the canonical machine-readable source; the YAML frontmatter is the inline shorthand.
2. **`tokens.css`** — every token as a CSS custom property in `:root` (`--color-primary`, `--text-h1-size`, `--rounded-md`, `--space-lg`, ...). Generated from the same token map so the HTML agent can `var()` everything.
3. **`design-a11y.md`** — WCAG 2.1 contrast report for key text/surface pairs (run `python scripts/check_contrast.py`).
4. **`design.html`** (optional) — self-contained, token-driven style guide mirroring the `.md`, for the human to read.

## Markdown Body (required sections, in order)

## Overview
2–3 sentences: visual character, intended product, key conventions.

## Colors
List every color as a bullet: `**Name (#hex):** role`. Group: Primary Foundation, Accent & Interactive, Typography & Text Hierarchy, Functional States, Surfaces. Include dark-mode variants if detected. Cite confidence per token.

## Typography
- Font families with character description (geometric vs humanist, serif vs sans) + Google Fonts fallback if proprietary.
- Full hierarchy table: Display, H1–H3, Body (lg/md/sm), Label, Caption — each with size, weight, line-height, letter-spacing, confidence.
- Rules: max two weights per screen, when to use uppercase labels, number styling.

## Layout
- Grid model and max content width.
- Spacing scale and the base unit (4px or 8px).
- Container padding, section gaps, card internal padding.
- Breakpoints.

## Elevation & Depth
Flat (borders/tonal layers) or shadowed. List each shadow level with its CSS string and which components use it. Note decorative depth (gradients, polarity flips) separately.

## Shapes
Corner radius language in words + tokens. Border widths.

## Components
For each relevant atom — Buttons, Chips, Inputs, Cards, Lists, Nav, Tooltips, Checkboxes, Radios — give: variants, sizing, padding, radius, colors, states (default/hover/active/focus/disabled), transitions.

## Do's and Don'ts
4–8 guardrails, each specific to this design and citing tokens. E.g. "Do use primary only for the single most important action per screen." "Don't mix rounded and sharp corners in one view."

## Responsive Behavior
Breakpoints, stacking rules, touch-target minimum (44px), what collapses and how.

## Open Questions
What couldn't be determined and what needs human input. If none, justify why.

## Agent Prompt Guide
A ready-to-paste instruction block the consuming agent can use, e.g.:

> Build a landing page using this DESIGN.md. Use `{colors.primary}` for the hero CTA, `{typography.h1}` for the headline, `{spacing.lg}` section padding, and `{rounded.lg}` cards. Never invent colors or spacing — every value is defined above.

## Conflicts (only if merging sources)
List any value that differed between sources and which one won.

---

## Validation Checklist (run before delivering)

- [ ] YAML frontmatter parses; every `{ref}` resolves to a defined primitive.
- [ ] Every color has name + hex + role; near-duplicates consolidated.
- [ ] Typography covers Display, H1–H3, Body, Label, Caption with size/weight/line-height/tracking + confidence.
- [ ] Spacing scale is complete and monotonic; base unit stated.
- [ ] Radius + border + shadow tokens present (or section marked TODO).
- [ ] At least Buttons, Cards, Inputs documented with states.
- [ ] Do's and Don'ts has ≥4 items; Responsive section present; Open Questions present (or justified).
- [ ] Image-sourced sizes were verified against the chosen typeface (Branch B).
- [ ] No fabricated values; every gap is a `TODO`.
- [ ] `npx @google/design.md lint DESIGN.md` (or lint script) returns zero errors.
- [ ] Document reads as intent + tokens, not a raw CSS dump.

---

## Output

Write `DESIGN.md` to the path the user gave (default: project root), plus `design-tokens.json`, `tokens.css`, and `design-a11y.md` when data allows. Then show:
1. A one-line summary (colors count, type levels, spacing steps).
2. The sections included vs marked TODO.
3. The validation result.

If the user asked for more (Tailwind config, shadcn theme, Figma variables), emit those as sibling files using the same tokens — but the canonical deliverable is always `DESIGN.md`.

## When NOT to Use

- The user wants a finished website, not a design document → use a build skill.
- The source is a video or 3D model → out of scope.
