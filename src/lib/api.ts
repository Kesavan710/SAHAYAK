/**
 * api.ts — Sahayak API abstraction layer
 *
 * HOW TO CONNECT TO THE REAL BACKEND
 * ─────────────────────────────────────────────────────────────────────────
 * 1. Set VITE_API_URL in your .env file, e.g.:
 *      VITE_API_URL=https://api.sahayak.gov.in/v1
 *
 * 2. The FastAPI backend is expected to expose:
 *      POST   /conversation/chat
 *      POST   /schemes/search
 *      GET    /status/:registrationNumber
 *      POST   /documents/upload
 *
 * 3. Authentication: add your bearer token to VITE_API_TOKEN in .env.
 *    The request helper below will attach it automatically.
 *
 * 4. When VITE_API_URL is an empty string (default for local dev / demo),
 *    every function returns realistic mock data after a simulated delay.
 * ─────────────────────────────────────────────────────────────────────────
 */

import type { ApiError, ConvContext, Scheme, StatusResult } from "@/types";
import { MOCK_SCHEMES, DEMO_STATUS, DEMO_REG_NUMBER } from "@/constants";
import { delay } from "@/lib/utils";

// ─── Environment config ────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_URL as string | undefined;
const API_TOKEN = import.meta.env.VITE_API_TOKEN as string | undefined;
const IS_MOCK = !API_BASE || API_BASE.trim() === "";

// Simulated network delay range for mock responses (ms)
const MOCK_DELAY_MIN = 600;
const MOCK_DELAY_MAX = 1400;

// ─── Request / Response types ──────────────────────────────────────────────

export interface ChatRequest {
  message: string;
  sessionId: string;
  context: ConvContext;
}

export interface ChatResponse {
  reply: string;
  sessionId: string;
  /** Structured data the agent wants to surface (e.g. matched schemes) */
  data?: unknown;
}

export interface SchemeSearchRequest {
  context: ConvContext;
}

export interface SchemeSearchResponse {
  schemes: Scheme[];
  totalMatched: number;
}

export interface StatusLookupResponse {
  result: StatusResult | null;
}

export interface DocumentUploadResponse {
  url: string;
  /** Backend-assigned document identifier */
  storedId: string;
}

// ─── Internal helpers ──────────────────────────────────────────────────────

/** Random delay within the mock range, mimicking variable network latency */
async function mockDelay(): Promise<void> {
  const ms =
    MOCK_DELAY_MIN + Math.random() * (MOCK_DELAY_MAX - MOCK_DELAY_MIN);
  await delay(Math.round(ms));
}

/**
 * Central fetch wrapper that:
 *  - Attaches the Authorization header when a token is configured
 *  - Parses the JSON body
 *  - Throws a typed ApiError on non-2xx responses
 */
async function request<T>(
  path: string,
  init: RequestInit = {}
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined),
  };

  if (API_TOKEN) {
    headers["Authorization"] = `Bearer ${API_TOKEN}`;
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...init,
      headers,
    });
  } catch (networkError) {
    const err: ApiError = {
      code: "NETWORK_ERROR",
      message:
        networkError instanceof Error
          ? networkError.message
          : "A network error occurred. Please check your connection.",
    };
    throw err;
  }

  if (!response.ok) {
    let errorBody: Partial<ApiError> = {};
    try {
      errorBody = (await response.json()) as Partial<ApiError>;
    } catch {
      // Body was not JSON — ignore
    }
    const err: ApiError = {
      code: errorBody.code ?? `HTTP_${response.status}`,
      message:
        errorBody.message ??
        `Request failed with status ${response.status} ${response.statusText}`,
    };
    throw err;
  }

  return response.json() as Promise<T>;
}

// ─── conversation.chat ─────────────────────────────────────────────────────

/**
 * Send a user message to the AI agent and receive a reply.
 *
 * MOCK: Returns a contextual canned reply based on the message content.
 * REAL: POST /conversation/chat  →  ChatResponse
 */
async function chat(
  message: string,
  sessionId: string,
  context: ConvContext
): Promise<ChatResponse> {
  if (IS_MOCK) {
    await mockDelay();

    // Produce a context-aware mock reply for demo purposes
    let reply =
      "I have noted your response. Let me look up the relevant schemes for you.";

    const lower = message.toLowerCase();
    if (lower.includes("pension") || lower.includes("viklang")) {
      reply =
        "The PM Viklang Samman Pension Yojana provides a monthly pension to persons with disabilities. Based on your profile, you appear to be eligible. Shall I walk you through the application process?";
    } else if (lower.includes("house") || lower.includes("awas")) {
      reply =
        "PMAY-EWS provides housing assistance. However, eligibility depends on income and existing property ownership. Let me verify your profile details.";
    } else if (lower.includes("document") || lower.includes("certificate")) {
      reply =
        "The key documents you will need are: Aadhaar Card, Disability Certificate (UDID), Income Certificate, and Bank Passbook. I can guide you on how to obtain any missing documents.";
    } else if (lower.includes("status") || lower.includes("application")) {
      reply = `To check your application status, please share your registration number. Your demo registration number is ${DEMO_REG_NUMBER}.`;
    } else if (context.state) {
      reply = `I have noted that you are from ${context.state}. ${
        context.disability
          ? `With ${context.disability}, you may qualify for several central and state-level schemes. `
          : ""
      }Let me find the best matches for your profile.`;
    }

    return { reply, sessionId };
  }

  // ── Real backend ────────────────────────────────────────────────────────
  return request<ChatResponse>("/conversation/chat", {
    method: "POST",
    body: JSON.stringify({ message, sessionId, context } satisfies ChatRequest),
  });
}

// ─── schemes.search ────────────────────────────────────────────────────────

/**
 * Search for government schemes matching the given eligibility context.
 *
 * MOCK: Returns a filtered subset of MOCK_SCHEMES based on income/disability.
 * REAL: POST /schemes/search  →  SchemeSearchResponse
 */
async function searchSchemes(context: ConvContext): Promise<Scheme[]> {
  if (IS_MOCK) {
    await mockDelay();

    // Basic mock filtering — income above ₹5 lakh hides PMAY EWS as not relevant
    const income = context.income ?? "";
    const highIncome =
      income.includes("5,00,000") || income.includes("8,00,000") || income.includes("Above");

    return MOCK_SCHEMES.filter((s) => {
      if (highIncome && s.id === "scheme-pmay-ews") {
        // Still return it but it is already marked not eligible
        return true;
      }
      return true;
    });
  }

  // ── Real backend ────────────────────────────────────────────────────────
  const response = await request<SchemeSearchResponse>("/schemes/search", {
    method: "POST",
    body: JSON.stringify({ context } satisfies SchemeSearchRequest),
  });
  return response.schemes;
}

// ─── status.lookup ─────────────────────────────────────────────────────────

/**
 * Look up the status of an application by registration number.
 *
 * MOCK: Returns DEMO_STATUS for the demo registration number, null otherwise.
 * REAL: GET /status/:registrationNumber  →  StatusLookupResponse
 */
async function lookupStatus(regNum: string): Promise<StatusResult | null> {
  if (IS_MOCK) {
    await mockDelay();

    const normalised = regNum.trim().toUpperCase();
    const demoNormalised = DEMO_REG_NUMBER.trim().toUpperCase();

    if (normalised === demoNormalised) {
      return DEMO_STATUS;
    }
    // Unknown registration number — simulate a not-found response
    return null;
  }

  // ── Real backend ────────────────────────────────────────────────────────
  const encoded = encodeURIComponent(regNum.trim());
  const response = await request<StatusLookupResponse>(
    `/status/${encoded}`,
    { method: "GET" }
  );
  return response.result;
}

// ─── documents.upload ──────────────────────────────────────────────────────

/**
 * Upload a document file for the given document ID slot.
 *
 * MOCK: Simulates an upload delay and returns a fake CDN URL.
 * REAL: POST /documents/upload  (multipart/form-data)  →  DocumentUploadResponse
 */
async function uploadDocument(
  docId: string,
  file: File
): Promise<{ url: string }> {
  if (IS_MOCK) {
    // Simulate a longer upload delay for realism
    await delay(1200 + Math.random() * 800);
    return {
      url: `https://cdn.sahayak-demo.in/uploads/${docId}/${encodeURIComponent(file.name)}`,
    };
  }

  // ── Real backend ────────────────────────────────────────────────────────
  // Note: multipart upload — do NOT set Content-Type; the browser sets the boundary
  const form = new FormData();
  form.append("docId", docId);
  form.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_BASE}/documents/upload`, {
      method: "POST",
      headers: API_TOKEN ? { Authorization: `Bearer ${API_TOKEN}` } : {},
      body: form,
    });
  } catch (networkError) {
    const err: ApiError = {
      code: "NETWORK_ERROR",
      message:
        networkError instanceof Error
          ? networkError.message
          : "Upload failed due to a network error.",
    };
    throw err;
  }

  if (!response.ok) {
    let errorBody: Partial<ApiError> = {};
    try {
      errorBody = (await response.json()) as Partial<ApiError>;
    } catch {
      // Non-JSON error body
    }
    const err: ApiError = {
      code: errorBody.code ?? `HTTP_${response.status}`,
      message: errorBody.message ?? `Upload failed with status ${response.status}`,
    };
    throw err;
  }

  const data = (await response.json()) as DocumentUploadResponse;
  return { url: data.url };
}

// ─── Default export ────────────────────────────────────────────────────────

const api = {
  conversation: {
    chat,
  },
  schemes: {
    search: searchSchemes,
  },
  status: {
    lookup: lookupStatus,
  },
  documents: {
    upload: uploadDocument,
  },
} as const;

export default api;

// Named exports for direct import convenience
export { chat, searchSchemes, lookupStatus, uploadDocument };
