---
name: app-analyst
description: >
  Perform a comprehensive audit of a full-stack web application covering frontend
  design quality, UX, accessibility, backend API design, security, architecture,
  and operational health. Use this skill whenever the user asks to review, audit,
  analyze, or assess their app. Also trigger when the user says their app "looks
  cheap", has quality issues, wants a health check, asks what's wrong, wants to
  know if it's production ready, asks why changes aren't working, or wants a
  prioritized list of things to fix. This includes any variation of "analyze my
  app", "what's wrong with my app", "review the codebase", "is this ready to
  ship", or "why does this look bad".
---

# App Analyst

A skill for performing deep, structured audits of full-stack web applications.
The goal is to surface real problems with specific file paths, line numbers, and
actionable fixes — not generic advice. Every finding must be something the
developer can act on immediately.

## When the user triggers this skill

They're usually frustrated. The app "looks cheap" or "changes aren't sticking"
or they just have a nagging feeling something is off. Your job is to be the
experienced senior engineer who looks at the whole picture — code, config, git
state, design, architecture — and gives them a clear, prioritized path forward.

## Audit Workflow

Run these phases in order. Each phase builds context for the next.

### Phase 1: Operational Health Check

This phase catches the "why aren't my changes showing up?" class of problems.
Do this first because it's the most common source of frustration and the
fastest to diagnose.

1. **Git state**: Run `git status` and `git diff --stat`. Look for:
   - Uncommitted changes (the #1 reason "changes don't work")
   - Untracked files that should be committed (or gitignored)
   - Divergence from remote (local behind origin)

2. **Environment config**: Check for `.env` files. Verify:
   - Required keys are present (don't expose values, just check existence)
   - No secrets committed to git (check `.gitignore`)
   - Config consistency between frontend and backend (API URLs, ports)

3. **Server viability**: Check if the app can actually start:
   - Import errors in Python/Node entry points
   - Missing dependencies
   - Port conflicts or hardcoded localhost references

Report any issues found before continuing — the user may want to fix these
first since they can make later findings misleading.

### Phase 2: Frontend Audit

Read the frontend checklist at `references/frontend-checklist.md` for detailed
criteria. Read all main frontend files (HTML, CSS, JS entry points).

Evaluate across these dimensions:
- **Design quality**: Typography, color palette, spacing, visual hierarchy
- **UX**: User flows, error states, loading states, empty states, responsiveness
- **Accessibility**: Semantic HTML, ARIA, contrast, keyboard navigation
- **Performance**: Image sizes, render-blocking resources, unnecessary deps
- **Code quality**: Separation of concerns, maintainability, duplication

The "looks cheap" feeling usually comes from one or more of:
- Inconsistent spacing (different padding/margins with no system)
- Too many fonts or font weights fighting each other
- Colors that don't form a cohesive palette
- Missing loading/error/empty states (makes the app feel unfinished)
- Generic stock design (no personality or brand identity)
- Poor mobile experience
- Janky animations or transitions

Be specific. "The spacing is inconsistent" is useless. "The card padding is
16px in the results section but 24px in the header, and the gap between cards
alternates between 8px and 12px" is actionable.

### Phase 3: Backend Audit

Read the backend checklist at `references/backend-checklist.md` for detailed
criteria. Read the main entry point, all API endpoint files, and key models.

Evaluate across these dimensions:
- **API design**: REST conventions, response consistency, status codes, validation
- **Security**: CORS policy, authentication, authorization, input sanitization
- **Architecture**: Separation of concerns, error propagation, dependency patterns
- **Performance**: Query efficiency, caching, connection management, rate limiting
- **Data integrity**: Model constraints, migration state, relationship correctness

### Phase 4: Cross-Cutting Analysis

Look at the seams between frontend and backend:
- API URL configuration alignment
- Request/response shape mismatches
- Error handling chain (do backend errors surface usefully in the frontend?)
- Authentication flow consistency
- CORS and header configuration

## Report Format

ALWAYS structure the output using this exact template. Read
`references/report-template.md` for the full template with field descriptions.

```
# App Analysis Report: [App Name]
Generated: [date]

## Executive Summary
[2-3 sentences: overall health, biggest risk, most impactful quick win]

## Critical Issues (breaks functionality or security risk)
## High Priority (significantly degrades quality or UX)
## Medium Priority (maintainability or minor UX issues)
## Low Priority (polish and nice-to-haves)

## Quick Wins
[Top 5 highest impact-to-effort ratio changes]

## What's Working Well
[Genuinely good things — don't skip this section]
```

Each issue follows this format:
```
### [ISSUE-ID] Issue Title
**Location:** `file/path.ext:line_number`
**Problem:** What is wrong
**Impact:** What happens if not fixed
**Fix:** Specific, actionable steps to resolve
```

## Important Guidelines

- Every finding MUST include a file path. If you can't point to a specific file,
  the finding isn't concrete enough.
- Include line numbers where possible. "Somewhere in main.py" is not helpful.
- The "Fix" field should be copy-pasteable or at minimum describe the exact
  change needed. Not "improve the error handling" but "wrap the OpenAI call in
  a try/except and return a 503 with a user-friendly message when the API is down."
- Don't pad the report with obvious or generic advice. "Use HTTPS in production"
  is filler unless they're actively serving over HTTP.
- The "What's Working Well" section is mandatory. If the design is actually
  good, say so. False negatives erode trust just like false positives.
- Prioritize ruthlessly. A report with 5 critical + 5 high + quick wins is
  more useful than 50 medium items.
