# Analysis Framework

How to judge whether an extraction is complete enough for an agent to rebuild
the design without inventing anything.

## Confidence levels

- ✅ high — directly measured (computed CSS, or verified typeface render).
- ⚠️ medium — grounded inference, could be off by one step.
- ❓ low — reasonable speculation; say so openly.

## Completeness bar

An extraction passes when:

1. Every color has name + hex + role + confidence.
2. Typography covers Display, H1–H3, Body, Label, Caption — each with
   size/weight/line-height/tracking + confidence, and image-sourced sizes were
   verified against the chosen typeface.
3. Spacing scale is complete and monotonic; base unit stated.
4. Radius, border, shadow tokens present (or section marked TODO).
5. At least Buttons, Cards, Inputs documented with states.
6. Do's and Don'ts ≥4 items; Responsive section present.
7. All output-pack files emitted (or explicitly TODO).
8. `*-variables.css` contains zero hardcoded global literals — everything is
   `var()`.
9. Lint script returns zero errors.

## Failure modes

- **designlang unavailable** → fall back to HTML+CSS-var extraction; mark ⚠️.
- **Image too abstract** → emit pack with heavy ❓ marking; list Open Questions.
- **Proprietary font** → Google Fonts fallback + documented original.
- **Conflicting sources** → later wins; list in Conflicts.
