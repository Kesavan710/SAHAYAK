import { useState, useCallback } from "react";
import type { A11ySettings, Lang } from "@/types";
import { LANGUAGES } from "@/constants";

const STORAGE_KEY = "sahayak-a11y";

const DEFAULT_SETTINGS: A11ySettings = {
  textSize: "normal",
  highContrast: false,
  reduceMotion: false,
  readAloud: false,
  voiceFirst: false,
  lang: LANGUAGES[0],
};

function loadFromStorage(): A11ySettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT_SETTINGS;
    const parsed = JSON.parse(raw) as Partial<A11ySettings>;
    return { ...DEFAULT_SETTINGS, ...parsed };
  } catch {
    return DEFAULT_SETTINGS;
  }
}

function saveToStorage(settings: A11ySettings): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // Storage unavailable — silently ignore
  }
}

interface UseA11yReturn {
  settings: A11ySettings;
  setSettings: (next: A11ySettings | ((prev: A11ySettings) => A11ySettings)) => void;
  lang: Lang;
  setLang: (lang: Lang) => void;
}

export function useA11y(): UseA11yReturn {
  const [settings, setSettingsState] = useState<A11ySettings>(loadFromStorage);

  const setSettings = useCallback(
    (next: A11ySettings | ((prev: A11ySettings) => A11ySettings)) => {
      setSettingsState((prev) => {
        const updated = typeof next === "function" ? next(prev) : next;
        saveToStorage(updated);
        return updated;
      });
    },
    []
  );

  const setLang = useCallback(
    (lang: Lang) => {
      setSettingsState((prev) => {
        const updated: A11ySettings = { ...prev, lang };
        saveToStorage(updated);
        return updated;
      });
    },
    []
  );

  return {
    settings,
    setSettings,
    lang: settings.lang,
    setLang,
  };
}
