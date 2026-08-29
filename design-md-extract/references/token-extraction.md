# Token Extraction — How to infer tokens with rigor

## Philosophy

**Token = named, reusable design decision.** A color is not a token; `primary = #3B82F6` with a semantic role is. Your job is to **infer the system** the designer used, not list loose values.

Three principles:
1. **Look for repetition.** If a value appears once, it's not a token. If it appears three or more times, it probably is.
2. **Infer semantic roles, not just numeric scales.** "Dark blue color" is worse than "primary".
3. **Mark confidence honestly.** If unsure about the role, say so.

## Color tokens
1. Identify unique colors with precise hex codes.
2. Group by family (all blues, all grays).
3. Assign semantic role based on where they appear:
   - CTA buttons, primary links → `primary`
   - Page backgrounds → `surface` / `background`
   - Card backgrounds → `surface-elevated`
   - Main text → `text-primary`
   - Secondary text → `text-muted`
   - Subtle borders → `border`
   - Success / warning / error → `success` / `warning` / `error`
4. Detect scale if 3+ tints of the same color are used systematically.

## Typography tokens
Identify family in order of reliability:
1. CSS accessible → ✅ certainty.
2. Visually recognized → ⚠️ medium. Say "looks like Inter".
3. Unrecognized → describe it ("geometric sans with open apertures").

Infer scale from most common measurements:
- Display: 48-72px · H1: 32-48px · H2: 24-32px · H3: 18-24px · Body: 14-16px · Caption: 11-12px

Report only weights actually seen. Don't assume 300-900 if you only saw 400 and 600.

Watch for: negative tracking on large headings (-0.02em), generous body line-height (1.5-1.7), tight heading line-height (1.1-1.2).

## Spacing tokens
Infer base unit from distances: 4px (fine-grained), 8px (classic), 16px (simple marketing).
Report observable multiples, not the entire possible scale.

## Radius tokens
none: 0 · sm: 4px · md: 8px · lg: 12px · xl: 16px · 2xl: 24px · full: 9999px

## Shadow tokens
shadow-sm / md / lg / xl with qualitative intensity. Report exact CSS only when inferable.

## Output: design-tokens.json (DTCG)

```json
{
  "color": {
    "primary": { "$value": "#3B82F6", "$type": "color", "$description": "Primary action", "$extensions": { "confidence": "high" } }
  },
  "typography": {
    "font-size": {
      "body": { "$value": "16px", "$type": "dimension" },
      "h1": { "$value": "48px", "$type": "dimension" }
    }
  },
  "spacing": {
    "1": { "$value": "4px", "$type": "dimension" },
    "4": { "$value": "16px", "$type": "dimension" }
  },
  "radius": {
    "sm": { "$value": "6px", "$type": "dimension" }
  }
}
```

- `$value` holds the concrete value. `$type` is canonical (`color`, `dimension`, `fontFamily`, ...).
- `$extensions.confidence` carries the skill-specific metadata without breaking spec compliance.
- **Only generate this file if you extracted real tokens.** If the source was ambiguous, don't invent the JSON.

## Golden rule
> A short and honest system is better than a long and invented one.
