# Analysis Framework — The layers

Analysis goes **from general to specific**. Don't skip layers.

## Layer 1 — Visual identity
**Guiding question:** What does this design want to be?
- Personality (3-5 adjectives), stylistic references, mood, information density, implicit positioning.
- Brand voice: 2-3 dense paragraphs answering what the design BELIEVES about its audience.
- The "ONE brand thing": the single element that carries the brand alone. If you can't identify it, say so — don't invent.

## Layer 2 — System (tokens)
Measure, don't just feel. Every observed token documented with its concrete value + confidence.
- Colors, typography, spacing, radii, elevation (Levels 0-N), borders, accessibility signals.
- Decorative depth (gradients, polarity flips, patterns) documented separately from UI elevation.

## Layer 3 — Components
Inventory visible components with variants and states. Split into:
- **Generic** (Button, Input, Card, Badge, Modal) — standard primitives.
- **Signature** (brand-unique) — "if you see this, you know which product this is".
Don't invent variants. If you only saw one button, say "1 variant observed".

## Layer 4 — Layout and composition
- Grid & containers, composition patterns, responsive behavior (breakpoints table, touch targets ≥44px, collapsing strategy), image behavior.
- If only desktop captured, populate breakpoints with ❓ low confidence and recommend re-running with multi-viewport capture.

## Layer 5 — Reconstruction
Prescriptive: suggested stack, quick wins, tricky bits, implicit states, confidence map.

## Layer 6 — Brand rules (Do's and Don'ts)
5-7 of each, each specific to this design and citing tokens. Brand-specific, not generic UX. If insufficient evidence, abstain explicitly — don't pad.

## Art Direction Patterns — QA pass (non-negotiable)
After Layers 1-6, run this checklist:
- [ ] Polarity-flipped section bands?
- [ ] Atmospheric gradient scoping (hero-only)?
- [ ] Density alternation (minimalist zones ↔ dense zones)?
- [ ] Pill scale coexistence (two radii deliberately)?
- [ ] Mono usage scope?
- [ ] Weight ceiling on display type?
- [ ] Tracking discipline?
- [ ] Color "voltage" (exactly ONE chromatic moment)?
- [ ] Stacked vs single-drop shadows?
- [ ] Split-hero vs centered-hero?
- [ ] Asymmetric whitespace?

If a pattern is present → document it (and consider a Section 6 rule). If absent → confirm you're confident in the absence, don't just "not see it".
