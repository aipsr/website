import React from "react";

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
