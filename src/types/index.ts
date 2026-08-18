// ─── Navigation ────────────────────────────────────────────────────────────

export type View =
  | "home"
  | "conversation"
  | "schemes"
  | "documents"
  | "application"
  | "status";

// ─── Voice / Audio ─────────────────────────────────────────────────────────

/** State of the AI voice-output engine */
export type VoiceState = "idle" | "listening" | "processing" | "speaking";

/** State of the microphone / speech-recognition input */
export type ListenState = "idle" | "listening" | "recognized";

// ─── Accessibility ─────────────────────────────────────────────────────────

export type TextSize = "normal" | "large" | "larger";

export interface Lang {
  /** ISO 639-1 language code (e.g. "kn", "hi") */
  code: string;
  /** English name of the language */
  name: string;
  /** Language name written in its own script */
  native: string;
}

export interface A11ySettings {
  textSize: TextSize;
  highContrast: boolean;
  reduceMotion: boolean;
  /** Read assistant replies aloud using TTS */
  readAloud: boolean;
  /** App starts in voice-first mode instead of text */
  voiceFirst: boolean;
  lang: Lang;
}

// ─── Conversation ──────────────────────────────────────────────────────────

export interface ConvMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  /** True while the assistant is generating a reply */
  isLoading?: boolean;
  /** True when the user input was captured via microphone */
  voiceInput?: boolean;
}

export interface ConvStep {
  id: string;
  /** Text shown by the assistant agent for this step */
  agentText: string;
  /** How the user responds to this step */
  inputType: "chips" | "text" | "loading";
  /** Chip option labels; empty for text/loading steps */
  options: string[];
  /** Short label shown in the progress indicator */
  progressLabel: string;
}

/** Accumulated answers from the guided conversation flow */
export interface ConvContext {
  /** Indian state chosen by the user */
  state?: string;
  /** Disability category (e.g. "Visual Impairment") */
  disability?: string;
  /** Annual household income bracket */
  income?: string;
  /** Arbitrary extra fields collected during conversation */
  [key: string]: string | undefined;
}

// ─── Schemes ───────────────────────────────────────────────────────────────

export interface Scheme {
  id: string;
  name: string;
  /** E.g. "Disability Support", "Housing", "Employment" */
  category: string;
  /** Nodal ministry name */
  ministry: string;
  /** Whether the applicant's profile matches eligibility criteria */
  eligible: boolean;
  /** Human-readable explanation when eligible is false */
  notEligibleReason?: string;
  /** Bullet points explaining why the profile matches */
  matchReasons: string[];
  /** Key benefits listed on the scheme */
  benefits: string[];
  /** Documents the applicant must submit */
  requiredDocuments: string[];
  /** Direct link to the official government portal */
  officialUrl: string;
  /** Source document / circular reference */
  sourceDoc: string;
  /** ISO date string of last data refresh */
  lastUpdated: string;
}

// ─── Documents ─────────────────────────────────────────────────────────────

export interface DocumentItem {
  id: string;
  /** Display label shown to the user */
  label: string;
  /** Tip on acceptable formats or where to obtain the document */
  note: string;
  status: "available" | "missing" | "uploading" | "uploaded";
}

// ─── Application ───────────────────────────────────────────────────────────

export interface ApplicationSummary {
  name: string;
  /** ISO date string */
  dob: string;
  state: string;
  district: string;
  education: string;
  disability: string;
  /** Annual household income (formatted string with currency) */
  income: string;
  scheme: string;
  /** System-generated reference number */
  applicationId: string;
}

// ─── Status Tracking ───────────────────────────────────────────────────────

export type ApplicationStatus =
  | "submitted"
  | "under_review"
  | "document_verification"
  | "approved"
  | "disbursed"
  | "rejected"
  | "on_hold";

export interface TimelineStep {
  label: string;
  /** Formatted date string; empty string if not yet reached */
  date: string;
  done: boolean;
  active: boolean;
}

export interface StatusResult {
  registrationNumber: string;
  scheme: string;
  state: string;
  currentStatus: ApplicationStatus;
  lastUpdated: string;
  timeline: TimelineStep[];
  /** URL of the official portal where the applicant can verify */
  officialSource: string;
}

// ─── API Errors ────────────────────────────────────────────────────────────

export interface ApiError {
  /** Machine-readable error code (e.g. "NOT_FOUND", "RATE_LIMITED") */
  code: string;
  message: string;
}
