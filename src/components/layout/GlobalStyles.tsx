import React from "react";

interface GlobalStylesProps {
  reduceMotion: boolean;
}

export function GlobalStyles({ reduceMotion }: GlobalStylesProps) {
  const css = `
/* ── Keyframe Animations ─────────────────────────────────────────────── */

@keyframes pulse-ring {
  0%   { transform: scale(1);    opacity: 0.6; }
  70%  { transform: scale(1.35); opacity: 0;   }
  100% { transform: scale(1.35); opacity: 0;   }
}

@keyframes pulse-ring-slow {
  0%   { transform: scale(1);    opacity: 0.4; }
  70%  { transform: scale(1.5);  opacity: 0;   }
  100% { transform: scale(1.5);  opacity: 0;   }
}

@keyframes pulse-ring-3 {
  0%   { transform: scale(1);    opacity: 0.25; }
  70%  { transform: scale(1.7);  opacity: 0;    }
  100% { transform: scale(1.7);  opacity: 0;    }
}

@keyframes dot-bounce {
  0%, 80%, 100% { transform: translateY(0);    opacity: 0.5; }
  40%            { transform: translateY(-6px); opacity: 1;   }
}

@keyframes glow-breathe {
  0%, 100% { box-shadow: 0 0 8px 2px rgba(99, 179, 237, 0.3); }
  50%       { box-shadow: 0 0 20px 6px rgba(99, 179, 237, 0.7); }
}

@keyframes bar-wave {
  0%, 100% { transform: scaleY(0.3); }
  50%       { transform: scaleY(1);   }
}

@keyframes speaker-wave {
  0%, 100% { opacity: 0.25; transform: scaleX(0.8); }
  50%       { opacity: 1;    transform: scaleX(1);   }
}

@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position:  400px 0; }
}

/* ── Reduce Motion Override ──────────────────────────────────────────── */

${
  reduceMotion
    ? `
*, *::before, *::after {
  animation-duration: 0.001ms !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.001ms !important;
}
`
    : ""
}

/* ── Utility: card hover elevation ──────────────────────────────────── */

.card-hover {
  transition: box-shadow 0.18s ease, transform 0.18s ease;
}
.card-hover:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* ── Utility: hide scrollbar ─────────────────────────────────────────── */

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* ── Utility: skeleton shimmer ───────────────────────────────────────── */

.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    rgba(226, 232, 240, 0.8) 25%,
    rgba(241, 245, 249, 0.9) 50%,
    rgba(226, 232, 240, 0.8) 75%
  );
  background-size: 800px 100%;
  animation: shimmer 1.6s infinite linear;
}
`;

  return <style dangerouslySetInnerHTML={{ __html: css }} />;
}
