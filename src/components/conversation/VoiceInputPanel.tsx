import React, {
  useState,
  useRef,
  useCallback,
  useEffect,
} from "react";
import { WAVEFORM_HEIGHTS } from "@/constants";

// ─── Types ──────────────────────────────────────────────────────────────────

type ListenState = "idle" | "listening" | "recognized";

interface VoiceInputPanelProps {
  /** Quick-select chip labels. Pass an empty array to hide the chips section. */
  options: string[];
  /** Called when the user commits an answer (chip, voice confirm, or text send). */
  onAnswer: (text: string) => void;
  disabled?: boolean;
  /** High-contrast mode — switches to black/white palette. */
  hc?: boolean;
  placeholder?: string;
  /** Show the "or" divider between chips and the voice section. Default true. */
  showOrDivider?: boolean;
}

// ─── Helper: section divider ─────────────────────────────────────────────────

function OrDivider({ hc }: { hc?: boolean }) {
  return (
    <div className="flex items-center gap-3 my-1">
      <div className={`flex-1 h-px ${hc ? "bg-black" : "bg-slate-200"}`} />
      <span
        className={`text-xs font-medium uppercase tracking-widest ${
          hc ? "text-black" : "text-slate-400"
        }`}
      >
        or
      </span>
      <div className={`flex-1 h-px ${hc ? "bg-black" : "bg-slate-200"}`} />
    </div>
  );
}

// ─── Helper: animated waveform ───────────────────────────────────────────────

function Waveform({ hc }: { hc?: boolean }) {
  return (
    <div className="flex items-end gap-[3px] h-10" aria-hidden="true">
      {WAVEFORM_HEIGHTS.map((h, i) => (
        <div
          key={i}
          className={`w-[3px] rounded-full origin-bottom ${
            hc ? "bg-black" : "bg-blue-500"
          }`}
          style={{
            height: `${h}px`,
            animation: `bar-wave 0.9s ease-in-out infinite`,
            animationDelay: `${(i * 0.9) / WAVEFORM_HEIGHTS.length}s`,
          }}
        />
      ))}
    </div>
  );
}

// ─── Mic SVG icon ────────────────────────────────────────────────────────────

function MicIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="9" y="2" width="6" height="12" rx="3" />
      <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
      <line x1="12" y1="19" x2="12" y2="22" />
      <line x1="8" y1="22" x2="16" y2="22" />
    </svg>
  );
}

// ─── Send SVG icon ───────────────────────────────────────────────────────────

function SendIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}

// ─── Main Component ──────────────────────────────────────────────────────────

export function VoiceInputPanel({
  options,
  onAnswer,
  disabled = false,
  hc = false,
  placeholder = "Type your answer…",
  showOrDivider = true,
}: VoiceInputPanelProps) {
  const [listenState, setListenState] = useState<ListenState>("idle");
  const [recognizedText, setRecognizedText] = useState("");
  const [textInput, setTextInput] = useState("");

  const listenTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // ── Voice simulation ──────────────────────────────────────────────────────

  const startListening = useCallback(() => {
    if (disabled) return;
    if (listenTimerRef.current !== null) clearTimeout(listenTimerRef.current);

    setListenState("listening");
    setRecognizedText("");

    listenTimerRef.current = setTimeout(() => {
      const captured = options.length > 0 ? options[0] : "Yes";
      setRecognizedText(captured);
      setListenState("recognized");
    }, 2600);
  }, [disabled, options]);

  const stopListening = useCallback(() => {
    if (listenTimerRef.current !== null) {
      clearTimeout(listenTimerRef.current);
      listenTimerRef.current = null;
    }
    setListenState("idle");
    setRecognizedText("");
  }, []);

  const confirmVoice = useCallback(() => {
    onAnswer(recognizedText);
    setListenState("idle");
    setRecognizedText("");
  }, [onAnswer, recognizedText]);

  const editVoice = useCallback(() => {
    setTextInput(recognizedText);
    setListenState("idle");
    setRecognizedText("");
    // Focus the text input after state settles
    requestAnimationFrame(() => {
      inputRef.current?.focus();
    });
  }, [recognizedText]);

  // ── Text submit ───────────────────────────────────────────────────────────

  const submitText = useCallback(() => {
    const trimmed = textInput.trim();
    if (!trimmed || disabled) return;
    onAnswer(trimmed);
    setTextInput("");
  }, [textInput, disabled, onAnswer]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        submitText();
      }
    },
    [submitText]
  );

  // ── Cleanup ───────────────────────────────────────────────────────────────

  useEffect(() => {
    return () => {
      if (listenTimerRef.current !== null) clearTimeout(listenTimerRef.current);
    };
  }, []);

  // ── Color tokens ──────────────────────────────────────────────────────────

  const chipBase = hc
    ? "border-2 border-black text-black hover:bg-black hover:text-white focus-visible:outline focus-visible:outline-2"
    : "border-2 border-blue-600 text-blue-700 hover:bg-blue-50 focus-visible:ring-2 focus-visible:ring-blue-500";

  const voiceIdleBase = hc
    ? "border-2 border-dashed border-black text-black hover:bg-black hover:text-white"
    : "border-2 border-dashed border-blue-400 text-blue-600 hover:bg-blue-50 hover:border-blue-500";

  // ─────────────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-3 w-full">
      {/* ── Section 1: Quick select chips ────────────────────────────────── */}
      {options.length > 0 && (
        <div className="flex flex-col gap-2">
          <p
            className={`text-xs font-semibold uppercase tracking-widest ${
              hc ? "text-black" : "text-slate-500"
            }`}
          >
            Quick select
          </p>
          <div className="flex flex-wrap gap-2">
            {options.map((opt) => (
              <button
                key={opt}
                type="button"
                disabled={disabled || listenState === "listening"}
                onClick={() => onAnswer(opt)}
                className={`
                  min-h-[44px] px-4 py-2 rounded-xl text-sm font-medium
                  transition-colors duration-150 cursor-pointer
                  disabled:opacity-50 disabled:cursor-not-allowed
                  ${chipBase}
                `}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Divider between chips and voice ──────────────────────────────── */}
      {options.length > 0 && showOrDivider && <OrDivider hc={hc} />}

      {/* ── Section 2: Voice input ────────────────────────────────────────── */}
      <div className="flex flex-col gap-2">
        <p
          className={`text-xs font-semibold uppercase tracking-widest ${
            hc ? "text-black" : "text-slate-500"
          }`}
        >
          Speak your answer
        </p>

        {listenState === "idle" && (
          <button
            type="button"
            disabled={disabled}
            onClick={startListening}
            className={`
              w-full flex items-center justify-center gap-2
              min-h-[52px] rounded-xl text-sm font-medium
              transition-colors duration-150
              disabled:opacity-50 disabled:cursor-not-allowed
              ${voiceIdleBase}
            `}
            aria-label="Start voice input"
          >
            <MicIcon className="w-5 h-5" />
            Tap to speak
          </button>
        )}

        {listenState === "listening" && (
          <div
            className={`
              w-full flex items-center justify-between gap-3
              min-h-[52px] px-4 rounded-xl
              ${hc ? "border-2 border-black bg-white" : "border-2 border-blue-400 bg-blue-50"}
            `}
          >
            <Waveform hc={hc} />
            <span
              className={`text-sm font-medium flex-1 text-center ${
                hc ? "text-black" : "text-blue-700"
              }`}
            >
              Listening…
            </span>
            <button
              type="button"
              onClick={stopListening}
              aria-label="Stop listening"
              className={`
                w-8 h-8 flex items-center justify-center rounded-full
                font-bold text-sm transition-colors
                ${
                  hc
                    ? "bg-black text-white hover:bg-slate-800"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }
              `}
            >
              ✕
            </button>
          </div>
        )}

        {listenState === "recognized" && (
          <div
            className={`
              w-full flex flex-col gap-2 p-4 rounded-xl
              ${
                hc
                  ? "border-2 border-black bg-white"
                  : "border border-green-200 bg-green-50"
              }
            `}
          >
            <p
              className={`text-sm font-medium ${
                hc ? "text-black" : "text-green-800"
              }`}
            >
              "{recognizedText}"
            </p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={confirmVoice}
                className={`
                  flex-1 min-h-[40px] rounded-lg text-sm font-semibold
                  transition-colors
                  ${
                    hc
                      ? "bg-black text-white hover:bg-slate-800"
                      : "bg-green-600 text-white hover:bg-green-700"
                  }
                `}
              >
                Use this answer
              </button>
              <button
                type="button"
                onClick={editVoice}
                className={`
                  flex-1 min-h-[40px] rounded-lg text-sm font-semibold
                  transition-colors
                  ${
                    hc
                      ? "border-2 border-black text-black hover:bg-black hover:text-white"
                      : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                  }
                `}
              >
                Edit
              </button>
              <button
                type="button"
                onClick={startListening}
                aria-label="Try again"
                className={`
                  w-10 h-10 flex items-center justify-center rounded-lg
                  transition-colors
                  ${
                    hc
                      ? "border-2 border-black text-black hover:bg-black hover:text-white"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }
                `}
              >
                <MicIcon className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* ── Divider between voice and text ───────────────────────────────── */}
      <OrDivider hc={hc} />

      {/* ── Section 3: Text input ─────────────────────────────────────────── */}
      <div className="flex gap-2 items-center">
        <input
          ref={inputRef}
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          aria-label={placeholder}
          className={`
            flex-1 h-11 px-4 rounded-xl text-sm
            border transition-colors duration-150
            disabled:opacity-50 disabled:cursor-not-allowed
            focus:outline-none
            ${
              hc
                ? "border-2 border-black text-black placeholder-slate-600 focus:ring-2 focus:ring-black"
                : "border-slate-300 text-slate-800 placeholder-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            }
          `}
        />
        <button
          type="button"
          disabled={disabled || textInput.trim() === ""}
          onClick={submitText}
          aria-label="Send"
          className={`
            w-11 h-11 flex items-center justify-center rounded-xl
            transition-colors duration-150
            disabled:opacity-40 disabled:cursor-not-allowed
            ${
              hc
                ? "bg-black text-white hover:bg-slate-800 disabled:bg-slate-400"
                : "bg-blue-600 text-white hover:bg-blue-700 disabled:bg-slate-200"
            }
          `}
        >
          <SendIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
