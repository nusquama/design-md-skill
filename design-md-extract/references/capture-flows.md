# Capture Flows — How to capture each source type

## Flow 1 — Local image
1. The image is available via multimodal vision. No script needed.
2. If you need pixel-precise hex codes, run `python scripts/extract_colors.py <image-path>` (Pillow quantization) or `python3 scripts/quantize_palette.py <image> --k 12` (k-means).
3. Move to analysis.

**When to ask for more:** image too small/low-res → ask for a better version. Only part of something visible → ask for other sections.

## Flow 2 — Website URL
**Strategy: HTML first, CSS variables second, screenshot only if needed.**

### 2.1 Fetch the HTML
Use WebFetch. Review for signs of real content:
- ✅ Good HTML (blogs, static landings, SSR): visible text, descriptive classes, semantic structure, linked stylesheets.
- ❌ Empty HTML (pure React/Vue SPA): `<body>` nearly empty → Playwright screenshot needed.

### 2.2 If HTML is sufficient
Look for framework signals (`bg-blue-500` = Tailwind, `MuiButton-root` = MUI, etc.), inline `<style>` with `--*: value;`, linked stylesheets, meta tags.

### 2.2.bis — CSS variables extraction (the gold)
CSS custom properties are the site's explicit token system. Extract them:

```bash
python scripts/extract_css_vars.py <URL> --output ./css-vars.json
```

They go into `design-tokens.json` with ✅ high confidence. Cite the source stylesheet URL.

### 2.3 If HTML is empty: on-demand Playwright
```bash
python scripts/capture_site.py <URL> --output ./capture.png
python scripts/capture_site.py <URL> --viewports desktop,tablet,mobile
```
Default sizes: 1440×900, 768×1024, 375×812. Warn the user the first run downloads ~300MB of Chromium.

## Flow 3 — Figma link (optional)
Requires Figma MCP. Order: `get_metadata` → `get_variable_defs` (gold: explicit tokens) → `get_design_context` → `get_screenshot`.

## Flow 4 — Combinations
URL + manual screenshot: HTML+CSS vars for structure/tokens, screenshot for visual presentation. Cite both sources.

## Error handling
| Error | What to do |
|---|---|
| URL 403/404 | Tell user, offer alternatives (manual screenshot, archive.org) |
| Cloudflare/captcha | Tell honestly. Don't bypass. Request manual screenshot. |
| Playwright not installed | Give install command. Don't workaround. |
| Corrupt image | Ask for a new version. |

**Principle:** honesty about limitations is part of being professional. An invented analysis is worse than an analysis with missing but clear data.
