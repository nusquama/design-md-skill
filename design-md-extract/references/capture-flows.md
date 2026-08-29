# Capture Flows

## Website / HTML

```bash
# default
npx designlang <url> --screenshots
# multi-page
npx designlang <url> --depth 3 --screenshots
# dark mode
npx designlang <url> --dark --screenshots
# brand book PDF
npx designlang <url> --pdf
# full pack
npx designlang <url> --full
```

Output lands in `./design-extract-output/`.

If `designlang` is missing: `npm install -g designlang`.

## Image / Screenshot

```bash
python3 scripts/quantize_palette.py <image> --k 12 --no-crop
python3 scripts/check_contrast.py <image>   # optional a11y pass
```

Then the agent writes the full output pack from the inferred token map.

## Codebase

Detect stack → read theme files → CSS vars → component styles → emit pack.
