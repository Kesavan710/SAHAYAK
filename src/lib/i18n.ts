// UI translations keyed by language code.
// Falls back to "en" for any missing string.

export interface Translations {
  // Navigation
  navHome: string;
  navConversation: string;
  navSchemes: string;
  navDocuments: string;
  navApplication: string;
  navStatus: string;
  brandDescriptor: string;

  // Home
  heroTitle: string;
  heroSubtitle: string;
  tapToSpeak: string;
  youCanType: string;
  homeInputPlaceholder: string;
  listeningLabel: string;
  thinkingLabel: string;
  speakingLabel: string;
  replayLabel: string;
  quickChips: [string, string, string, string];

  // Trust strip
  trust1Title: string;
  trust1Desc: string;
  trust2Title: string;
  trust2Desc: string;
  trust3Title: string;
  trust3Desc: string;

  // Conversation
  convListening: string;
  convThinking: string;
  convRecognised: string;
  convUseAnswer: string;
  convEdit: string;
  convRetry: string;
  convQuickSelect: string;
  convSpeakAnswer: string;
  convTypeAnswer: string;
  convTypePlaceholder: string;
  convSend: string;
  convDetailsCollected: (done: number, total: number) => string;

  // Schemes
  schemesTitle: string;
  schemesSubtitle: string;
  schemesSource: string;
  eligible: string;
  notEligible: string;
  whyMatches: string;
  benefitsLabel: string;
  officialSource: string;
  viewDocs: string;
  viewSource: string;

  // Documents
  docsTitle: string;
  docsSubtitle: string;
  youHave: string;
  stillNeeded: string;
  docsReady: (done: number, total: number) => string;
  continueBtn: string;

  // Application
  appTitle: string;
  safetyHeading: string;
  safetyBody: string;
  safetyWarning: string;
  downloadBtn: string;
  downloadDesc: string;
  checkStatusBtn: string;

  // Status
  statusTitle: string;
  statusSubtitle: string;
  regPlaceholder: string;
  checkBtn: string;
  timelineLabel: string;
  lastUpdated: string;
  officialPortal: string;
  notFoundTitle: string;
  notFoundDesc: string;

  // Accessibility panel
  a11yTitle: string;
  textSizeLabel: string;
  highContrastLabel: string;
  reduceMotionLabel: string;
  readAloudLabel: string;
  voiceFirstLabel: string;
  languageLabel: string;

  // Conversation step texts
  convStep0: string;
  convStep1: string;
  convStep2: string;
  convStep3: string;
}

const en: Translations = {
  navHome: "Home",
  navConversation: "My Conversation",
  navSchemes: "Schemes",
  navDocuments: "Documents",
  navApplication: "Application",
  navStatus: "Status",
  brandDescriptor: "Government Access, Simplified",

  heroTitle: "How can we help you today?",
  heroSubtitle: "Ask Sahayak in your language. You can speak or type — one step at a time.",
  tapToSpeak: "Tap to speak",
  youCanType: "You can also type your request below.",
  homeInputPlaceholder: "Tell Sahayak what you need…",
  listeningLabel: "Listening…",
  thinkingLabel: "Sahayak is thinking…",
  speakingLabel: "Sahayak is speaking",
  replayLabel: "Replay",
  quickChips: [
    "What government schemes can I apply for?",
    "Am I eligible for disability benefits?",
    "What documents do I need?",
    "Check my application status",
  ],

  trust1Title: "Privacy-first",
  trust1Desc: "Your sensitive credentials stay with you.",
  trust2Title: "Accessibility-first",
  trust2Desc: "Designed for different ways of interacting.",
  trust3Title: "Official sources",
  trust3Desc: "Eligibility information is linked to official sources.",

  convListening: "Listening…",
  convThinking: "Sahayak is thinking…",
  convRecognised: "Recognised:",
  convUseAnswer: "Use this answer",
  convEdit: "Edit",
  convRetry: "Retry",
  convQuickSelect: "Quick select",
  convSpeakAnswer: "Speak your answer",
  convTypeAnswer: "or type",
  convTypePlaceholder: "Type your answer…",
  convSend: "Send",
  convDetailsCollected: (done, total) => `${done} of ${total} details collected`,

  schemesTitle: "Schemes that may be relevant to you",
  schemesSubtitle: "Based on the information you shared with Sahayak.",
  schemesSource: "Eligibility information is based on available scheme data and official sources.",
  eligible: "Eligible",
  notEligible: "Not eligible",
  whyMatches: "Why this matches",
  benefitsLabel: "Benefits",
  officialSource: "Official source",
  viewDocs: "View required documents",
  viewSource: "View official source",

  docsTitle: "Get your documents ready",
  docsSubtitle: "Sahayak has checked what you already have and what is still needed.",
  youHave: "You have",
  stillNeeded: "Still needed",
  docsReady: (done, total) => `${done} of ${total} documents ready`,
  continueBtn: "Continue to Application Package",

  appTitle: "Your application package is ready",
  safetyHeading: "Important — Sahayak has not submitted this application",
  safetyBody: "You must complete government login, OTP verification and CAPTCHA steps yourself on the official portal.",
  safetyWarning: "Never share your UPI PIN, password or Aadhaar OTP with anyone.",
  downloadBtn: "Download application package",
  downloadDesc: "Your prepared information and checklist are included.",
  checkStatusBtn: "Check application status",

  statusTitle: "Check your application status",
  statusSubtitle: "Enter your registration number to see the current status and timeline.",
  regPlaceholder: "e.g. DPSP/2024/KA/007423",
  checkBtn: "Check status",
  timelineLabel: "Application Timeline",
  lastUpdated: "Last updated",
  officialPortal: "Source: Official government portal",
  notFoundTitle: "Application not found",
  notFoundDesc: "Check the registration number and try again.",

  a11yTitle: "Accessibility",
  textSizeLabel: "Text Size",
  highContrastLabel: "High contrast",
  reduceMotionLabel: "Reduce motion",
  readAloudLabel: "Read aloud",
  voiceFirstLabel: "Voice-first mode",
  languageLabel: "Language",

  convStep0: "Namaste! I am Sahayak, your government scheme assistant. To find schemes you are eligible for, let me ask a few quick questions. First — which state do you live in?",
  convStep1: "Thank you. What type of disability does the applicant have? This helps me match the correct central and state schemes.",
  convStep2: "Got it. What is the approximate annual household income?",
  convStep3: "Thank you! Let me find the schemes that are most relevant for you. This will just take a moment…",
};

const kn: Translations = {
  ...en,
  navHome: "ಮುಖಪುಟ",
  navConversation: "ನನ್ನ ಸಂಭಾಷಣೆ",
  navSchemes: "ಯೋಜನೆಗಳು",
  navDocuments: "ದಾಖಲೆಗಳು",
  navApplication: "ಅರ್ಜಿ",
  navStatus: "ಸ್ಥಿತಿ",
  brandDescriptor: "ಸರ್ಕಾರಿ ಸೇವೆ, ಸರಳವಾಗಿ",

  heroTitle: "ಇಂದು ನಾವು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
  heroSubtitle: "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಸಹಾಯಕ್‌ ಕೇಳಿ. ಮಾತನಾಡಬಹುದು ಅಥವಾ ಟೈಪ್ ಮಾಡಬಹುದು — ಒಂದೊಂದೇ ಹೆಜ್ಜೆ.",
  tapToSpeak: "ಮಾತನಾಡಲು ಒತ್ತಿ",
  youCanType: "ನೀವು ಕೆಳಗೆ ಟೈಪ್ ಮಾಡಬಹುದು.",
  homeInputPlaceholder: "ಸಹಾಯಕ್‌ಗೆ ನಿಮ್ಮ ಅಗತ್ಯ ತಿಳಿಸಿ…",
  listeningLabel: "ಆಲಿಸುತ್ತಿದ್ದೇನೆ…",
  thinkingLabel: "ಸಹಾಯಕ್ ಯೋಚಿಸುತ್ತಿದ್ದಾರೆ…",
  speakingLabel: "ಸಹಾಯಕ್ ಮಾತನಾಡುತ್ತಿದ್ದಾರೆ",
  replayLabel: "ಮತ್ತೆ ಕೇಳಿ",
  quickChips: [
    "ನಾನು ಯಾವ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು?",
    "ನಾನು ಅಂಗವಿಕಲ ಸೌಲಭ್ಯಕ್ಕೆ ಅರ್ಹನೇ?",
    "ನನಗೆ ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?",
    "ನನ್ನ ಅರ್ಜಿ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ",
  ],

  trust1Title: "ಗೌಪ್ಯತೆ ಮೊದಲು",
  trust1Desc: "ನಿಮ್ಮ ಸೂಕ್ಷ್ಮ ಮಾಹಿತಿ ನಿಮ್ಮ ಬಳಿಯೇ ಇರುತ್ತದೆ.",
  trust2Title: "ಅಂಗವಿಕಲರ ಅನುಕೂಲ",
  trust2Desc: "ವಿವಿಧ ರೀತಿಯ ಸಂವಹನಕ್ಕೆ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.",
  trust3Title: "ಅಧಿಕೃತ ಮೂಲಗಳು",
  trust3Desc: "ಅರ್ಹತೆಯ ಮಾಹಿತಿ ಅಧಿಕೃತ ಮೂಲಗಳಿಗೆ ಸಂಪರ್ಕಿಸಲಾಗಿದೆ.",

  convListening: "ಆಲಿಸುತ್ತಿದ್ದೇನೆ…",
  convThinking: "ಸಹಾಯಕ್ ಯೋಚಿಸುತ್ತಿದ್ದಾರೆ…",
  convRecognised: "ಗ್ರಹಿಸಲಾಗಿದೆ:",
  convUseAnswer: "ಈ ಉತ್ತರ ಬಳಸಿ",
  convEdit: "ತಿದ್ದು",
  convRetry: "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ",
  convQuickSelect: "ತ್ವರಿತ ಆಯ್ಕೆ",
  convSpeakAnswer: "ನಿಮ್ಮ ಉತ್ತರ ಹೇಳಿ",
  convTypeAnswer: "ಅಥವಾ ಟೈಪ್ ಮಾಡಿ",
  convTypePlaceholder: "ನಿಮ್ಮ ಉತ್ತರ ಟೈಪ್ ಮಾಡಿ…",
  convSend: "ಕಳಿಸಿ",
  convDetailsCollected: (done, total) => `${total} ರಲ್ಲಿ ${done} ವಿವರಗಳು ಸಂಗ್ರಹಿಸಲಾಗಿದೆ`,

  schemesTitle: "ನಿಮಗೆ ಸಂಬಂಧಿತ ಯೋಜನೆಗಳು",
  schemesSubtitle: "ನೀವು ಸಹಾಯಕ್‌ಗೆ ಹಂಚಿಕೊಂಡ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ.",
  schemesSource: "ಅರ್ಹತೆ ಮಾಹಿತಿ ಲಭ್ಯ ಯೋಜನೆ ಡೇಟಾ ಮತ್ತು ಅಧಿಕೃತ ಮೂಲಗಳ ಆಧಾರದ ಮೇಲಿದೆ.",
  eligible: "ಅರ್ಹ",
  notEligible: "ಅರ್ಹರಲ್ಲ",
  whyMatches: "ಏಕೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆ",
  benefitsLabel: "ಪ್ರಯೋಜನಗಳು",
  officialSource: "ಅಧಿಕೃತ ಮೂಲ",
  viewDocs: "ಅಗತ್ಯ ದಾಖಲೆಗಳು ವೀಕ್ಷಿಸಿ",
  viewSource: "ಅಧಿಕೃತ ಮೂಲ ವೀಕ್ಷಿಸಿ",

  docsTitle: "ನಿಮ್ಮ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ",
  docsSubtitle: "ಸಹಾಯಕ್ ನೀವು ಈಗಾಗಲೇ ಏನು ಹೊಂದಿದ್ದೀರಿ ಮತ್ತು ಏನು ಬೇಕು ಎಂದು ಪರಿಶೀಲಿಸಿದ್ದಾರೆ.",
  youHave: "ನಿಮ್ಮ ಬಳಿ ಇದೆ",
  stillNeeded: "ಇನ್ನೂ ಬೇಕಾಗಿದೆ",
  docsReady: (done, total) => `${total} ರಲ್ಲಿ ${done} ದಾಖಲೆಗಳು ಸಿದ್ಧ`,
  continueBtn: "ಅರ್ಜಿ ಪ್ಯಾಕೇಜ್‌ಗೆ ಮುಂದುವರಿಯಿರಿ",

  appTitle: "ನಿಮ್ಮ ಅರ್ಜಿ ಪ್ಯಾಕೇಜ್ ಸಿದ್ಧವಾಗಿದೆ",
  safetyHeading: "ಮುಖ್ಯ — ಸಹಾಯಕ್ ಈ ಅರ್ಜಿ ಸಲ್ಲಿಸಿಲ್ಲ",
  safetyBody: "ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಸರ್ಕಾರಿ ಲಾಗಿನ್, OTP ಪರಿಶೀಲನೆ ಮತ್ತು CAPTCHA ಹಂತಗಳನ್ನು ನೀವೇ ಪೂರ್ಣಗೊಳಿಸಬೇಕು.",
  safetyWarning: "ನಿಮ್ಮ UPI PIN, ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ ಆಧಾರ್ OTP ಯಾರಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
  downloadBtn: "ಅರ್ಜಿ ಪ್ಯಾಕೇಜ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
  downloadDesc: "ನಿಮ್ಮ ಸಿದ್ಧಪಡಿಸಿದ ಮಾಹಿತಿ ಮತ್ತು ಚೆಕ್‌ಲಿಸ್ಟ್ ಸೇರಿದೆ.",
  checkStatusBtn: "ಅರ್ಜಿ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ",

  statusTitle: "ನಿಮ್ಮ ಅರ್ಜಿ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ",
  statusSubtitle: "ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ ಮತ್ತು ಟೈಮ್‌ಲೈನ್ ನೋಡಲು ನೋಂದಣಿ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.",
  regPlaceholder: "ಉದಾ. DPSP/2024/KA/007423",
  checkBtn: "ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ",
  timelineLabel: "ಅರ್ಜಿ ಟೈಮ್‌ಲೈನ್",
  lastUpdated: "ಕೊನೆಯ ನವೀಕರಣ",
  officialPortal: "ಮೂಲ: ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್",
  notFoundTitle: "ಅರ್ಜಿ ಕಂಡುಬಂದಿಲ್ಲ",
  notFoundDesc: "ನೋಂದಣಿ ಸಂಖ್ಯೆ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",

  a11yTitle: "ಅಂಗವಿಕಲ ಅನುಕೂಲ",
  textSizeLabel: "ಅಕ್ಷರ ಗಾತ್ರ",
  highContrastLabel: "ಹೆಚ್ಚಿನ ವ್ಯತಿರಿಕ್ತತೆ",
  reduceMotionLabel: "ಚಲನೆ ಕಡಿಮೆ ಮಾಡಿ",
  readAloudLabel: "ಜೋರಾಗಿ ಓದಿ",
  voiceFirstLabel: "ಧ್ವನಿ-ಮೊದಲ ಮೋಡ್",
  languageLabel: "ಭಾಷೆ",

  convStep0: "ನಮಸ್ತೆ! ನಾನು ಸಹಾಯಕ್, ನಿಮ್ಮ ಸರ್ಕಾರಿ ಯೋಜನೆ ಸಹಾಯಕ. ನಿಮಗೆ ಅರ್ಹ ಯೋಜನೆಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಕೆಲವು ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಲಿದ್ದೇನೆ. ಮೊದಲು — ನೀವು ಯಾವ ರಾಜ್ಯದಲ್ಲಿ ವಾಸಿಸುತ್ತೀರಿ?",
  convStep1: "ಧನ್ಯವಾದ. ಅರ್ಜಿದಾರರಿಗೆ ಯಾವ ರೀತಿಯ ಅಂಗವೈಕಲ್ಯ ಇದೆ? ಇದು ಸರಿಯಾದ ಯೋಜನೆಗಳನ್ನು ಹೊಂದಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
  convStep2: "ಅರ್ಥ ಆಯಿತು. ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ ಎಷ್ಟು?",
  convStep3: "ಧನ್ಯವಾದ! ನಿಮಗೆ ಸೂಕ್ತ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕುತ್ತಿದ್ದೇನೆ. ಸ್ವಲ್ಪ ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತದೆ…",
};

const hi: Translations = {
  ...en,
  navHome: "होम",
  navConversation: "मेरी बातचीत",
  navSchemes: "योजनाएं",
  navDocuments: "दस्तावेज़",
  navApplication: "आवेदन",
  navStatus: "स्थिति",
  brandDescriptor: "सरकारी सेवा, सरल तरीके से",

  heroTitle: "आज हम आपकी कैसे मदद कर सकते हैं?",
  heroSubtitle: "अपनी भाषा में सहायक से पूछें। आप बोल या टाइप कर सकते हैं — एक कदम एक बार।",
  tapToSpeak: "बोलने के लिए टैप करें",
  youCanType: "आप नीचे टाइप भी कर सकते हैं।",
  homeInputPlaceholder: "सहायक को बताएं आपको क्या चाहिए…",
  listeningLabel: "सुन रहा हूं…",
  thinkingLabel: "सहायक सोच रहा है…",
  speakingLabel: "सहायक बोल रहा है",
  replayLabel: "फिर से सुनें",
  quickChips: [
    "मैं किन सरकारी योजनाओं के लिए आवेदन कर सकता हूं?",
    "क्या मैं विकलांगता लाभ के लिए पात्र हूं?",
    "मुझे कौन से दस्तावेज़ चाहिए?",
    "मेरी आवेदन स्थिति जांचें",
  ],

  trust1Title: "गोपनीयता प्रथम",
  trust1Desc: "आपकी संवेदनशील जानकारी आपके पास ही रहती है।",
  trust2Title: "सुलभता प्रथम",
  trust2Desc: "विभिन्न प्रकार के इंटरेक्शन के लिए डिज़ाइन किया गया।",
  trust3Title: "आधिकारिक स्रोत",
  trust3Desc: "पात्रता की जानकारी आधिकारिक स्रोतों से जुड़ी है।",

  convListening: "सुन रहा हूं…",
  convThinking: "सहायक सोच रहा है…",
  convRecognised: "पहचाना गया:",
  convUseAnswer: "इस उत्तर का उपयोग करें",
  convEdit: "संपादित करें",
  convRetry: "फिर प्रयास करें",
  convQuickSelect: "त्वरित चुनाव",
  convSpeakAnswer: "अपना उत्तर बोलें",
  convTypeAnswer: "या टाइप करें",
  convTypePlaceholder: "अपना उत्तर टाइप करें…",
  convSend: "भेजें",
  convDetailsCollected: (done, total) => `${total} में से ${done} विवरण एकत्र किए`,

  schemesTitle: "आपसे संबंधित योजनाएं",
  schemesSubtitle: "आपके द्वारा सहायक के साथ साझा की गई जानकारी के आधार पर।",
  schemesSource: "पात्रता की जानकारी उपलब्ध योजना डेटा और आधिकारिक स्रोतों पर आधारित है।",
  eligible: "पात्र",
  notEligible: "अपात्र",
  whyMatches: "यह क्यों मेल खाता है",
  benefitsLabel: "लाभ",
  officialSource: "आधिकारिक स्रोत",
  viewDocs: "आवश्यक दस्तावेज़ देखें",
  viewSource: "आधिकारिक स्रोत देखें",

  docsTitle: "अपने दस्तावेज़ तैयार करें",
  docsSubtitle: "सहायक ने जांचा है कि आपके पास क्या है और क्या अभी भी चाहिए।",
  youHave: "आपके पास है",
  stillNeeded: "अभी भी चाहिए",
  docsReady: (done, total) => `${total} में से ${done} दस्तावेज़ तैयार`,
  continueBtn: "आवेदन पैकेज पर जारी रखें",

  appTitle: "आपका आवेदन पैकेज तैयार है",
  safetyHeading: "महत्वपूर्ण — सहायक ने यह आवेदन जमा नहीं किया है",
  safetyBody: "आपको आधिकारिक पोर्टल पर स्वयं सरकारी लॉगिन, OTP सत्यापन और CAPTCHA चरण पूरे करने होंगे।",
  safetyWarning: "अपना UPI PIN, पासवर्ड या आधार OTP किसी के साथ साझा न करें।",
  downloadBtn: "आवेदन पैकेज डाउनलोड करें",
  downloadDesc: "आपकी तैयार जानकारी और चेकलिस्ट शामिल है।",
  checkStatusBtn: "आवेदन स्थिति जांचें",

  statusTitle: "अपनी आवेदन स्थिति जांचें",
  statusSubtitle: "वर्तमान स्थिति और समयरेखा देखने के लिए पंजीकरण संख्या दर्ज करें।",
  regPlaceholder: "उदा. DPSP/2024/KA/007423",
  checkBtn: "स्थिति जांचें",
  timelineLabel: "आवेदन समयरेखा",
  lastUpdated: "अंतिम अपडेट",
  officialPortal: "स्रोत: आधिकारिक सरकारी पोर्टल",
  notFoundTitle: "आवेदन नहीं मिला",
  notFoundDesc: "पंजीकरण संख्या जांचें और फिर प्रयास करें।",

  a11yTitle: "सुलभता",
  textSizeLabel: "टेक्स्ट आकार",
  highContrastLabel: "उच्च कंट्रास्ट",
  reduceMotionLabel: "गति कम करें",
  readAloudLabel: "ज़ोर से पढ़ें",
  voiceFirstLabel: "आवाज़-प्रथम मोड",
  languageLabel: "भाषा",

  convStep0: "नमस्ते! मैं सहायक हूं, आपका सरकारी योजना सहायक। आपके लिए उपयुक्त योजनाएं खोजने के लिए कुछ त्वरित प्रश्न पूछूंगा। पहला — आप किस राज्य में रहते हैं?",
  convStep1: "धन्यवाद। आवेदक को किस प्रकार की विकलांगता है? यह सही योजनाओं से मिलान करने में मदद करता है।",
  convStep2: "समझ आया। वार्षिक पारिवारिक आय लगभग कितनी है?",
  convStep3: "धन्यवाद! मैं आपके लिए सबसे उपयुक्त योजनाएं खोज रहा हूं। बस एक पल…",
};

const ta: Translations = {
  ...en,
  navHome: "முகப்பு",
  navConversation: "என் உரையாடல்",
  navSchemes: "திட்டங்கள்",
  navDocuments: "ஆவணங்கள்",
  navApplication: "விண்ணப்பம்",
  navStatus: "நிலை",
  brandDescriptor: "அரசு சேவை, எளிமையாக",
  heroTitle: "இன்று நாம் உங்களுக்கு எப்படி உதவலாம்?",
  heroSubtitle: "உங்கள் மொழியில் சஹாயக்கிடம் கேளுங்கள். பேசலாம் அல்லது தட்டச்சு செய்யலாம் — ஒரு படி ஒரு முறை.",
  tapToSpeak: "பேச தட்டவும்",
  youCanType: "கீழே தட்டச்சு செய்யலாம்.",
  homeInputPlaceholder: "சஹாயக்கிடம் உங்கள் தேவையை சொல்லுங்கள்…",
  listeningLabel: "கேட்கிறேன்…",
  thinkingLabel: "சஹாயக் யோசிக்கிறார்…",
  speakingLabel: "சஹாயக் பேசுகிறார்",
  replayLabel: "மீண்டும் கேளுங்கள்",
  eligible: "தகுதியானவர்",
  notEligible: "தகுதியற்றவர்",
  checkBtn: "நிலை சரிபார்க்கவும்",
  notFoundTitle: "விண்ணப்பம் கிடைக்கவில்லை",
  notFoundDesc: "பதிவு எண்ணை சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
  a11yTitle: "அணுகல்தன்மை",
  languageLabel: "மொழி",
};

const te: Translations = {
  ...en,
  navHome: "హోమ్",
  navConversation: "నా సంభాషణ",
  navSchemes: "పథకాలు",
  navDocuments: "పత్రాలు",
  navApplication: "దరఖాస్తు",
  navStatus: "స్థితి",
  brandDescriptor: "ప్రభుత్వ సేవ, సులభంగా",
  heroTitle: "ఈ రోజు మేము మీకు ఎలా సహాయం చేయగలము?",
  heroSubtitle: "మీ భాషలో సహాయక్‌ని అడగండి. మీరు మాట్లాడవచ్చు లేదా టైప్ చేయవచ్చు — ఒక్కో అడుగు.",
  tapToSpeak: "మాట్లాడటానికి నొక్కండి",
  youCanType: "మీరు దిగువన టైప్ చేయవచ్చు.",
  homeInputPlaceholder: "సహాయక్‌కు మీకు ఏమి కావాలో చెప్పండి…",
  listeningLabel: "వింటున్నాను…",
  thinkingLabel: "సహాయక్ ఆలోచిస్తున్నారు…",
  speakingLabel: "సహాయక్ మాట్లాడుతున్నారు",
  replayLabel: "మళ్ళీ వినండి",
  eligible: "అర్హులు",
  notEligible: "అర్హులు కాదు",
  checkBtn: "స్థితి తనిఖీ చేయండి",
  notFoundTitle: "దరఖాస్తు కనుగొనబడలేదు",
  notFoundDesc: "నమోదు సంఖ్య తనిఖీ చేసి మళ్ళీ ప్రయత్నించండి.",
  a11yTitle: "అందుబాటు",
  languageLabel: "భాష",
};

const mr: Translations = {
  ...en,
  navHome: "मुखपृष्ठ",
  navConversation: "माझी संभाषण",
  navSchemes: "योजना",
  navDocuments: "कागदपत्रे",
  navApplication: "अर्ज",
  navStatus: "स्थिती",
  brandDescriptor: "सरकारी सेवा, सोप्या पद्धतीने",
  heroTitle: "आज आम्ही तुम्हाला कशी मदत करू शकतो?",
  heroSubtitle: "तुमच्या भाषेत सहायकला विचारा. बोलू किंवा टाइप करू शकता — एक एक पाऊल.",
  tapToSpeak: "बोलण्यासाठी टॅप करा",
  youCanType: "तुम्ही खाली टाइप देखील करू शकता.",
  homeInputPlaceholder: "सहायकला तुम्हाला काय हवे आहे ते सांगा…",
  listeningLabel: "ऐकत आहे…",
  thinkingLabel: "सहायक विचार करत आहे…",
  speakingLabel: "सहायक बोलत आहे",
  replayLabel: "पुन्हा ऐका",
  eligible: "पात्र",
  notEligible: "अपात्र",
  checkBtn: "स्थिती तपासा",
  notFoundTitle: "अर्ज सापडला नाही",
  notFoundDesc: "नोंदणी क्रमांक तपासा आणि पुन्हा प्रयत्न करा.",
  a11yTitle: "प्रवेशयोग्यता",
  languageLabel: "भाषा",
};

const bn: Translations = {
  ...en,
  navHome: "হোম",
  navConversation: "আমার কথোপকথন",
  navSchemes: "প্রকল্প",
  navDocuments: "নথি",
  navApplication: "আবেদন",
  navStatus: "অবস্থা",
  brandDescriptor: "সরকারি সেবা, সহজভাবে",
  heroTitle: "আজ আমরা আপনাকে কীভাবে সাহায্য করতে পারি?",
  heroSubtitle: "আপনার ভাষায় সহায়ককে জিজ্ঞেস করুন। কথা বলতে বা টাইপ করতে পারেন — এক ধাপ এক সময়।",
  tapToSpeak: "কথা বলতে ট্যাপ করুন",
  youCanType: "আপনি নিচে টাইপ করতে পারেন।",
  homeInputPlaceholder: "সহায়ককে বলুন আপনার কী দরকার…",
  listeningLabel: "শুনছি…",
  thinkingLabel: "সহায়ক ভাবছে…",
  speakingLabel: "সহায়ক বলছে",
  replayLabel: "আবার শুনুন",
  eligible: "যোগ্য",
  notEligible: "অযোগ্য",
  checkBtn: "অবস্থা পরীক্ষা করুন",
  notFoundTitle: "আবেদন পাওয়া যায়নি",
  notFoundDesc: "নিবন্ধন নম্বর পরীক্ষা করুন এবং আবার চেষ্টা করুন।",
  a11yTitle: "অ্যাক্সেসিবিলিটি",
  languageLabel: "ভাষা",
};

const ml: Translations = {
  ...en,
  navHome: "ഹോം",
  navConversation: "എന്റെ സംഭാഷണം",
  navSchemes: "പദ്ധതികൾ",
  navDocuments: "രേഖകൾ",
  navApplication: "അപേക്ഷ",
  navStatus: "നില",
  brandDescriptor: "സർക്കാർ സേവനം, ലളിതമായി",
  heroTitle: "ഇന്ന് ഞങ്ങൾക്ക് നിങ്ങളെ എങ്ങനെ സഹായിക്കാൻ കഴിയും?",
  heroSubtitle: "നിങ്ങളുടെ ഭാഷയിൽ സഹായകിനോട് ചോദിക്കൂ. സംസാരിക്കാം അല്ലെങ്കിൽ ടൈപ്പ് ചെയ്യാം — ഒരു ഘട്ടം ഒരു സമയം.",
  tapToSpeak: "സംസാരിക്കാൻ ടാപ്പ് ചെയ്യുക",
  youCanType: "നിങ്ങൾക്ക് താഴെ ടൈപ്പ് ചെയ്യാം.",
  homeInputPlaceholder: "സഹായകിന് നിങ്ങൾക്ക് എന്ത് വേണമെന്ന് പറയൂ…",
  listeningLabel: "ശ്രദ്ധിക്കുന്നു…",
  thinkingLabel: "സഹായക് ചിന്തിക്കുകയാണ്…",
  speakingLabel: "സഹായക് സംസാരിക്കുകയാണ്",
  replayLabel: "വീണ്ടും കേൾക്കുക",
  eligible: "യോഗ്യൻ",
  notEligible: "അയോഗ്യൻ",
  checkBtn: "നില പരിശോധിക്കുക",
  notFoundTitle: "അപേക്ഷ കണ്ടെത്തിയില്ല",
  notFoundDesc: "രജിസ്ട്രേഷൻ നമ്പർ പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.",
  a11yTitle: "ഉൾക്കൊള്ളൽ",
  languageLabel: "ഭാഷ",
};

const TRANSLATIONS: Record<string, Translations> = { en, kn, hi, ta, te, mr, bn, ml };

export function getT(langCode: string): Translations {
  return TRANSLATIONS[langCode] ?? en;
}
