# Token Extraction — designlang parity

This reference defines how tokens are produced for each branch, so every
emitter (DTCG, Tailwind, shadcn, Figma, CSS, theme.js) consumes the **same**
map.

## Common token groups

```yaml
colors:        primary, secondary, tertiary, neutral, surface, on-surface,
               error, success, warning, info (+ dark variants)
typography:    display, h1, h2, h3, body-lg, body-md, body-sm, label-lg,
               label-sm, caption
spacing:       base, xs, sm, md, lg, xl, 2xl, 3xl, gutter
rounded:       none, sm, md, lg, xl, full
borders:       thin, thick
shadows:       sm, md, lg
components:    button-primary, button-primary-hover, button-primary-active,
               card, input, nav, ...
```

## Branch A — Website (designlang)

1. Run `npx designlang <url> [--screenshots] [--dark] [--depth N] [--pdf]`.
2. Read `*-design-tokens.json` (DTCG) and `*-variables.css` directly — these
   ARE the canonical map. Do not re-derive.
3. Confidence: ✅ for every token coming from computed CSS. ⚠️ only for
   visual-only details the CSS didn't declare (e.g. a shadow).

## Branch B — Image (infer + verify)

1. **Palette:** `python3 scripts/quantize_palette.py <image> --k 12 --no-crop`.
   Filter grays/photographic/near-duplicates. Map to semantic names.
2. **Typography:** identify typeface by visual signature → pick closest web
   font → **verify** by rendering sample text at guessed size and comparing
   x-height, letter-spacing, weight to the image. Adjust until match. Record
   final size + confidence.
3. **Spacing:** measure gaps vs body font size, snap to 4px/8px base.
4. **Radius / borders / shadows:** compare to known scales, pick closest.
5. Emit the same DTCG + CSS + Tailwind + shadcn + Figma + theme.js + preview
   from this map. Mark ⚠️/❓ on every inferred value.

## Branch C — Codebase

Priority: theme/token files → `tailwind.config.*` → global CSS vars →
component styles → inline styles. CSS custom properties are intentional
tokens — respect them.

## Branch D — Merge

Later sources override earlier ones. List conflicts in `## Conflicts`.

## Emitter rules (all branches)

- `*-variables.css`: every global value is a `var()` — no hardcoded literals for
  colors, spacing, radii, type sizes. This is what makes "change H1 size →
  updates everywhere" true.
- `*-tailwind.config.js`: `theme.extend` wired to the same tokens.
- `*-shadcn-theme.css`: shadcn globals.css format.
- `*-figma-variables.json`: light + dark.
- `*-theme.js`: React/CSS-in-JS object.
- `*-design-tokens.json`: DTCG with `$value` / `$type` / `$description` /
  `$extensions.confidence`.
