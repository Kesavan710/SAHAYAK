import type {
  Lang,
  ConvStep,
  Scheme,
  DocumentItem,
  ApplicationSummary,
  StatusResult,
} from "@/types";

// ─── Languages ─────────────────────────────────────────────────────────────

export const LANGUAGES: Lang[] = [
  { code: "en", name: "English",   native: "English"    },
  { code: "kn", name: "Kannada",   native: "ಕನ್ನಡ"       },
  { code: "hi", name: "Hindi",     native: "हिन्दी"       },
  { code: "ta", name: "Tamil",     native: "தமிழ்"       },
  { code: "te", name: "Telugu",    native: "తెలుగు"      },
  { code: "mr", name: "Marathi",   native: "मराठी"       },
  { code: "bn", name: "Bengali",   native: "বাংলা"       },
  { code: "ml", name: "Malayalam", native: "മലയാളം"     },
];

// ─── Conversation Steps ────────────────────────────────────────────────────

export const CONV_STEPS: ConvStep[] = [
  {
    id: "step-state",
    agentText:
      "Namaste! I am Sahayak, your government scheme assistant. To find schemes you are eligible for, let me ask a few quick questions. First — which state do you live in?",
    inputType: "chips",
    options: [
      "Karnataka",
      "Maharashtra",
      "Tamil Nadu",
      "Uttar Pradesh",
      "West Bengal",
      "Rajasthan",
      "Andhra Pradesh",
      "Kerala",
      "Gujarat",
      "Madhya Pradesh",
      "Other",
    ],
    progressLabel: "Your State",
  },
  {
    id: "step-disability",
    agentText:
      "Thank you. What type of disability does the applicant have? This helps me match the correct central and state schemes.",
    inputType: "chips",
    options: [
      "Visual Impairment",
      "Hearing Impairment",
      "Locomotor Disability",
      "Intellectual Disability",
      "Multiple Disabilities",
      "Chronic Neurological Condition",
      "Other / Not Listed",
    ],
    progressLabel: "Disability Type",
  },
  {
    id: "step-income",
    agentText:
      "Almost done. What is the approximate annual household income? Many schemes have income-based eligibility (Below Poverty Line, EWS, etc.).",
    inputType: "chips",
    options: [
      "Below ₹1,00,000 (BPL)",
      "₹1,00,000 – ₹2,50,000",
      "₹2,50,000 – ₹5,00,000",
      "₹5,00,000 – ₹8,00,000",
      "Above ₹8,00,000",
    ],
    progressLabel: "Annual Income",
  },
  {
    id: "step-loading",
    agentText:
      "Perfect — analysing your profile against 200+ central and state government schemes. This will take just a moment…",
    inputType: "loading",
    options: [],
    progressLabel: "Analysing",
  },
];

// ─── Waveform Heights ──────────────────────────────────────────────────────

/**
 * 32 deterministic bar heights (px) for the voice waveform animation.
 * Generated once to avoid layout jitter between renders.
 */
export const WAVEFORM_HEIGHTS: number[] = [
  14, 22, 18, 30, 12, 26, 20, 34, 16, 28, 24, 10, 32, 18, 14, 26,
  20, 34, 12, 22, 30, 16, 28, 10, 24, 18, 32, 14, 26, 20, 34, 12,
];

// ─── Mock Schemes ──────────────────────────────────────────────────────────

export const MOCK_SCHEMES: Scheme[] = [
  // ── Scheme 1: Eligible ──────────────────────────────────────────────────
  {
    id: "scheme-dpsp",
    name: "PM Viklang Samman Pension Yojana",
    category: "Disability Support",
    ministry: "Ministry of Social Justice and Empowerment",
    eligible: true,
    matchReasons: [
      "Applicant has a certified disability of ≥40% — meets the minimum threshold",
      "Annual household income is below ₹2,50,000 — within BPL/EWS limit",
      "Karnataka is a participating state under the National Social Assistance Programme",
      "Age is within the 18–79 year eligible bracket",
    ],
    benefits: [
      "Monthly pension of ₹300 (central component) + ₹500 (Karnataka state top-up) = ₹800/month",
      "Direct Benefit Transfer (DBT) to linked bank account or Jan Dhan account",
      "Annual health check-up camp linkage through Aarogya Maitri initiative",
      "Priority enrolment in Pradhan Mantri Jeevan Jyoti Bima Yojana at subsidised premium",
    ],
    requiredDocuments: [
      "Aadhaar Card",
      "Disability Certificate (UDID) with ≥40% disability benchmark",
      "BPL Ration Card or Income Certificate from Tahsildar",
      "Bank passbook / Jan Dhan account details",
      "Passport-size photograph",
    ],
    officialUrl: "https://socialjustice.gov.in/schemes/21",
    sourceDoc: "NSAP Guidelines 2023-24, MoSJE Circular No. 16-1/2023-DD.III",
    lastUpdated: "2024-03-15",
  },

  // ── Scheme 2: Eligible ──────────────────────────────────────────────────
  {
    id: "scheme-sugamya",
    name: "Sugamya Bharat Abhiyan – Accessible India Campaign",
    category: "Accessibility & Infrastructure",
    ministry: "Department of Empowerment of Persons with Disabilities (DEPwD)",
    eligible: true,
    matchReasons: [
      "Person with locomotor/visual disability qualifies for assistive device grant component",
      "Karnataka has active District Implementation Units under this campaign",
      "Household income below ₹2,50,000 makes applicant eligible for fully subsidised devices",
    ],
    benefits: [
      "Free or heavily subsidised assistive devices (wheelchair, crutches, hearing aids, Braille kits)",
      "Retrofitting of home and local public spaces with accessibility ramps and tactile paths",
      "Skill development training under SIPDA for livelihood enhancement",
      "Access to free legal aid services via District Legal Services Authority",
    ],
    requiredDocuments: [
      "UDID Card or Disability Certificate issued by CMO/District Hospital",
      "Aadhaar Card",
      "Domicile / Residence Certificate",
      "Income Certificate from Tahsildar (for subsidy calculation)",
      "Recent photograph",
    ],
    officialUrl: "https://accessibleindia.gov.in",
    sourceDoc:
      "Sugamya Bharat Abhiyan Phase-III Implementation Manual, DEPwD (2023)",
    lastUpdated: "2024-01-20",
  },

  // ── Scheme 3: Not Eligible ───────────────────────────────────────────────
  {
    id: "scheme-pmay-ews",
    name: "Pradhan Mantri Awas Yojana – EWS/LIG Component",
    category: "Housing",
    ministry: "Ministry of Housing and Urban Affairs",
    eligible: false,
    notEligibleReason:
      "Annual household income exceeds ₹3,00,000 (EWS ceiling). Applicant may qualify under the LIG slab (₹3–6 lakh) but additional verification of existing property ownership is required. Urban local body records show a pucca dwelling registered in the family name, which disqualifies under the 'no-pucca-house' criterion.",
    matchReasons: [],
    benefits: [
      "Central assistance of up to ₹1.5 lakh for new construction or enhancement",
      "Interest subsidy of 6.5% per annum on housing loan up to ₹6 lakh under CLSS",
      "Preference given to women beneficiaries, SCs/STs, and PwD applicants in allotment",
      "Convergence with Swachh Bharat Mission for sanitation infrastructure",
    ],
    requiredDocuments: [
      "Aadhaar Card (all adult family members)",
      "Income Certificate",
      "Property / Land ownership documents",
      "Self-declaration of 'no pucca house'",
      "Bank account details for DBT",
      "Caste certificate (if applicable)",
    ],
    officialUrl: "https://pmaymis.gov.in",
    sourceDoc:
      "PMAY-Urban Scheme Guidelines 2022 (Revised), MoHUA Circular HFA-13/1/2022",
    lastUpdated: "2024-02-28",
  },
];

// ─── Demo Documents ────────────────────────────────────────────────────────

/** Documents the applicant already has */
export const DEMO_HAVE_DOCS: DocumentItem[] = [
  {
    id: "doc-aadhaar",
    label: "Aadhaar Card",
    note: "Both sides of the physical card or e-Aadhaar PDF are accepted.",
    status: "available",
  },
  {
    id: "doc-disability-cert",
    label: "Disability Certificate (UDID)",
    note: "Issued by the Chief Medical Officer or authorised District Hospital. Must show ≥40% disability benchmark.",
    status: "available",
  },
  {
    id: "doc-income-cert",
    label: "Income Certificate",
    note: "Issued by Tahsildar / Revenue Department, valid for the current financial year.",
    status: "available",
  },
];

/** Documents the applicant still needs to obtain */
export const DEMO_NEED_DOCS: DocumentItem[] = [
  {
    id: "doc-residence-cert",
    label: "Residence / Domicile Certificate",
    note: "Obtain from your local Gram Panchayat or Ward Office. Processing typically takes 3–7 working days.",
    status: "missing",
  },
  {
    id: "doc-bank-passbook",
    label: "Bank Passbook (first page)",
    note: "Must clearly show account holder name, account number, IFSC, and branch. Jan Dhan accounts are accepted.",
    status: "missing",
  },
];

// ─── Demo Application Summary ──────────────────────────────────────────────

export const DEMO_APPLICATION: ApplicationSummary = {
  name: "Ravi Kumar B.",
  dob: "1989-04-12",
  state: "Karnataka",
  district: "Tumkur",
  education: "Secondary School Certificate (SSLC)",
  disability: "Locomotor Disability (Left Lower Limb) — 55%",
  income: "₹1,44,000 per annum",
  scheme: "PM Viklang Samman Pension Yojana",
  applicationId: "KA-DPSP-2024-088321",
};

// ─── Demo Status Result ────────────────────────────────────────────────────

export const DEMO_REG_NUMBER = "DPSP/2024/KA/007423";

export const DEMO_STATUS: StatusResult = {
  registrationNumber: DEMO_REG_NUMBER,
  scheme: "PM Viklang Samman Pension Yojana",
  state: "Karnataka",
  currentStatus: "approved",
  lastUpdated: "2024-07-10",
  timeline: [
    {
      label: "Application Submitted",
      date: "12 Apr 2024",
      done: true,
      active: false,
    },
    {
      label: "Document Verification",
      date: "24 Apr 2024",
      done: true,
      active: false,
    },
    {
      label: "Field Enquiry by Social Worker",
      date: "09 May 2024",
      done: true,
      active: false,
    },
    {
      label: "Approved by District Welfare Officer",
      date: "10 Jul 2024",
      done: true,
      active: true,
    },
    {
      label: "First Pension Disbursed to Bank Account",
      date: "",
      done: false,
      active: false,
    },
  ],
  officialSource: "https://socialjustice.gov.in/schemes/21",
};
