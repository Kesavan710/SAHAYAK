import { useState, useRef, useEffect, useCallback, createContext, useContext } from "react";
import type { ReactNode, RefObject } from "react";
import { AnimatePresence, motion } from "motion/react";
import {
  Mic, Loader2, Volume2, Send, Lock, Accessibility, Landmark,
  CheckCircle, AlertCircle, AlertTriangle, Download, User, X,
  RotateCcw, Home, MessageSquare, List, FileText, ClipboardList,
  Activity, ChevronRight,
} from "lucide-react";

import type { View, ConvMessage, StatusResult } from "@/types";
import {
  LANGUAGES, CONV_STEPS, WAVEFORM_HEIGHTS, MOCK_SCHEMES,
  DEMO_HAVE_DOCS, DEMO_NEED_DOCS, DEMO_APPLICATION,
  DEMO_STATUS, DEMO_REG_NUMBER,
} from "@/constants";
import { cn, generateId } from "@/lib/utils";
import { getT, type Translations } from "@/lib/i18n";
import { useVoice } from "@/hooks/useVoice";
import { useA11y } from "@/hooks/useA11y";
import { SahayakLogo } from "@/components/ui/SahayakLogo";
import { GlobalStyles } from "@/components/layout/GlobalStyles";
import { VoiceInputPanel } from "@/components/conversation/VoiceInputPanel";

// ─── Translation context ─────────────────────────────────────────────────────

const TCtx = createContext<Translations>(getT("en"));
const useT = () => useContext(TCtx);

// ─── Constants ──────────────────────────────────────────────────────────────

const TEXT_SIZE_PX: Record<string, string> = {
  normal: "16px",
  large: "18px",
  larger: "20px",
};

const TEXT_SIZE_ORDER = ["normal", "large", "larger"] as const;

// ─── App ────────────────────────────────────────────────────────────────────

export default function App() {
  // ── View ──────────────────────────────────────────────────────────────────
  const [view, setView] = useState<View>("home");
  const [showA11y, setShowA11y] = useState(false);

  // ── Accessibility ─────────────────────────────────────────────────────────
  const { settings, setSettings, lang, setLang } = useA11y();
  const t = getT(lang.code);

  // ── Conversation ──────────────────────────────────────────────────────────
  const [convMessages, setConvMessages] = useState<ConvMessage[]>([]);
  const [step, setStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // ── Home text input ───────────────────────────────────────────────────────
  const [homeInput, setHomeInput] = useState("");

  // ── Status ────────────────────────────────────────────────────────────────
  const [regInput, setRegInput] = useState(DEMO_REG_NUMBER);
  const [statusResult, setStatusResult] = useState<StatusResult | null>(null);
  const [statusChecked, setStatusChecked] = useState(false);

  // ── Voice (home) ──────────────────────────────────────────────────────────
  const startConversation = useCallback((text: string, fromVoice = false) => {
    const userMsg: ConvMessage = {
      id: generateId(),
      role: "user",
      content: text,
      timestamp: new Date(),
      voiceInput: fromVoice,
    };
    const agentMsg: ConvMessage = {
      id: generateId(),
      role: "assistant",
      content: CONV_STEPS[0].agentText,
      timestamp: new Date(),
    };
    setConvMessages([userMsg, agentMsg]);
    setStep(0);
    setIsLoading(false);
    setView("conversation");
  }, []);

  const voice = useVoice({
    simulatedTranscript: "What government schemes can I apply for?",
    onListenEnd: (transcript) => {
      if (transcript) startConversation(transcript, true);
    },
  });

  // ── Effects ───────────────────────────────────────────────────────────────

  useEffect(() => {
    document.documentElement.style.fontSize = TEXT_SIZE_PX[settings.textSize] ?? "16px";
  }, [settings.textSize]);

  useEffect(() => {
    if (view === "conversation") {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [convMessages, view]);

  // ── Handlers ──────────────────────────────────────────────────────────────

  const handleHomeSubmit = useCallback(() => {
    const text = homeInput.trim();
    if (!text) return;
    setHomeInput("");
    startConversation(text);
  }, [homeInput, startConversation]);

  const handleAnswer = useCallback((text: string) => {
    const userMsg: ConvMessage = {
      id: generateId(),
      role: "user",
      content: text,
      timestamp: new Date(),
    };
    setConvMessages((prev) => [...prev, userMsg]);

    const nextStep = step + 1;
    if (nextStep < CONV_STEPS.length) {
      const nextConvStep = CONV_STEPS[nextStep];
      const agentMsg: ConvMessage = {
        id: generateId(),
        role: "assistant",
        content: nextConvStep.agentText,
        timestamp: new Date(),
      };
      setConvMessages((prev) => [...prev, agentMsg]);
      setStep(nextStep);

      if (nextConvStep.inputType === "loading") {
        setIsLoading(true);
        setTimeout(() => {
          setIsLoading(false);
          setView("schemes");
        }, 2200);
      }
    }
  }, [step]);

  const handleStatusCheck = useCallback(() => {
    setStatusChecked(true);
    const normalised = regInput.trim().toUpperCase();
    if (normalised === DEMO_REG_NUMBER.toUpperCase()) {
      setStatusResult(DEMO_STATUS);
    } else {
      setStatusResult(null);
    }
  }, [regInput]);

  const adjustTextSize = useCallback((dir: "up" | "down") => {
    setSettings((prev) => {
      const idx = TEXT_SIZE_ORDER.indexOf(prev.textSize);
      const nextIdx = dir === "up"
        ? Math.min(idx + 1, TEXT_SIZE_ORDER.length - 1)
        : Math.max(idx - 1, 0);
      return { ...prev, textSize: TEXT_SIZE_ORDER[nextIdx] };
    });
  }, [setSettings]);

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <TCtx.Provider value={t}>
    <div
      className={cn(
        "min-h-screen bg-background text-foreground font-sans",
        settings.highContrast && "contrast-150 saturate-150"
      )}
    >
      <GlobalStyles reduceMotion={settings.reduceMotion} />

      {/* ── Navigation ───────────────────────────────────────────────────── */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-border">
        <div className="max-w-screen-xl mx-auto px-4 h-16 flex items-center gap-3">
          {/* Brand */}
          <button
            className="flex items-center gap-2 shrink-0 min-h-[44px]"
            onClick={() => setView("home")}
            aria-label="Go to home"
          >
            <SahayakLogo size={32} />
            <div className="flex flex-col leading-tight text-left">
              <span className="font-bold text-sm text-foreground">Sahayak</span>
              <span className="text-xs text-muted-foreground hidden sm:block">
                {t.brandDescriptor}
              </span>
            </div>
          </button>

          {/* Nav items */}
          <div className="flex-1 flex items-center justify-center gap-0.5 overflow-x-auto scrollbar-hide px-2">
            {(
              [
                { view: "home" as const, label: t.navHome },
                { view: "conversation" as const, label: t.navConversation },
                { view: "schemes" as const, label: t.navSchemes },
                { view: "documents" as const, label: t.navDocuments },
                { view: "application" as const, label: t.navApplication },
                { view: "status" as const, label: t.navStatus },
              ]
            ).map(({ view: v, label }) => (
              <button
                key={v}
                onClick={() => setView(v)}
                className={cn(
                  "min-h-[44px] px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                  view === v
                    ? "bg-primary/10 text-primary font-semibold"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
              >
                {label}
              </button>
            ))}
          </div>

          {/* Right controls */}
          <div className="flex items-center gap-1.5 shrink-0">
            <select
              value={lang.code}
              onChange={(e) => {
                const found = LANGUAGES.find((l) => l.code === e.target.value);
                if (found) setLang(found);
              }}
              className="min-h-[44px] px-2 py-1 rounded-lg border border-border text-sm bg-background text-foreground cursor-pointer"
              aria-label="Select language"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code}>{l.native}</option>
              ))}
            </select>
            <button
              onClick={() => setShowA11y(true)}
              className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg border border-border hover:bg-muted transition-colors"
              aria-label="Accessibility settings"
            >
              <Accessibility className="w-5 h-5" />
            </button>
            <button
              className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg border border-border hover:bg-muted transition-colors"
              aria-label="User account"
            >
              <User className="w-5 h-5" />
            </button>
          </div>
        </div>
      </nav>

      {/* ── Views ────────────────────────────────────────────────────────── */}
      <main className="pt-16">
        <AnimatePresence mode="wait">
          {view === "home" && (
            <PageWrap key="home">
              <HomeView
                voice={voice}
                homeInput={homeInput}
                setHomeInput={setHomeInput}
                onSubmit={handleHomeSubmit}
                onChip={(text) => startConversation(text)}
              />
            </PageWrap>
          )}
          {view === "conversation" && (
            <PageWrap key="conversation">
              <ConversationView
                messages={convMessages}
                step={step}
                isLoading={isLoading}
                messagesEndRef={messagesEndRef}
                onAnswer={handleAnswer}
              />
            </PageWrap>
          )}
          {view === "schemes" && (
            <PageWrap key="schemes">
              <SchemesView onDocuments={() => setView("documents")} />
            </PageWrap>
          )}
          {view === "documents" && (
            <PageWrap key="documents">
              <DocumentsView onContinue={() => setView("application")} />
            </PageWrap>
          )}
          {view === "application" && (
            <PageWrap key="application">
              <ApplicationView onStatus={() => setView("status")} />
            </PageWrap>
          )}
          {view === "status" && (
            <PageWrap key="status">
              <StatusView
                regInput={regInput}
                setRegInput={setRegInput}
                onCheck={handleStatusCheck}
                statusResult={statusResult}
                statusChecked={statusChecked}
              />
            </PageWrap>
          )}
        </AnimatePresence>
      </main>

      {/* ── Accessibility Panel ──────────────────────────────────────────── */}
      <AnimatePresence>
        {showA11y && (
          <>
            {/* Backdrop */}
            <motion.div
              key="a11y-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 bg-black/40"
              onClick={() => setShowA11y(false)}
            />
            {/* Panel */}
            <motion.aside
              key="a11y-panel"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 28, stiffness: 280 }}
              className="fixed top-0 right-0 bottom-0 z-50 w-80 bg-card border-l border-border shadow-2xl overflow-y-auto scrollbar-hide"
              aria-label="Accessibility settings panel"
            >
              <div className="p-6 flex flex-col gap-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-bold text-foreground">{t.a11yTitle}</h2>
                  <button
                    onClick={() => setShowA11y(false)}
                    className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg hover:bg-muted transition-colors"
                    aria-label="Close accessibility panel"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Text size */}
                <div>
                  <p className="text-sm font-semibold text-foreground mb-3">{t.textSizeLabel}</p>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => adjustTextSize("down")}
                      disabled={settings.textSize === "normal"}
                      className="min-h-[44px] flex-1 flex items-center justify-center rounded-xl border border-border font-bold text-lg hover:bg-muted transition-colors disabled:opacity-40"
                      aria-label="Decrease text size"
                    >
                      A−
                    </button>
                    <button
                      className="min-h-[44px] flex-1 flex items-center justify-center rounded-xl border border-primary bg-primary/10 text-primary font-semibold text-base"
                      aria-current="true"
                    >
                      A
                    </button>
                    <button
                      onClick={() => adjustTextSize("up")}
                      disabled={settings.textSize === "larger"}
                      className="min-h-[44px] flex-1 flex items-center justify-center rounded-xl border border-border font-bold text-xl hover:bg-muted transition-colors disabled:opacity-40"
                      aria-label="Increase text size"
                    >
                      A+
                    </button>
                  </div>
                </div>

                {/* Toggles */}
                {(
                  [
                    { key: "highContrast", label: t.highContrastLabel },
                    { key: "reduceMotion", label: t.reduceMotionLabel },
                    { key: "readAloud", label: t.readAloudLabel },
                    { key: "voiceFirst", label: t.voiceFirstLabel },
                  ] as const
                ).map(({ key, label }) => (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">{label}</span>
                    <button
                      role="switch"
                      aria-checked={settings[key]}
                      onClick={() => setSettings((prev) => ({ ...prev, [key]: !prev[key] }))}
                      className={cn(
                        "relative w-12 h-6 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
                        settings[key] ? "bg-primary" : "bg-muted-foreground/30"
                      )}
                    >
                      <span
                        className={cn(
                          "absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform",
                          settings[key] && "translate-x-6"
                        )}
                      />
                    </button>
                  </div>
                ))}

                {/* Language */}
                <div>
                  <p className="text-sm font-semibold text-foreground mb-3">{t.languageLabel}</p>
                  <div className="flex flex-col gap-2">
                    {LANGUAGES.map((l) => (
                      <button
                        key={l.code}
                        onClick={() => setLang(l)}
                        className={cn(
                          "min-h-[44px] px-4 py-2 rounded-xl text-sm font-medium text-left transition-colors",
                          lang.code === l.code
                            ? "bg-primary/10 text-primary border border-primary/30 font-semibold"
                            : "border border-border hover:bg-muted"
                        )}
                      >
                        <span className="mr-2">{l.native}</span>
                        <span className="text-muted-foreground text-xs">{l.name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </div>
    </TCtx.Provider>
  );
}

// ─── PageWrap ───────────────────────────────────────────────────────────────

function PageWrap({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
}

// ─── HomeView ───────────────────────────────────────────────────────────────

interface HomeViewProps {
  voice: ReturnType<typeof useVoice>;
  homeInput: string;
  setHomeInput: (v: string) => void;
  onSubmit: () => void;
  onChip: (text: string) => void;
}

function HomeView({ voice, homeInput, setHomeInput, onSubmit, onChip }: HomeViewProps) {
  const t = useT();
  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl flex flex-col items-center gap-8">
        {/* Headline */}
        <div className="text-center space-y-3">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
            {t.heroTitle}
          </h1>
          <p className="text-lg text-muted-foreground max-w-md mx-auto">
            {t.heroSubtitle}
          </p>
        </div>

        {/* Mic button */}
        <div className="flex flex-col items-center gap-4">
          {voice.state === "idle" && (
            <div className="relative flex items-center justify-center">
              {/* Dashed animated ring */}
              <span
                className="absolute w-28 h-28 rounded-full border-2 border-dashed border-primary/40 animate-spin"
                style={{ animationDuration: "6s" }}
                aria-hidden="true"
              />
              <button
                onClick={voice.startListening}
                className="relative z-10 w-20 h-20 rounded-full bg-white border-2 border-border shadow-md flex items-center justify-center hover:bg-primary/5 transition-colors"
                aria-label="Tap to speak"
              >
                <Mic className="w-8 h-8 text-primary" />
              </button>
            </div>
          )}

          {voice.state === "listening" && (
            <div className="relative flex items-center justify-center">
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  className="absolute rounded-full bg-blue-500/20"
                  style={{
                    width: `${5 + i * 2.5}rem`,
                    height: `${5 + i * 2.5}rem`,
                    animation: `pulse-ring ${1.2 + i * 0.3}s ease-out infinite`,
                    animationDelay: `${i * 0.2}s`,
                  }}
                  aria-hidden="true"
                />
              ))}
              <button
                onClick={voice.stopListening}
                className="relative z-10 w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg flex items-center justify-center"
                aria-label="Stop listening"
              >
                <Mic className="w-8 h-8 text-white" />
              </button>
            </div>
          )}

          {voice.state === "processing" && (
            <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center">
              <Loader2 className="w-8 h-8 text-primary animate-spin" />
            </div>
          )}

          {voice.state === "speaking" && (
            <div className="flex flex-col items-center gap-3">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 shadow-lg flex items-center justify-center">
                <Volume2 className="w-8 h-8 text-white" />
              </div>
              {/* Waveform bars */}
              <div className="flex items-end gap-[3px] h-10" aria-hidden="true">
                {WAVEFORM_HEIGHTS.slice(0, 8).map((h, i) => (
                  <div
                    key={i}
                    className="w-1 rounded-full bg-teal-500 origin-bottom"
                    style={{
                      height: `${h}px`,
                      animation: "bar-wave 0.9s ease-in-out infinite",
                      animationDelay: `${(i * 0.9) / 8}s`,
                    }}
                  />
                ))}
              </div>
              <button
                onClick={voice.startListening}
                className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                {t.replayLabel}
              </button>
            </div>
          )}

          <p className="text-sm text-muted-foreground text-center">
            {voice.state === "idle" && t.tapToSpeak}
            {voice.state === "listening" && t.listeningLabel}
            {voice.state === "processing" && t.thinkingLabel}
            {voice.state === "speaking" && t.speakingLabel}
          </p>
        </div>

        {/* Text input */}
        <div className="w-full flex gap-2">
          <input
            type="text"
            value={homeInput}
            onChange={(e) => setHomeInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                onSubmit();
              }
            }}
            placeholder={t.homeInputPlaceholder}
            className="flex-1 min-h-[52px] px-5 rounded-2xl border border-border bg-background text-foreground placeholder:text-muted-foreground text-base focus:outline-none focus:ring-2 focus:ring-primary/40"
            aria-label="Type your question"
          />
          <button
            onClick={onSubmit}
            disabled={!homeInput.trim()}
            className="min-h-[52px] min-w-[52px] bg-primary text-primary-foreground rounded-2xl flex items-center justify-center hover:bg-primary/90 transition-colors disabled:opacity-40"
            aria-label="Send"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>

        {/* Quick-start chips */}
        <div className="flex flex-wrap gap-2 justify-center">
          {t.quickChips.map((chip) => (
            <button
              key={chip}
              onClick={() => onChip(chip)}
              className="min-h-[44px] px-4 py-2 rounded-xl text-sm font-medium border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Trust strip */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full pt-4 border-t border-border">
          {[
            { icon: <Lock className="w-5 h-5 text-primary" />, title: t.trust1Title, desc: t.trust1Desc },
            { icon: <Accessibility className="w-5 h-5 text-primary" />, title: t.trust2Title, desc: t.trust2Desc },
            { icon: <Landmark className="w-5 h-5 text-primary" />, title: t.trust3Title, desc: t.trust3Desc },
          ].map(({ icon, title, desc }) => (
            <div key={title} className="flex flex-col items-center text-center gap-1.5 p-4">
              {icon}
              <span className="text-sm font-semibold text-foreground">{title}</span>
              <span className="text-xs text-muted-foreground">{desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── ConversationView ───────────────────────────────────────────────────────

interface ConversationViewProps {
  messages: ConvMessage[];
  step: number;
  isLoading: boolean;
  messagesEndRef: RefObject<HTMLDivElement>;
  onAnswer: (text: string) => void;
}

function ConversationView({ messages, step, isLoading, messagesEndRef, onAnswer }: ConversationViewProps) {
  const t = useT();
  const STEP_TEXTS = [t.convStep0, t.convStep1, t.convStep2, t.convStep3];
  const currentStep = CONV_STEPS[step];
  const currentAgentText = STEP_TEXTS[step] ?? currentStep?.agentText ?? "";
  const completedSteps = step;
  const totalSteps = CONV_STEPS.length - 1;

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-6 flex flex-col md:flex-row gap-6 min-h-[calc(100vh-4rem)]">
      {/* Left: message history */}
      <div className="flex-1 md:w-2/3 flex flex-col gap-4 overflow-y-auto scrollbar-hide max-h-[calc(100vh-8rem)]">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={cn(
              "flex gap-3",
              msg.role === "user" && "justify-end"
            )}
          >
            {msg.role === "assistant" && (
              <div className="shrink-0 mt-1">
                <SahayakLogo size={28} />
              </div>
            )}
            <div
              className={cn(
                "max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
                msg.role === "assistant"
                  ? "bg-secondary text-secondary-foreground"
                  : "bg-primary/10 text-foreground"
              )}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {/* Thinking indicator */}
        {isLoading && (
          <div className="flex gap-3 items-center">
            <div className="shrink-0">
              <SahayakLogo size={28} />
            </div>
            <div className="bg-secondary rounded-2xl px-4 py-3 flex gap-1.5 items-center">
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  className="w-2 h-2 rounded-full bg-muted-foreground"
                  style={{
                    animation: "dot-bounce 1.2s ease-in-out infinite",
                    animationDelay: `${i * 0.2}s`,
                  }}
                />
              ))}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Right: current question panel */}
      <div className="md:w-1/3 shrink-0">
        <div className="bg-card rounded-2xl border border-border shadow-sm p-6 sticky top-20">
          {/* Progress */}
          <div className="mb-5">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-widest">
                {currentStep?.progressLabel ?? "Analysing"}
              </span>
              <span className="text-xs text-muted-foreground">
                {t.convDetailsCollected(Math.min(completedSteps, totalSteps), totalSteps)}
              </span>
            </div>
            <div className="flex gap-1.5">
              {CONV_STEPS.slice(0, totalSteps).map((_, i) => (
                <div
                  key={i}
                  className={cn(
                    "h-1.5 flex-1 rounded-full transition-colors",
                    i < completedSteps ? "bg-primary" : "bg-muted"
                  )}
                />
              ))}
            </div>
          </div>

          {/* Loading skeleton */}
          {currentStep?.inputType === "loading" ? (
            <div className="flex flex-col gap-3">
              <p className="text-sm text-muted-foreground mb-2">{currentAgentText}</p>
              {[1, 2, 3].map((i) => (
                <div key={i} className="rounded-xl overflow-hidden">
                  <div
                    className="skeleton-shimmer h-16 rounded-xl"
                    style={{ animationDelay: `${i * 0.15}s` }}
                  />
                </div>
              ))}
            </div>
          ) : (
            currentStep && (
              <div className="flex flex-col gap-4">
                <p className="text-sm font-medium text-foreground leading-relaxed">
                  {currentAgentText}
                </p>
                <VoiceInputPanel
                  options={currentStep.options}
                  onAnswer={onAnswer}
                  hc={false}
                />
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ─── SchemesView ─────────────────────────────────────────────────────────────

function SchemesView({ onDocuments }: { onDocuments: () => void }) {
  const t = useT();
  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground mb-1">
          {t.schemesTitle}
        </h1>
        <p className="text-sm text-muted-foreground">
          {t.schemesSubtitle}
        </p>
      </div>

      <div className="flex flex-col gap-6">
        {MOCK_SCHEMES.map((scheme) => (
          <div key={scheme.id} className="bg-card rounded-2xl border border-border shadow-sm p-6">
            {/* Header */}
            <div className="flex flex-wrap items-start justify-between gap-3 mb-4">
              <div>
                <h2 className="text-lg font-bold text-foreground">{scheme.name}</h2>
                <p className="text-sm text-muted-foreground mt-0.5">
                  {scheme.ministry} · {scheme.category}
                </p>
              </div>
              <span
                className={cn(
                  "shrink-0 px-3 py-1 rounded-full text-xs font-semibold",
                  scheme.eligible
                    ? "bg-green-100 text-green-800"
                    : "bg-slate-100 text-slate-600"
                )}
              >
                {scheme.eligible ? t.eligible : t.notEligible}
              </span>
            </div>

            {/* Not eligible reason */}
            {!scheme.eligible && scheme.notEligibleReason && (
              <div className="mb-4 p-3 rounded-xl bg-amber-50 border border-amber-200 text-sm text-amber-800">
                {scheme.notEligibleReason}
              </div>
            )}

            {/* Why this matches */}
            {scheme.matchReasons.length > 0 && (
              <div className="mb-4">
                <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-2">
                  {t.whyMatches}
                </p>
                <ul className="flex flex-col gap-1">
                  {scheme.matchReasons.map((r) => (
                    <li key={r} className="flex gap-2 text-sm text-foreground">
                      <CheckCircle className="w-4 h-4 text-green-600 shrink-0 mt-0.5" />
                      {r}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Benefits */}
            <div className="mb-4">
              <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-2">
                {t.benefitsLabel}
              </p>
              <ul className="flex flex-col gap-1">
                {scheme.benefits.map((b) => (
                  <li key={b} className="flex gap-2 text-sm text-foreground">
                    <ChevronRight className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                    {b}
                  </li>
                ))}
              </ul>
            </div>

            {/* Official source */}
            <p className="text-xs text-muted-foreground mb-4">
              Official source:{" "}
              <span className="text-primary underline cursor-pointer">
                {scheme.officialUrl}
              </span>
              {" "}· Last updated: {scheme.lastUpdated}
            </p>

            {/* CTA */}
            {scheme.eligible && (
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={onDocuments}
                  className="min-h-[44px] bg-primary text-primary-foreground rounded-xl px-6 py-3 font-semibold text-sm hover:bg-primary/90 transition-colors"
                >
                  {t.viewDocs}
                </button>
                <button className="min-h-[44px] border border-border rounded-xl px-6 py-3 text-sm font-medium hover:bg-muted transition-colors">
                  {t.viewSource}
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── DocumentsView ───────────────────────────────────────────────────────────

function DocumentsView({ onContinue }: { onContinue: () => void }) {
  const t = useT();
  const have = DEMO_HAVE_DOCS;
  const need = DEMO_NEED_DOCS;
  const total = have.length + need.length;
  const readyCount = have.length;
  const progressPct = Math.round((readyCount / total) * 100);

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-foreground mb-1">
          {t.docsTitle}
        </h1>
        <p className="text-muted-foreground text-sm">
          {t.docsSubtitle}
        </p>
      </div>

      {/* Progress */}
      <div className="bg-card rounded-2xl border border-border shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-3">
          <span className="font-semibold text-foreground">
            {t.docsReady(readyCount, total)}
          </span>
          <span className="text-sm text-muted-foreground">{progressPct}%</span>
        </div>
        <div className="h-3 rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>

      {/* Two columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* You have */}
        <div className="bg-card rounded-2xl border border-border shadow-sm p-6">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h2 className="font-semibold text-green-800">{t.youHave}</h2>
          </div>
          <div className="flex flex-col gap-3">
            {have.map((doc) => (
              <div key={doc.id} className="flex gap-3">
                <CheckCircle className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-foreground">{doc.label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{doc.note}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Still needed */}
        <div className="bg-card rounded-2xl border border-border shadow-sm p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-5 h-5 text-amber-600" />
            <h2 className="font-semibold text-amber-800">{t.stillNeeded}</h2>
          </div>
          <div className="flex flex-col gap-3">
            {need.map((doc) => (
              <div key={doc.id} className="flex gap-3">
                <div className="w-5 h-5 rounded-full border-2 border-dashed border-amber-400 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-foreground">{doc.label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{doc.note}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <button
        onClick={onContinue}
        className="min-h-[52px] bg-primary text-primary-foreground rounded-xl px-8 py-3 font-semibold text-base hover:bg-primary/90 transition-colors"
      >
        {t.continueBtn}
      </button>
    </div>
  );
}

// ─── ApplicationView ─────────────────────────────────────────────────────────

function ApplicationView({ onStatus }: { onStatus: () => void }) {
  const t = useT();
  const fields: [string, string][] = [
    ["Name", DEMO_APPLICATION.name],
    ["Date of Birth", DEMO_APPLICATION.dob],
    ["State", DEMO_APPLICATION.state],
    ["District", DEMO_APPLICATION.district],
    ["Education", DEMO_APPLICATION.education],
    ["Disability", DEMO_APPLICATION.disability],
    ["Annual Income", DEMO_APPLICATION.income],
  ];

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-foreground mb-1">
          {t.appTitle}
        </h1>
        <p className="text-sm text-muted-foreground">
          {DEMO_APPLICATION.scheme}
        </p>
      </div>

      {/* Progress — full */}
      <div className="bg-card rounded-2xl border border-border shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-3">
          <span className="font-semibold text-foreground">4 / 4 documents ready</span>
          <span className="text-sm text-green-700 font-medium">100%</span>
        </div>
        <div className="h-3 rounded-full bg-muted overflow-hidden">
          <div className="h-full w-full rounded-full bg-green-500" />
        </div>
      </div>

      {/* Safety notice */}
      <div className="bg-amber-50 border border-amber-300 rounded-2xl p-5 mb-6 flex gap-3">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold text-amber-900 mb-1">
            {t.safetyHeading}
          </p>
          <p className="text-sm text-amber-800 leading-relaxed">
            {t.safetyBody}{" "}
            {t.safetyWarning}
          </p>
        </div>
      </div>

      {/* Application summary */}
      <div className="bg-card rounded-2xl border border-border shadow-sm p-6 mb-6">
        <h2 className="font-semibold text-foreground mb-4">Application Summary</h2>
        <div className="divide-y divide-border">
          {fields.map(([label, value]) => (
            <div key={label} className="flex gap-4 py-3">
              <span className="text-sm text-muted-foreground w-36 shrink-0">{label}</span>
              <span className="text-sm text-foreground font-medium">{value}</span>
            </div>
          ))}
        </div>
        <div className="mt-4 pt-4 border-t border-border flex gap-4">
          <span className="text-sm text-muted-foreground w-36 shrink-0">Application ID</span>
          <span className="text-sm font-mono text-foreground">{DEMO_APPLICATION.applicationId}</span>
        </div>
      </div>

      {/* CTA */}
      <div className="flex flex-col sm:flex-row gap-3">
        <button className="min-h-[52px] bg-primary text-primary-foreground rounded-xl px-8 py-3 font-semibold text-base hover:bg-primary/90 transition-colors flex items-center gap-2 justify-center">
          <Download className="w-5 h-5" />
          {t.downloadBtn}
        </button>
        <p className="hidden sm:flex items-center text-sm text-muted-foreground pl-2">
          {t.downloadDesc}
        </p>
      </div>
      <p className="text-sm text-muted-foreground mt-2 mb-4 sm:hidden">
        {t.downloadDesc}
      </p>
      <button
        onClick={onStatus}
        className="min-h-[44px] border border-border rounded-xl px-6 py-3 text-sm font-medium hover:bg-muted transition-colors mt-3"
      >
        {t.checkStatusBtn}
      </button>
    </div>
  );
}

// ─── StatusView ───────────────────────────────────────────────────────────────

interface StatusViewProps {
  regInput: string;
  setRegInput: (v: string) => void;
  onCheck: () => void;
  statusResult: StatusResult | null;
  statusChecked: boolean;
}

function StatusView({ regInput, setRegInput, onCheck, statusResult, statusChecked }: StatusViewProps) {
  const t = useT();
  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground mb-1">
          {t.statusTitle}
        </h1>
        <p className="text-sm text-muted-foreground">
          {t.statusSubtitle}
        </p>
      </div>

      {/* Input */}
      <div className="bg-card rounded-2xl border border-border shadow-sm p-6 mb-8 flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={regInput}
          onChange={(e) => setRegInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") onCheck(); }}
          placeholder={t.regPlaceholder}
          className="flex-1 min-h-[52px] px-5 rounded-xl border border-border bg-background text-foreground font-mono text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
          aria-label="Registration number"
        />
        <button
          onClick={onCheck}
          className="min-h-[52px] bg-primary text-primary-foreground rounded-xl px-8 font-semibold text-sm hover:bg-primary/90 transition-colors"
        >
          {t.checkBtn}
        </button>
      </div>

      {/* Result */}
      {statusChecked && (
        <>
          {statusResult ? (
            <div className="flex flex-col gap-6">
              {/* Status badge */}
              <div className="bg-card rounded-2xl border border-border shadow-sm p-6">
                <div className="flex flex-wrap items-center justify-between gap-4 mb-3">
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">{statusResult.scheme}</p>
                    <span className="px-4 py-1.5 rounded-full bg-green-100 text-green-800 font-semibold text-sm capitalize">
                      {statusResult.currentStatus.replace(/_/g, " ")}
                    </span>
                  </div>
                  <div className="text-right text-sm text-muted-foreground">
                    <p>{t.lastUpdated}: {statusResult.lastUpdated}</p>
                    <p className="text-xs mt-0.5">{t.officialPortal}</p>
                  </div>
                </div>
              </div>

              {/* Horizontal timeline */}
              <div className="bg-card rounded-2xl border border-border shadow-sm p-6 overflow-x-auto">
                <h2 className="font-semibold text-foreground mb-6">{t.timelineLabel}</h2>
                <div className="flex items-start min-w-max gap-0">
                  {statusResult.timeline.map((step, i) => {
                    const isLast = i === statusResult.timeline.length - 1;
                    return (
                      <div key={i} className="flex items-start">
                        <div className="flex flex-col items-center w-28">
                          {/* Circle */}
                          <div
                            className={cn(
                              "w-8 h-8 rounded-full border-2 flex items-center justify-center mb-2 transition-colors",
                              step.active
                                ? "border-primary bg-primary"
                                : step.done
                                ? "border-green-500 bg-green-500"
                                : "border-muted-foreground/30 bg-background"
                            )}
                          >
                            {(step.done || step.active) && (
                              <CheckCircle className="w-4 h-4 text-white" />
                            )}
                          </div>
                          {/* Label */}
                          <p
                            className={cn(
                              "text-xs text-center font-medium leading-tight",
                              step.active ? "text-primary" : step.done ? "text-green-700" : "text-muted-foreground"
                            )}
                          >
                            {step.label}
                          </p>
                          {step.date && (
                            <p className="text-xs text-muted-foreground mt-1">{step.date}</p>
                          )}
                        </div>

                        {/* Connector line */}
                        {!isLast && (
                          <div
                            className={cn(
                              "h-0.5 w-8 mt-4 shrink-0 transition-colors",
                              step.done ? "bg-green-400" : "bg-muted"
                            )}
                          />
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          ) : (
            /* Not found */
            <div className="bg-card rounded-2xl border border-border shadow-sm p-10 text-center">
              <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                <FileText className="w-6 h-6 text-muted-foreground" />
              </div>
              <h2 className="text-lg font-semibold text-foreground mb-2">{t.notFoundTitle}</h2>
              <p className="text-sm text-muted-foreground max-w-xs mx-auto">
                {t.notFoundDesc}
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
