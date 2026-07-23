from pathlib import Path

OUT = Path('/mnt/data/redes-ia-logo-kit')
SVG = OUT/'svg'
PNG = OUT/'png'

colors = {
    'redes':'#3C5D72',
    'ia':'#6E9A86',
    'arch1':'#527D8A',
    'arch2':'#9DC4B6',
    'carbon':'#2B2B2B',
    'off':'#F4F6F8',
}
palette = ['#3C5D72','#527D8A','#6E9A86','#9DC4B6','#A8662A','#B7655D','#D9B24C','#93B5C4','#DCC1A9','#D4998F']

font = "Inter, Aptos, Avenir Next, Helvetica Neue, Arial, sans-serif"

def defs():
    return f'''<defs>
    <linearGradient id="archGradient" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{colors['arch1']}"/>
      <stop offset="100%" stop-color="{colors['arch2']}"/>
    </linearGradient>
  </defs>'''

def bridge_mark(x=0,y=0,scale=1,mono=False,reverse=False):
    # Asymmetric arch, left lower and heavier, right lighter. Gradient only on arch.
    arch_color = 'white' if reverse else ('#000000' if mono else 'url(#archGradient)')
    line_color = 'white' if reverse else ('#000000' if mono else '#93B5C4')
    dot_cols = ['white']*10 if reverse else (['#000000']*10 if mono else palette)
    sq_cols = ['white']*7 if reverse else (['#000000']*7 if mono else ['#3C5D72','#6E9A86','#B7655D','#527D8A','#D9B24C','#DCC1A9','#93B5C4'])
    # left dots, uneven, social/network
    dots = [(0,48,8),(20,20,6),(30,62,5),(48,38,9),(68,12,7),(82,55,5),(98,28,6),(112,48,7),(134,14,5),(145,70,4)]
    # fewer and uneven squares on right
    squares = [(470,20,12),(510,36,14),(552,16,10),(494,72,15),(540,84,12),(582,60,11),(620,88,9)]
    parts=[]
    parts.append(f'<g transform="translate({x} {y}) scale({scale})">')
    for i,(cx,cy,r) in enumerate(dots):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{dot_cols[i%len(dot_cols)]}"/>')
    # arch cubic curve
    parts.append(f'<path d="M170 86 C250 -10 415 -4 635 80" fill="none" stroke="{arch_color}" stroke-width="16" stroke-linecap="round"/>')
    # vertical bridge lines: fade lighter via opacity, not color gradient; okay these are arch support lines, not dots/squares.
    for idx,xx in enumerate([245,285,325,365,405,445,485,525,565]):
        top = 36 + abs(405-xx)/12
        op = max(0.18, 0.62 - idx*0.04)
        parts.append(f'<line x1="{xx}" y1="{top:.1f}" x2="{xx}" y2="110" stroke="{line_color}" stroke-width="2" opacity="{op:.2f}"/>')
    for i,(sx,sy,s) in enumerate(squares):
        parts.append(f'<rect x="{sx}" y="{sy}" width="{s}" height="{s}" rx="2.5" fill="{sq_cols[i%len(sq_cols)]}"/>')
    parts.append('</g>')
    return '\n'.join(parts)

def wordmark(x=0,y=0,scale=1,reverse=False,with_tagline=True,english=False):
    redes = 'white' if reverse else colors['redes']
    ia = 'white' if reverse else colors['ia']
    tagline_color = 'white' if reverse else colors['carbon']
    tagline = 'Public policy for the transition to AI' if english else 'Políticas públicas para la transición a la IA'
    parts=[f'<g transform="translate({x} {y}) scale({scale})">']
    parts.append(f'<text x="0" y="0" font-family="{font}" font-size="86" font-weight="700" letter-spacing="12" fill="{redes}">REDES-</text>')
    parts.append(f'<text x="484" y="0" font-family="{font}" font-size="86" font-weight="700" letter-spacing="8" fill="{ia}">IA</text>')
    if with_tagline:
        parts.append(f'<line x1="0" y1="34" x2="650" y2="34" stroke="{colors['ia'] if not reverse else 'white'}" stroke-width="2"/>')
        parts.append(f'<text x="325" y="78" text-anchor="middle" font-family="{font}" font-size="30" font-weight="400" fill="{tagline_color}">{tagline}</text>')
    parts.append('</g>')
    return '\n'.join(parts)

def svg_wrap(w,h,content,bg=None):
    bgrect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
  <title id="title">REDES-IA logo</title>
  <desc id="desc">Bridge logo for REDES-IA, connecting social research dots with AI governance squares.</desc>
  {defs()}
  {bgrect}
  {content}
</svg>\n'''

# Primary horizontal
content = bridge_mark(75,30,1.0) + wordmark(88,255,1.0,with_tagline=True)
(SVG/'redes-ia-primary-horizontal.svg').write_text(svg_wrap(820,395,content), encoding='utf-8')
# Spanish no tagline compact
content = bridge_mark(65,35,0.78) + wordmark(80,225,0.78,with_tagline=False)
(SVG/'redes-ia-horizontal-compact.svg').write_text(svg_wrap(680,285,content), encoding='utf-8')
# Stacked
content = bridge_mark(38,30,0.65) + wordmark(50,190,0.68,with_tagline=True)
(SVG/'redes-ia-stacked.svg').write_text(svg_wrap(540,330,content), encoding='utf-8')
# English secondary
content = bridge_mark(75,30,1.0) + wordmark(88,255,1.0,with_tagline=True,english=True)
(SVG/'redes-ia-secondary-english.svg').write_text(svg_wrap(820,395,content), encoding='utf-8')
# Icon/avatar
content = f'<circle cx="160" cy="160" r="148" fill="none" stroke="{colors['ia']}" stroke-width="4" opacity="0.95"/>' + bridge_mark(48,86,0.36)
(SVG/'redes-ia-icon.svg').write_text(svg_wrap(320,320,content), encoding='utf-8')
# monochrome
content = bridge_mark(75,30,1.0,mono=True) + wordmark(88,255,1.0,with_tagline=True)
# override wordmark colors? It uses color. For true mono easier replace colors after
mono_svg = svg_wrap(820,395,content).replace(colors['redes'],'#000000').replace(colors['ia'],'#000000').replace(colors['carbon'],'#000000').replace('url(#archGradient)','#000000')
(SVG/'redes-ia-monochrome-black.svg').write_text(mono_svg, encoding='utf-8')
# reverse
content = bridge_mark(75,30,1.0,reverse=True) + wordmark(88,255,1.0,reverse=True,with_tagline=True)
(SVG/'redes-ia-reversed-dark.svg').write_text(svg_wrap(820,395,content,bg=colors['carbon']), encoding='utf-8')
# favicon simple no circle bg transparent
content = bridge_mark(25,72,0.42)
(SVG/'redes-ia-favicon.svg').write_text(svg_wrap(320,220,content), encoding='utf-8')

# React component
react = r'''import React from "react";

export type RedesIALogoVariant = "primary" | "compact" | "icon" | "english";

type Props = {
  variant?: RedesIALogoVariant;
  className?: string;
  title?: string;
};

const palette = {
  redes: "#3C5D72",
  ia: "#6E9A86",
  archStart: "#527D8A",
  archEnd: "#9DC4B6",
  carbon: "#2B2B2B",
  support: "#93B5C4",
  dots: ["#3C5D72", "#527D8A", "#6E9A86", "#9DC4B6", "#A8662A", "#B7655D", "#D9B24C", "#93B5C4", "#DCC1A9", "#D4998F"],
  squares: ["#3C5D72", "#6E9A86", "#B7655D", "#527D8A", "#D9B24C", "#DCC1A9", "#93B5C4"],
};

function Mark({ scale = 1, x = 0, y = 0 }: { scale?: number; x?: number; y?: number }) {
  const dots = [[0,48,8],[20,20,6],[30,62,5],[48,38,9],[68,12,7],[82,55,5],[98,28,6],[112,48,7],[134,14,5],[145,70,4]];
  const squares = [[470,20,12],[510,36,14],[552,16,10],[494,72,15],[540,84,12],[582,60,11],[620,88,9]];
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`}>
      {dots.map(([cx, cy, r], i) => <circle key={i} cx={cx} cy={cy} r={r} fill={palette.dots[i]} />)}
      <path d="M170 86 C250 -10 415 -4 635 80" fill="none" stroke="url(#redes-ia-arch-gradient)" strokeWidth="16" strokeLinecap="round" />
      {[245,285,325,365,405,445,485,525,565].map((xx, i) => {
        const top = 36 + Math.abs(405 - xx) / 12;
        const opacity = Math.max(0.18, 0.62 - i * 0.04);
        return <line key={xx} x1={xx} y1={top} x2={xx} y2={110} stroke={palette.support} strokeWidth="2" opacity={opacity} />;
      })}
      {squares.map(([sx, sy, s], i) => <rect key={i} x={sx} y={sy} width={s} height={s} rx="2.5" fill={palette.squares[i]} />)}
    </g>
  );
}

export default function RedesIALogo({ variant = "primary", className, title = "REDES-IA" }: Props) {
  const english = variant === "english";
  const icon = variant === "icon";
  const compact = variant === "compact";
  const tagline = english ? "Public policy for the transition to AI" : "Políticas públicas para la transición a la IA";

  if (icon) {
    return (
      <svg className={className} viewBox="0 0 320 320" role="img" aria-label={title} xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="redes-ia-arch-gradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stopColor={palette.archStart}/><stop offset="100%" stopColor={palette.archEnd}/></linearGradient></defs>
        <circle cx="160" cy="160" r="148" fill="none" stroke={palette.ia} strokeWidth="4" opacity="0.95" />
        <Mark x={48} y={86} scale={0.36} />
      </svg>
    );
  }

  return (
    <svg className={className} viewBox="0 0 820 395" role="img" aria-label={title} xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="redes-ia-arch-gradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stopColor={palette.archStart}/><stop offset="100%" stopColor={palette.archEnd}/></linearGradient></defs>
      <Mark x={75} y={30} />
      <text x="88" y="255" fontFamily="Inter, Aptos, Avenir Next, Helvetica Neue, Arial, sans-serif" fontSize="86" fontWeight="700" letterSpacing="12" fill={palette.redes}>REDES-</text>
      <text x="572" y="255" fontFamily="Inter, Aptos, Avenir Next, Helvetica Neue, Arial, sans-serif" fontSize="86" fontWeight="700" letterSpacing="8" fill={palette.ia}>IA</text>
      {!compact && <>
        <line x1="88" y1="289" x2="738" y2="289" stroke={palette.ia} strokeWidth="2" />
        <text x="413" y="333" textAnchor="middle" fontFamily="Inter, Aptos, Avenir Next, Helvetica Neue, Arial, sans-serif" fontSize="30" fontWeight="400" fill={palette.carbon}>{tagline}</text>
      </>}
    </svg>
  );
}
'''
(OUT/'web'/'RedesIALogo.tsx').write_text(react, encoding='utf-8')

# README
readme = '''# REDES-IA logo working kit

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
'''
(OUT/'README.md').write_text(readme, encoding='utf-8')
