/**
 * Text-to-Speech service for Sahayak.
 *
 * Uses window.speechSynthesis (Web Speech API).
 * Gracefully degrades when TTS is unavailable.
 */

const TTS_RATE = 0.9;
const TTS_PITCH = 1.0;

/** True when the browser supports SpeechSynthesis. */
export function isTTSSupported(): boolean {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

/**
 * Speak text aloud using the browser TTS engine.
 * Always cancels any in-progress speech first to prevent overlap.
 *
 * @param text - Text to speak
 * @param speechCode - BCP-47 language code, e.g. "kn-IN"
 * @param onEnd - Called when speech finishes or is cancelled
 * @param onStart - Called when speech actually begins
 */
export function speak(
  text: string,
  speechCode: string,
  onEnd?: () => void,
  onStart?: () => void
): void {
  if (!isTTSSupported()) {
    console.warn("[Sahayak TTS] speechSynthesis not supported in this browser.");
    onEnd?.();
    return;
  }

  // Cancel any ongoing speech before starting new speech
  window.speechSynthesis.cancel();

  if (!text?.trim()) {
    onEnd?.();
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = speechCode;
  utterance.rate = TTS_RATE;
  utterance.pitch = TTS_PITCH;

  utterance.onstart = () => {
    onStart?.();
  };

  utterance.onend = () => {
    onEnd?.();
  };

  utterance.onerror = (event) => {
    // 'interrupted' is a normal cancellation — not a real error
    if (event.error !== "interrupted" && event.error !== "canceled") {
      console.error("[Sahayak TTS] Speech error:", event.error);
    }
    onEnd?.();
  };

  window.speechSynthesis.speak(utterance);
}

/**
 * Stop any currently playing TTS immediately.
 */
export function stopSpeaking(): void {
  if (!isTTSSupported()) return;
  window.speechSynthesis.cancel();
}

/**
 * Returns true if the TTS engine is currently speaking.
 */
export function isSpeaking(): boolean {
  if (!isTTSSupported()) return false;
  return window.speechSynthesis.speaking;
}
