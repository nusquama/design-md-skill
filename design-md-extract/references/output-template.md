# Output Template — DESIGN.md

This is the **base** template. Adapt depth per emphasis (reconstruction / mood / system), but don't remove sections unless explicitly empty — in which case, say so.

The frontmatter is a subset of the companion `design-tokens.json` (DTCG). The YAML is the inline-readable shorthand; the JSON is the canonical machine source.

```markdown
---
version: alpha
name: [Site / file / reference name]
source: [the URL, file path, or image path analyzed]
captured_at: YYYY-MM-DD
description: |
  [2-3 sentence atmosphere paragraph.]

colors:
  primary: "#171717"
  surface: "#FFFFFF"
  text-primary: "#171717"
  text-muted: "#4D4D4D"
  border: "#EBEBEB"
  accent: "#10B981"

typography:
  display:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: 48px
    fontWeight: 600
    letterSpacing: -0.02em
  h1:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: 32px
    fontWeight: 600
  body:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  caption-mono:
    fontFamily: "Geist Mono, ui-monospace, monospace"
    fontSize: 12px
    fontWeight: 400

spacing:
  base: 4px
  scale: [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]

rounded:
  sm: 6px
  md: 8px
  lg: 12px
  pill: 9999px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: 10px 24px
  card:
    backgroundColor: "{colors.surface}"
    border: "1px solid {colors.border}"
    rounded: "{rounded.lg}"
    padding: 32px
---

# Design Analysis — [Site / file / reference name]

## Source
- **Source type**: [local image | URL | HTML | codebase | combination]
- **Path / URL**: `<the concrete source>`
- **Capture method**: [designlang | HTML+CSS vars | k-means+vision | Playwright]
- **Detected limitations**: [if any]

## TL;DR
[2-3 sentences. Visual personality + what's distinctive + one actionable insight.]

## 1. Visual identity
### 1.1 Surface description
**Personality** (3-5 adjectives): [...]
**Mood**: [...]
**Information density**: [minimalist | balanced | dense]
**Confidence**: [✅ | ⚠️ | ❓]

### 1.2 Brand voice / Atmosphere
[2-3 dense paragraphs: what does this design BELIEVE about its audience?]

### 1.3 The "ONE brand thing"
[The single element that carries the brand alone.]

## 2. Design System (tokens)
### 2.1 Colors — table: Token | Hex | Role | Where | Confidence
### 2.2 Typography — detected family + observed scale table
### 2.3 Spacing — inferred base unit + observable multiples
### 2.4 Radii
### 2.5 Elevation system — Levels 0-N with treatment + use
### 2.6 Borders
### 2.7 Accessibility quick-check

## 3. Components Inventory
### 3.1 Generic components (Button, Input, Card, ...)
### 3.2 Signature components (brand-unique)

## 4. Layout & Composition
### 4.1 Grid & containers
### 4.2 Composition patterns
### 4.3 Responsive behavior — breakpoints table, touch targets, collapsing strategy
### 4.4 Image behavior

## 5. Reconstruction Notes
Suggested stack, quick wins, tricky bits, implicit states, confidence map.

## 6. Do's and Don'ts
5-7 of each, each citing tokens explicitly. Brand-specific, not generic UX.

## 7. Open Questions
[Things you couldn't determine. Or: "Material sufficient for complete reconstruction."]

## 8. Companion files
- [ ] design-tokens.json (DTCG)
- [ ] tokens.css
- [ ] design-a11y.md
- [ ] design.html (optional)
```

### Confidence marker rules
- ✅ high: directly seen, without significant inference
- ⚠️ medium: well-grounded inference but could be wrong
- ❓ low: reasonable speculation, say so openly

### Token reference syntax in prose
Write the ref followed by the literal value in parens: `{colors.primary}` (#171717). This makes the file refactor-safe.
