# references/extraction-examples.md

Long worked examples for the agent. Read only when stuck.

## Example — extracting from a Tailwind site

Source signals:
- `tailwind.config.js` → `theme.extend.colors.brand = "#2665fd"`
- `globals.css` → `--radius: 0.5rem`
- Button component → `className="bg-brand text-white rounded-md px-5 py-2.5"`

Mapping:
```yaml
colors:
  primary: "#2665fd"   # from brand
rounded:
  md: 8px              # 0.5rem
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 10px 20px
```

## Example — image verification loop

Guessed H1 = 48px in Inter. Render "The quick brown fox" at 48px Inter and compare
to the screenshot. If the rendered x-height is taller than the image's, drop to 44px
and re-check. Record the first size where letter-spacing and cap-height match.

## Example — do's and don'ts

- Do use `{colors.primary}` for exactly one primary action per view.
- Don't mix `{rounded.sm}` and `{rounded.lg}` inside the same card.
- Do keep body text ≥ 16px (`{typography.body-md}`) for readability.
- Don't use more than two font weights on a single screen.
- Do maintain 4.5:1 contrast for normal text (WCAG AA).
