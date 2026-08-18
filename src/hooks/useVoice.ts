import { useState, useRef, useCallback, useEffect } from "react";
import type { VoiceState } from "@/types";

export type { VoiceState };

interface UseVoiceOptions {
  onListenEnd?: (transcript: string) => void;
  onSpeakEnd?: () => void;
  listenDuration?: number;
  simulatedTranscript?: string;
}

interface UseVoiceReturn {
  state: VoiceState;
  transcript: string;
  startListening: () => void;
  stopListening: () => void;
  speak: (text: string) => void;
}

export function useVoice(options: UseVoiceOptions = {}): UseVoiceReturn {
  const {
    onListenEnd,
    onSpeakEnd,
    listenDuration = 3000,
    simulatedTranscript = "",
  } = options;

  const [state, setState] = useState<VoiceState>("idle");
  const [transcript, setTranscript] = useState("");

  const listenTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const processTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const speakTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearAllTimers = useCallback(() => {
    if (listenTimerRef.current !== null) {
      clearTimeout(listenTimerRef.current);
      listenTimerRef.current = null;
    }
    if (processTimerRef.current !== null) {
      clearTimeout(processTimerRef.current);
      processTimerRef.current = null;
    }
    if (speakTimerRef.current !== null) {
      clearTimeout(speakTimerRef.current);
      speakTimerRef.current = null;
    }
  }, []);

  const startListening = useCallback(() => {
    clearAllTimers();
    setState("listening");
    setTranscript("");

    // After listenDuration → processing
    listenTimerRef.current = setTimeout(() => {
      setState("processing");

      // After 1200ms → speaking
      processTimerRef.current = setTimeout(() => {
        const captured = simulatedTranscript || "";
        setTranscript(captured);
        setState("speaking");
        onListenEnd?.(captured);

        // After 2200ms → idle
        speakTimerRef.current = setTimeout(() => {
          setState("idle");
          onSpeakEnd?.();
        }, 2200);
      }, 1200);
    }, listenDuration);
  }, [clearAllTimers, listenDuration, simulatedTranscript, onListenEnd, onSpeakEnd]);

  const stopListening = useCallback(() => {
    clearAllTimers();
    setState("idle");
    setTranscript("");
  }, [clearAllTimers]);

  const speak = useCallback((text: string) => {
    if (typeof window !== "undefined" && window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
      } catch {
        // Graceful fallback: speech synthesis unavailable
      }
    }
  }, []);

  // Clean up all timers on unmount
  useEffect(() => {
    return () => {
      clearAllTimers();
    };
  }, [clearAllTimers]);

  return { state, transcript, startListening, stopListening, speak };
}
