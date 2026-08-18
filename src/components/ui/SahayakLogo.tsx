import React from "react";

interface SahayakLogoProps {
  size?: number;
}

export function SahayakLogo({ size = 34 }: SahayakLogoProps) {
  const id = "sahayak-logo";
  const gradBgId = `${id}-bg-grad`;
  const gradDotId = `${id}-dot-grad`;
  const r = size * 0.22; // corner radius: ~22% of size

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 34 34"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Sahayak logo"
      role="img"
    >
      <defs>
        {/* Navy-to-teal background gradient */}
        <linearGradient id={gradBgId} x1="0" y1="0" x2="34" y2="34" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#1a2e5a" />
          <stop offset="100%" stopColor="#0d9488" />
        </linearGradient>
        {/* Gradient for the three AI dots */}
        <linearGradient id={gradDotId} x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#7dd3fc" />
          <stop offset="100%" stopColor="#5eead4" />
        </linearGradient>
      </defs>

      {/* Rounded square background */}
      <rect
        width="34"
        height="34"
        rx={r}
        ry={r}
        fill={`url(#${gradBgId})`}
      />

      {/* Speech bubble body */}
      <path
        d="M6 8.5C6 7.12 7.12 6 8.5 6H25.5C26.88 6 28 7.12 28 8.5V20C28 21.38 26.88 22.5 25.5 22.5H13L8.5 27.5V22.5H8.5C7.12 22.5 6 21.38 6 20V8.5Z"
        fill="white"
        opacity="0.97"
      />

      {/* Three gradient dots — AI chat indicator */}
      <circle cx="12.5" cy="14.25" r="2" fill={`url(#${gradDotId})`} />
      <circle cx="17"   cy="14.25" r="2" fill={`url(#${gradDotId})`} />
      <circle cx="21.5" cy="14.25" r="2" fill={`url(#${gradDotId})`} />
    </svg>
  );
}
