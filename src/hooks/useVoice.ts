import { useState, useCallback, useEffect } from "react";
import type { VoiceState } from "@/types";
import { useSpeechRecognition } from "./useSpeechRecognition";
import { speak as ttsSpeak, stopSpeaking, isTTSSupported } from "@/services/speech";

export type { VoiceState };

interface UseVoiceOptions {
  /** Called when speech recognition completes with a final transcript */
  onListenEnd?: (transcript: string) => void;
  /** Called when TTS finishes speaking */
  onSpeakEnd?: () => void;
  /** BCP-47 language code for speech recognition (e.g., "en-IN", "kn-IN") */
  speechCode?: string;
}

interface UseVoiceReturn {
  state: VoiceState;
  transcript: string;
  startListening: () => void;
  stopListening: () => void;
  speak: (text: string) => void;
  /** True if speech recognition is supported in this browser */
  isSupported: boolean;
  /** Current error message, if any */
  error: string | null;
}

export function useVoice(options: UseVoiceOptions = {}): UseVoiceReturn {
  const {
    onListenEnd,
    onSpeakEnd,
    speechCode = "en-IN",
  } = options;

  const [state, setState] = useState<VoiceState>("idle");
  const [error, setError] = useState<string | null>(null);

  // Use real speech recognition hook
  const {
    transcript,
    isListening,
    isSupported,
    permissionState,
    startListening: startSTT,
    stopListening: stopSTT,
    resetTranscript,
    error: sttError,
  } = useSpeechRecognition();

  // ── Start listening ────────────────────────────────────────────────────────

  const startListening = useCallback(() => {
    setError(null);
    resetTranscript();
    setState("listening");

    startSTT(speechCode, (finalTranscript) => {
      // Called when speech recognition produces a final result
      if (finalTranscript.trim()) {
        setState("processing");
        // Small delay to show processing state before callback
        setTimeout(() => {
          setState("idle");
          onListenEnd?.(finalTranscript);
        }, 300);
      } else {
        // Empty transcript - just return to idle
        setState("idle");
      }
    });
  }, [speechCode, startSTT, onListenEnd, resetTranscript]);

  // ── Stop listening ─────────────────────────────────────────────────────────

  const stopListening = useCallback(() => {
    stopSTT();
    setState("idle");
    setError(null);
  }, [stopSTT]);

  // ── Speak (TTS) ────────────────────────────────────────────────────────────

  const speak = useCallback(
    (text: string) => {
      if (!text?.trim()) {
        onSpeakEnd?.();
        return;
      }

      if (!isTTSSupported()) {
        console.warn("[useVoice] TTS not supported in this browser");
        onSpeakEnd?.();
        return;
      }

      setState("speaking");

      ttsSpeak(
        text,
        speechCode,
        () => {
          // onEnd
          setState("idle");
          onSpeakEnd?.();
        },
        () => {
          // onStart
          setState("speaking");
        }
      );
    },
    [speechCode, onSpeakEnd]
  );

  // ── Sync state with speech recognition ─────────────────────────────────────

  useEffect(() => {
    if (!isListening && state === "listening") {
      // Recognition stopped but we're still in listening state
      // Check if there was an error
      if (sttError) {
        setState("idle");
        // Map STT errors to user-friendly messages
        switch (sttError) {
          case "UNSUPPORTED":
            setError("Voice input is not supported in this browser.");
            break;
          case "PERMISSION_DENIED":
            setError("Microphone access was denied. Please allow microphone access.");
            break;
          case "NO_SPEECH":
            setError("No speech detected. Please try again.");
            break;
          case "NETWORK_ERROR":
            setError("Network error. Please check your connection.");
            break;
          case "MIC_ERROR":
            setError("Microphone error. Please check your microphone.");
            break;
          default:
            setError("Voice recognition error. Please try again.");
        }
      } else if (!transcript.trim()) {
        // No error, but also no transcript - user probably didn't speak
        setState("idle");
      }
    }
  }, [isListening, state, sttError, transcript]);

  // ── Cleanup ────────────────────────────────────────────────────────────────

  useEffect(() => {
    return () => {
      stopSTT();
      stopSpeaking();
    };
  }, [stopSTT]);

  return {
    state,
    transcript,
    startListening,
    stopListening,
    speak,
    isSupported,
    error,
  };
}
