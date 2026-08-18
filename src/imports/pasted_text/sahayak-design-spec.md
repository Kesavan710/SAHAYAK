# Sahayak — Premium AI-Powered Government Accessibility Agent

Design and prototype a polished, production-quality responsive web application called **Sahayak**.

## 1. Product Vision

Sahayak is a **voice-first government accessibility agent** designed to help citizens discover government schemes, understand eligibility, identify required documents, prepare applications, and check application status.

The product must feel:

* Trustworthy
* Human
* Calm
* Inclusive
* Modern
* Highly accessible
* AI-powered without feeling overly futuristic
* Simple enough for elderly users and people with disabilities
* Premium enough to look like a winning hackathon product

Do NOT design it like a conventional government portal.

Do NOT create a generic chatbot UI.

The design should communicate:

> **“Government services, made simple for everyone.”**

---

# 2. Design Direction

Use a **modern civic-tech + accessible AI** visual language.

### Visual personality

* Minimal
* Warm
* Spacious
* Human-centered
* Premium
* Calm
* High trust
* Accessibility-first

Use a light interface as the primary theme.

### Suggested palette

Primary:

* Deep Navy / Indigo: `#172554`
* Accessible Blue: `#2563EB`

Secondary:

* Teal: `#0F766E`

Background:

* Soft off-white: `#F8FAFC`

Cards:

* `#FFFFFF`

Text:

* Primary: `#0F172A`
* Secondary: `#475569`

Success:

* `#15803D`

Warning:

* `#B45309`

Error:

* `#B91C1C`

Use color carefully. Never communicate meaning through color alone.

---

# 3. Typography

Use **Inter** or another highly legible modern sans-serif.

Hierarchy:

* Large page headings: 40–48px
* Section headings: 28–32px
* Card headings: 20–24px
* Body: 16–18px
* Supporting text: 14–16px
* Buttons: 16px medium/semibold

Prioritize readability over decorative typography.

The UI must work comfortably for elderly users and users with visual/cognitive challenges.

---

# 4. Global Layout

Create a responsive desktop-first application with mobile adaptation.

Desktop:

* Maximum content width around 1200–1280px
* Generous whitespace
* 12-column grid
* Consistent 24px spacing system
* Rounded cards
* Subtle borders
* Very soft shadows

Mobile:

* Single-column layout
* Large touch targets
* Sticky primary action where appropriate
* No dense tables
* No tiny controls

Minimum interactive target:

**44 × 44px**

Primary microphone button:

**minimum 64 × 64px**

---

# 5. Global Navigation

Create a simple top navigation bar.

Left:

**Sahayak logo**

Logo concept:

A subtle combination of:

* Helping hand
* Speech bubble
* Government/civic symbol
* AI spark

Do NOT use an overly complex logo.

Next to logo:

**Sahayak**

Small descriptor:

**Government Access, Simplified**

Navigation:

* Home
* My Conversation
* Schemes
* Documents
* Application
* Status

Right side:

### Language selector

`English ▾`

Options:

* English
* ಕನ್ನಡ
* हिंदी

Then:

### Accessibility button

Icon + text:

**Accessibility**

Opens accessibility controls.

Also include a user/profile icon.

---

# 6. HOME SCREEN — Hero Experience

Create a beautiful, highly focused landing experience.

Do NOT fill the screen with cards.

The primary focus should be:

## “How can we help you today?”

Supporting text:

**Ask Sahayak in your language. You can speak or type — one step at a time.**

### Main interaction

Create a large circular microphone control in the center.

Use a subtle animated AI listening ring around it.

Inside:

🎙 microphone icon

Below:

**Tap to speak**

Secondary text:

**You can also type your request below.**

### Text input

Large accessible input:

**“Tell Sahayak what you need…”**

Right side:

Send button.

### Example prompts

Small suggestion chips:

* “What government schemes can I apply for?”
* “Am I eligible for disability benefits?”
* “What documents do I need?”
* “Check my application status”

Keep these visually secondary.

---

# 7. TRUST STRIP

Below the hero interaction, create a compact trust section.

Three items:

### 🔒 Privacy-first

Your sensitive credentials stay with you.

### ♿ Accessibility-first

Designed for different ways of interacting.

### 🏛 Official sources

Eligibility information is linked to official sources.

This should create confidence without looking like marketing.

---

# 8. CONVERSATION SCREEN

This is the heart of Sahayak.

Create an extremely clean conversational interface.

Left/main area:

Conversation history.

User messages:

Right aligned.

Agent messages:

Left aligned.

Give Sahayak a small friendly AI avatar/icon.

Avoid cartoon-style avatars.

Use a simple abstract assistant symbol.

### Agent message

Example:

**Sahayak**

> “I can help you find schemes you may qualify for. First, what is your state?”

Then show:

### Single-question interaction

Large response control:

**Select your state**

or:

Large text/voice input.

IMPORTANT:

Never display a huge form.

The agent asks **ONE question at a time**.

This is central to the product UX.

---

# 9. VOICE INTERACTION STATE

Design multiple microphone states:

### Idle

Mic icon.

**Tap to speak**

### Listening

Animated concentric rings.

Text:

**Listening…**

### Processing

Small animated AI indicator.

Text:

**Sahayak is thinking…**

### Speaking

Speaker animation.

Text:

**Sahayak is speaking**

Include:

**Replay**

button.

Never rely on audio alone.

Always show the response as text.

---

# 10. CONVERSATION PROGRESS

Add a subtle progress indicator.

Example:

**Understanding your needs**

`● ● ● ○ ○`

Supporting text:

**2 of 5 details collected**

Do not make this feel like a traditional form.

It should feel like a guided conversation.

---

# 11. RESULTS / SCHEME MATCHING SCREEN

Create a premium results page.

Header:

## “Schemes that may be relevant to you”

Supporting text:

**Based on the information you shared with Sahayak.**

Add a small trust label:

**Eligibility information is based on the available scheme data and official sources.**

### Scheme cards

Each card contains:

**Scheme name**

Eligibility badge:

`Eligible`

or

`Not eligible`

Then:

### Why this matches

Use 2–4 concise bullet points.

Example:

✓ Disability percentage requirement met
✓ Income requirement met
✓ Karnataka resident

### Benefits

Display benefits in a clean section.

Example:

**Benefits**

* Monthly financial assistance
* Educational support

### Source

At bottom:

**Official source**

`View official source ↗`

Also display:

**Source document: Government Scheme Guidelines.pdf**

Do not fabricate sources.

---

# 12. SCHEME CARD DESIGN

Cards should feel like premium information panels.

Structure:

Top:
Scheme name + status

Middle:
Why you match

Benefits

Bottom:
Source + action

Primary CTA:

**View required documents**

Secondary:

**View official source**

Eligible cards should be visually prominent.

Not-eligible cards should remain readable and respectful.

Never use red as the only indicator.

---

# 13. DOCUMENTS SCREEN

Title:

## “Get your documents ready”

Subtitle:

**Sahayak has checked what you already have and what is still needed.**

Create two large sections.

### You have

Checklist rows:

✓ Aadhaar Card
✓ Disability Certificate
✓ Income Certificate

### Still needed

Rows:

○ Residence Certificate
○ Bank Passbook

Use clear icons and status labels.

### Progress visualization

Example:

**3 of 5 documents ready**

Large progress bar.

---

# 14. APPLICATION PACKAGE SCREEN

Title:

## “Your application package is ready”

Top:

Large progress indicator.

Example:

**4 / 4 documents ready**

Then:

### Application summary

Clean label/value rows:

Name
Date of Birth
State
District
Education
Disability
Income

Make this read-only.

### Download section

Large premium CTA:

**Download application package**

Supporting text:

**Your prepared information and checklist are included.**

---

# 15. CRITICAL SAFETY NOTICE

This must be extremely visible.

Create a persistent highlighted information panel:

### ⚠️ Important

**Sahayak has not submitted this application.**

You must complete government login, OTP and CAPTCHA steps yourself on the official portal.

Do NOT make this look like an error.

Make it look like a clear safety boundary.

Never design any UI that asks for:

* UPI PIN
* Password
* Aadhaar OTP

---

# 16. APPLICATION STATUS SCREEN

Create a simple, reassuring interface.

Header:

## “Check your application status”

Large input:

**Enter registration number**

Primary button:

**Check status**

After submission:

Create a status timeline.

Example:

`Submitted → Under Review → Approved`

Highlight current status.

Display:

### Current status

**Under Review**

### Last updated

**18 August 2026**

### Source

Official government portal

If not found:

Create a calm empty state:

**Application not found**

> Check the registration number and try again.

Do not speculate about the reason.

---

# 17. ACCESSIBILITY CENTER

Create a dedicated accessibility settings panel.

Controls:

### Text size

`A−  A  A+`

### Contrast

Toggle:

**High contrast**

### Motion

Toggle:

**Reduce motion**

### Reading assistance

Toggle:

**Read responses aloud**

### Interaction

Option:

**Voice-first mode**

### Language

English / ಕನ್ನಡ / हिंदी

The panel itself must be accessible.

---

# 18. MULTILINGUAL UI

Design the UI so it can support:

**English**

**ಕನ್ನಡ**

**हिंदी**

Do not merely put translations in tiny dropdowns.

Ensure layouts can expand for longer text.

Use appropriate typography and spacing.

The selected language should be visually obvious.

---

# 19. EMPTY / LOADING / ERROR STATES

Design polished states for every major screen.

### AI thinking

Animated subtle dots +:

**Sahayak is thinking…**

### Loading schemes

Skeleton cards.

### Network error

> **We couldn't connect to Sahayak.**

Button:

**Try again**

### No scheme matches

> **No matches found in the current scheme set.**

Supporting text:

**You can provide more information or try another request.**

Never imply that Sahayak searched every government scheme.

---

# 20. MICROINTERACTIONS

Use subtle animations only.

Examples:

* Microphone listening pulse
* AI thinking indicator
* Smooth card entrance
* Progress bar animation
* Button hover
* Focus ring
* Status timeline transitions

Avoid excessive glassmorphism, neon effects, gradients or flashy AI animations.

This is a **civic accessibility product**, not a gaming dashboard.

---

# 21. DESIGN SYSTEM

Create reusable Figma components:

### Buttons

* Primary
* Secondary
* Ghost
* Destructive
* Icon button

### Inputs

* Text
* Voice
* Search
* Registration number

### Cards

* Scheme card
* Document card
* Status card
* Trust card

### Chat

* User message
* Sahayak message
* Voice message
* Thinking state

### Status

* Eligible
* Not eligible
* Available
* Missing
* Pending
* Approved
* Error

### Navigation

* Navbar
* Language selector
* Accessibility menu

Use Auto Layout and component variants throughout.

---

# 22. RESPONSIVE MOBILE DESIGN

Create mobile versions for:

* Home
* Conversation
* Results
* Documents
* Application
* Status
* Accessibility panel

On mobile, prioritize:

**Voice → Conversation → Results → Documents**

Use large touch targets.

Keep the microphone easily reachable.

Never hide the text input.

---

# 23. FIGMA PROTOTYPE FLOW

Create a clickable prototype demonstrating the complete golden path:

### Flow

Home

↓

Tap microphone

↓

Conversation

↓

Sahayak asks one question at a time

↓

User provides information

↓

Matched schemes

↓

Select scheme

↓

Required documents

↓

Documents complete

↓

Application package

↓

Download package

↓

Status check

Also create an alternate flow:

**Home → Accessibility settings → High contrast / Voice-first mode**

---

# 24. GOLDEN DEMO SCENARIO

Optimize the prototype around this hackathon demonstration:

### User

A citizen with a disability who is not comfortable with complex digital interfaces.

### Interaction

User taps:

**🎙 “What government schemes can I get?”**

Sahayak responds conversationally.

It asks one question at a time.

The system identifies relevant schemes.

The user opens a scheme.

Sahayak shows:

**Why you're eligible**

↓

**What you already have**

↓

**What you're missing**

↓

**Generate application package**

↓

**Download**

The user never has to navigate a complicated government website during the discovery/preparation process.

---

# 25. VISUAL QUALITY BAR

The final design should look like a combination of:

**Modern AI product**
+
**Premium fintech trust**
+
**Government civic utility**
+
**Accessibility-first UX**

Avoid:

* Generic chatbot aesthetics
* Excessive gradients
* Neon AI visuals
* Huge dashboards
* Tiny typography
* Dense forms
* Excessive cards
* Stock illustrations
* Cartoon robots
* Fake government logos
* Fake government seals

Use authentic-looking but fictional Sahayak branding.

---

# 26. IMPORTANT PRODUCT PRINCIPLES

Design every screen around these principles:

### 1. One question at a time

Never overwhelm the citizen.

### 2. Voice is primary, not mandatory

Every voice interaction must have an equivalent text interaction.

### 3. Accessibility is built in

Not an afterthought.

### 4. Explain AI decisions

Eligibility should show reasons.

### 5. Show sources

Always expose official_url and source_document where applicable.

### 6. Never overclaim

Sahayak prepares and guides. It does not pretend to submit government applications.

### 7. Human-readable language

Avoid bureaucratic terminology wherever possible.

### 8. Trust before automation

For sensitive actions, require explicit user confirmation.

---

# FINAL OUTPUT

Generate a complete polished Figma design system and clickable prototype for **Sahayak**.

Include:

* Desktop screens
* Mobile screens
* Design system
* Components
* Accessibility states
* Voice interaction states
* Loading/error/empty states
* Full prototype navigation
* Golden-path demo flow

Make it feel like a **real startup product ready for a national-level hackathon demo**, not a student project.

The final visual impression should be:

**Calm. Trustworthy. Intelligent. Inclusive. Human. Premium.**
