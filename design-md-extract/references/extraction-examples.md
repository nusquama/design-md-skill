# Extraction Examples

## Website (designlang)

```bash
npx designlang https://stripe.com --screenshots
# → ./design-extract-output/stripe-com-design-language.md
# → ./design-extract-output/stripe-com-design-tokens.json
# → ./design-extract-output/stripe-com-variables.css
# → ./design-extract-output/stripe-com-tailwind.config.js
# → ./design-extract-output/stripe-com-shadcn-theme.css
# → ./design-extract-output/stripe-com-figma-variables.json
# → ./design-extract-output/stripe-com-theme.js
# → ./design-extract-output/stripe-com-preview.html
```

## Image (infer + verify + emit)

```bash
python3 scripts/quantize_palette.py mockup.png --k 12 --no-crop
# agent verifies typeface, then writes the same 12+ files from the inferred map
```
