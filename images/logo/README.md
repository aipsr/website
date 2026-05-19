# REDES-IA logo working kit

This folder contains editable logo materials for continuing the REDES-IA identity work and integrating the mark into the website.

## Concept

The logo uses a moving bridge as the central symbol. The bridge connects an organic cluster of dots on the left with a smaller, uneven grid of squares on the right.

- Bridge: transition to AI, with movement rather than a perfectly symmetrical arch.
- Dots: society, research network, plural knowledge, collaboration.
- Squares: AI systems, data, governance, institutional design.
- Wordmark: `REDES` uses `#3C5D72`; `IA` uses `#6E9A86`.
- The dots and squares use flat colors only. The gradient is reserved for the bridge arch.

## Core sentence

Primary Spanish line:

`Políticas públicas para la transición a la IA`

Secondary English version:

`Public policy for the transition to AI`

Recommended use: keep only one descriptive line inside the logo. Longer institutional descriptions should be used in body copy, footers, or about sections rather than inside the logo lockup.

## Files

### SVG

- `svg/redes-ia-primary-horizontal.svg` — main Spanish horizontal lockup.
- `svg/redes-ia-horizontal-compact.svg` — horizontal version without tagline.
- `svg/redes-ia-stacked.svg` — smaller stacked Spanish version.
- `svg/redes-ia-secondary-english.svg` — English lockup.
- `svg/redes-ia-icon.svg` — icon/avatar version.
- `svg/redes-ia-favicon.svg` — simplified favicon/source icon.
- `svg/redes-ia-monochrome-black.svg` — one-color black version.
- `svg/redes-ia-reversed-dark.svg` — reversed version on carbon background.

### Web

- `web/RedesIALogo.tsx` — React/TypeScript component.
- `web/redes-ia-logo.css` — CSS custom properties.
- `web/palette.json` — palette tokens and usage roles.

### PNG

PNG exports are included when conversion is available. SVG should remain the source of truth.

## Color system

Primary text and institutional color:

- `#3C5D72` — REDES wordmark.

Secondary institutional color:

- `#6E9A86` — IA wordmark and some symbolic elements.

Arch gradient only:

- Start: `#527D8A`
- End: `#9DC4B6`

Dot/square palette:

- `#3C5D72`
- `#527D8A`
- `#6E9A86`
- `#9DC4B6`
- `#A8662A`
- `#B7655D`
- `#D9B24C`
- `#93B5C4`
- `#DCC1A9`
- `#D4998F`

Neutrals:

- Carbon: `#2B2B2B`
- Off-white: `#F4F6F8`

## Integration recommendation

Use SVG for the website header, footer, and static pages. Use the React component only if the website build system already supports React/TypeScript. Otherwise, inline the SVG or serve it as a static asset.

Suggested placements:

- Header desktop: `redes-ia-horizontal-compact.svg`
- Homepage hero: `redes-ia-primary-horizontal.svg`
- Footer: compact or monochrome variant
- Social avatar: `redes-ia-icon.svg`
- Favicon source: `redes-ia-favicon.svg`

## Design cautions

Do not add gradients to the dots or squares. Use the full palette in the dots and squares as flat colors. Keep the right-side grid sparse and uneven; too many squares make the mark look like generic tech branding. Preserve the asymmetry of the arch because it gives the logo movement and makes the transition concept clearer.
