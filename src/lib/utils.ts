import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind class strings, resolving conflicts via tailwind-merge
 * and handling conditional classes via clsx.
 *
 * @example
 *   cn("px-4 py-2", isActive && "bg-blue-600", className)
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Returns a promise that resolves after `ms` milliseconds.
 * Used to simulate network latency in mock API calls.
 */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const MONTH_NAMES = [
  "January", "February", "March",     "April",   "May",      "June",
  "July",    "August",   "September", "October", "November", "December",
] as const;

/**
 * Format a Date object as a human-readable string.
 *
 * @example
 *   formatDate(new Date("2026-08-18")) // "18 August 2026"
 */
export function formatDate(d: Date): string {
  const day   = d.getDate();
  const month = MONTH_NAMES[d.getMonth()];
  const year  = d.getFullYear();
  return `${day} ${month} ${year}`;
}

/**
 * Truncate `str` to at most `n` characters, appending "…" if trimmed.
 *
 * @example
 *   truncate("Hello world", 7) // "Hello w…"
 */
export function truncate(str: string, n: number): string {
  if (str.length <= n) return str;
  return str.slice(0, n) + "…";
}

/**
 * Generate a short, URL-safe unique ID.
 * Uses crypto.randomUUID when available, falling back to Math.random.
 *
 * @example
 *   generateId() // "k7x9qm2p"
 */
export function generateId(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    // Take first 8 characters of a UUID v4 (sufficiently unique for UI keys)
    return crypto.randomUUID().replace(/-/g, "").slice(0, 8);
  }
  // Fallback for environments without Web Crypto API
  return Math.random().toString(36).slice(2, 10);
}
