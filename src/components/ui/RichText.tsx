import React from "react";

interface RichTextProps {
  text: string;
  className?: string;
  style?: React.CSSProperties;
}

/**
 * Renders text with support for **bold** markdown syntax and newline-to-block
 * conversion. Uses no dangerouslySetInnerHTML — all output is React elements.
 */
export function RichText({ text, className, style }: RichTextProps) {
  const lines = text.split("\n");

  return (
    <span className={className} style={style}>
      {lines.map((line, lineIdx) => (
        <span key={lineIdx} style={{ display: "block" }}>
          {parseBold(line)}
          {/* Preserve empty lines as visible spacing */}
          {line === "" && <br />}
        </span>
      ))}
    </span>
  );
}

/** Splits a single line on **bold** markers and returns React nodes. */
function parseBold(line: string): React.ReactNode[] {
  const parts = line.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, idx) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      const inner = part.slice(2, -2);
      return <strong key={idx}>{inner}</strong>;
    }
    return part;
  });
}
