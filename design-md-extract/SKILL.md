---
name: design-md-extract
description: >-
  Extracts a complete, agent-ready design.md from any website URL, HTML file,
  image, screenshot, or frontend codebase (React, Vue, Svelte, Angular, plain
  HTML/CSS, Tailwind). Produces a DESIGN.md with YAML design tokens (colors,
  typography, spacing, rounded, components) plus prose sections so any agent can
  rebuild the site without inventing styles. Use when the user says "extract the
  design", "create a design.md", "reverse-engineer this site's style", "clone
  this look", "design system from this image", or provides a URL/HTML/image and
  wants a reusable design document.
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
- Always run the validation checklist before delivering.
- Always confirm with the user (summary + missing sections) before writing the final file, unless they said "just do it" / "auto".
- Keep this SKILL.md under 500 lines. Put long examples in `references/`.

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

## Branch A — Website / HTML

Goal: read the **rendered** styles, not just the source. Source CSS lies; computed styles tell the truth.

1. If a URL: fetch the page. Prefer a headless browser (Playwright) to get the fully rendered DOM + computed styles. If only `curl`/fetch is available, parse the raw HTML/CSS and note that computed values may differ.
2. Collect stylesheets: `<link rel=stylesheet>`, inline `<style>`, and any CSS-in-JS runtime styles.
3. For the key elements (hero, nav, buttons, cards, inputs, headings, body), record **computed** values:
   - `color`, `background-color`, `border-color`, `border-width`, `border-radius`
   - `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`
   - `padding`, `margin`, `gap`, `width`, `max-width`
   - `box-shadow`, `opacity`, `transition`
4. Detect the framework from signals (`data-reactroot`, `ng-version`, `data-v-`, Tailwind utility classes, etc.) and read its theme config if present (`tailwind.config.*`, CSS variables on `:root`).
5. Map everything into the token schema (Branch D).

## Branch B — Image / Screenshot

Goal: infer the system, then **verify** it. Images are lossy — an 18px font in a screenshot may actually be 16px or 20px in the real typeface. Never trust a raw pixel measurement alone.

1. Describe the overall atmosphere in 1–2 sentences (density, mood, temperature).
2. Sample the dominant colors with a color picker / histogram. Group into primary, secondary, tertiary, neutral, surfaces, text, borders, functional states.
3. Identify the typeface by visual signature (geometric sans, humanist sans, serif, mono). Pick the closest available web font. **Then verify**: render sample text at the guessed size and compare letter-spacing, x-height, and weight against the image. Adjust the size up or down until the rendered text matches the image's proportions. Record the final verified size.
4. Measure spacing by comparing element gaps to a reference (e.g., the body font size). Snap to a scale (4px or 8px base). Record both the measured value and the snapped token.
5. For borders/radius: compare corner curvature to known scales (`rounded-sm` 4px, `md` 8px, `lg` 12px, `full`). Pick the closest and note confidence.
6. Shadows: classify flat / whisper / soft / heavy and record the CSS `box-shadow` string that best reproduces it.
7. Run the same validation checklist as Branch A. Mark low-confidence values with `> TODO: verify`.

## Branch C — Codebase

1. Detect stack from `package.json` / config files (React, Vue, Svelte, Angular, Tailwind, styled-components, CSS-in-JS, plain CSS).
2. Read, in priority order: theme/token files → `tailwind.config.*` → global CSS / CSS variables → component styles → inline styles.
3. Theme files beat component styles: a `theme.ts` declares intent; scattered inline styles show what shipped. Extract from the theme first, spot-check components for overrides.
4. CSS custom properties (`--brand-primary`) are intentional tokens — respect them.
5. Map into the token schema.

## Branch D — Token Mapping (all branches converge here)

Build the YAML frontmatter. Use these groups:

```yaml
---
version: alpha
name: <project or descriptive name>
description: <one line>
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
  button-primary-hover:
    backgroundColor: "{colors.primary-dark}"
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
- Token references use `{path.to.token}` and must point to primitives (except inside `components`, where composite refs like `{typography.label-lg}` are allowed).
- Every color token value is a valid CSS color; hex `#RRGGBB` is the default.
- `fontWeight` is numeric. `lineHeight` is unitless (multiplier) when possible.
- `spacing` scale uses named levels: `xs sm md lg xl 2xl 3xl` plus semantic keys (`gutter`, `margin`).
- Component variants get their own keys: `button-primary`, `button-primary-hover`, `button-primary-active`.

---

## Markdown Body (required sections, in order)

## Overview
2–3 sentences: visual character, intended product, key conventions. E.g. "A focused, minimal dark interface for a developer tool. Clean lines, low visual noise, high information density."

## Colors
List every color as a bullet: `**Name (#hex):** role`. Group: Primary Foundation, Accent & Interactive, Typography & Text Hierarchy, Functional States (success/error/warning/info), Surfaces. Include dark-mode variants if detected.

## Typography
- Font families with character description (geometric vs humanist, serif vs sans).
- Full hierarchy table: Display, H1–H3, Body (lg/md/sm), Label, Caption — each with size, weight, line-height, letter-spacing.
- Rules: max two weights per screen, when to use uppercase labels, number styling.

## Layout
- Grid model (fluid / fixed-max-width / hybrid) and max content width.
- Spacing scale and the base unit (4px or 8px).
- Container padding, section gaps, card internal padding.
- Breakpoints: `sm 640, md 768, lg 1024, xl 1280, 2xl 1536` (Tailwind defaults) or the project's actual ones.

## Elevation & Depth
Flat (borders/tonal layers) or shadowed. List each shadow level with its CSS string and which components use it. Note z-index scale if present.

## Shapes
Corner radius language in words + tokens. E.g. "Architectural sharpness: 4px on all interactive elements." Border widths.

## Components
For each relevant atom — Buttons, Chips, Inputs, Cards, Lists, Nav, Tooltips, Checkboxes, Radios — give: variants, sizing, padding, radius, colors, states (default/hover/active/focus/disabled), transitions.

## Do's and Don'ts
4–8 guardrails. E.g. "Do use primary only for the single most important action per screen." "Don't mix rounded and sharp corners in one view." "Do maintain WCAG AA (4.5:1 normal text)."

## Responsive Behavior
Breakpoints, stacking rules, touch-target minimum (44px), what collapses and how.

## Agent Prompt Guide
A ready-to-paste instruction block the consuming agent can use, e.g.:

> Build a landing page using this DESIGN.md. Use `{colors.primary}` for the hero CTA, `{typography.h1}` for the headline, `{spacing.lg}` section padding, and `{rounded.lg}` cards. Never invent colors or spacing — every value is defined above.

## Conflicts (only if merging sources)
List any value that differed between sources and which one won.

---

## Validation Checklist (run before delivering)

- [ ] YAML frontmatter parses; every `{ref}` resolves to a defined primitive.
- [ ] Every color has name + hex + role; near-duplicates consolidated.
- [ ] Typography covers Display, H1–H3, Body, Label, Caption with size/weight/line-height/tracking.
- [ ] Spacing scale is complete and monotonic; base unit stated.
- [ ] Radius + border + shadow tokens present (or section marked TODO).
- [ ] At least Buttons, Cards, Inputs documented with states.
- [ ] Do's and Don'ts has ≥4 items; Responsive section present.
- [ ] Image-sourced sizes were verified against the chosen typeface (Branch B).
- [ ] No fabricated values; every gap is a `TODO`.
- [ ] Document reads as intent + tokens, not a raw CSS dump.

---

## Output

Write `DESIGN.md` to the path the user gave (default: project root). Then show:
1. A one-line summary (colors count, type levels, spacing steps).
2. The sections included vs marked TODO.
3. The validation result.

If the user asked for more (Tailwind config, shadcn theme, Figma variables, DTCG `tokens.json`), emit those as sibling files using the same tokens — but the canonical deliverable is always `DESIGN.md`.

## When NOT to Use

- The user wants a finished website, not a design document → use a build skill.
- The user wants brand guidelines for a known company → point them to awesome-design-md.
- The source is a video or 3D model → out of scope.
