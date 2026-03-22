# Report Template

Use this exact structure for the audit report. Every section is required.

---

```markdown
# App Analysis Report: [App Name]
Generated: [YYYY-MM-DD]

## Executive Summary

[2-3 sentences maximum. State: overall health assessment (healthy/needs work/
critical issues), the single biggest risk, and the single highest-impact quick
win. This section should let someone who reads nothing else know what to do
first.]

---

## Critical Issues

[Issues that break functionality, expose security vulnerabilities, or cause
data loss. If there are none, write "No critical issues found." Do not omit
the section.]

### [CRT-001] Issue Title
**Location:** `path/to/file.ext:line_number`
**Problem:** Concise description of what is wrong.
**Impact:** What happens if this is not fixed. Be specific — "security risk"
is too vague; "any user can call admin endpoints without authentication,
allowing database manipulation" is actionable.
**Fix:** Exact steps to resolve. Code snippets welcome. Should be specific
enough that a developer can implement without further research.

---

## High Priority

[Issues that significantly degrade user experience, performance, or code
quality. Things that make the app feel broken or unprofessional.]

### [HIGH-001] Issue Title
**Location:** `path/to/file.ext:line_number`
**Problem:** ...
**Impact:** ...
**Fix:** ...

---

## Medium Priority

[Issues affecting maintainability, minor UX problems, or things that will
become bigger problems as the app scales.]

### [MED-001] Issue Title
**Location:** `path/to/file.ext:line_number`
**Problem:** ...
**Impact:** ...
**Fix:** ...

---

## Low Priority

[Polish items, nice-to-haves, and future considerations. Things that don't
hurt now but would improve the app.]

### [LOW-001] Issue Title
**Location:** `path/to/file.ext:line_number`
**Problem:** ...
**Impact:** ...
**Fix:** ...

---

## Quick Wins

[Top 5 changes with the highest impact-to-effort ratio. These should be
things that take under 30 minutes each but make a noticeable difference.]

1. **[Title]** — [One sentence: what to do and what it fixes.] `file:line`
2. **[Title]** — ...
3. **[Title]** — ...
4. **[Title]** — ...
5. **[Title]** — ...

---

## What's Working Well

[Genuine positives. Good architectural decisions, well-implemented features,
solid design choices. This section builds trust in the rest of the report —
if you only criticize, the developer won't trust your judgment on what
matters. Be specific: "good use of CSS variables for theming" not just
"the code is clean".]

- ...
- ...
- ...
```

---

## Guidelines for writing findings

1. **Be specific over comprehensive.** 10 precise findings beat 30 vague ones.
2. **Include file paths and line numbers.** Every finding must point to code.
3. **Write actionable fixes.** "Improve error handling" is not a fix.
   "Add try/except around the OpenAI call at line 142 and return a 503
   with message 'AI service temporarily unavailable'" is a fix.
4. **Calibrate severity honestly.** Not everything is critical. Marking
   cosmetic issues as critical destroys trust in the real critical findings.
5. **Acknowledge good work.** The "What's Working Well" section is required
   and should contain genuine observations, not filler.
