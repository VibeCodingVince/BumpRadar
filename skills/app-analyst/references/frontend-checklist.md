# Frontend Audit Checklist

Use this checklist when performing the frontend audit phase. Not every item
applies to every app — use judgment about what's relevant.

## Typography

- [ ] Font choices are intentional (not system defaults unless deliberate)
- [ ] Font loading strategy exists (preload, font-display: swap, etc.)
- [ ] Clear hierarchy: display, heading, body, caption sizes are distinct
- [ ] Consistent font weights (not random bold/light scattered around)
- [ ] Line height appropriate for body text (1.4-1.6 for readability)
- [ ] Letter spacing used purposefully (not default everywhere)
- [ ] No more than 2-3 font families in use
- [ ] Font sizes responsive (rem/em or clamp, not fixed px everywhere)

## Color & Theme

- [ ] Colors defined as CSS variables or theme tokens
- [ ] Palette is cohesive (colors feel related, not random)
- [ ] Sufficient contrast for text readability (WCAG AA: 4.5:1 normal, 3:1 large)
- [ ] Semantic colors for status (success, warning, error, info)
- [ ] Hover/active/focus states use palette colors (not random darken/lighten)
- [ ] Background colors create clear visual zones
- [ ] No color-only information (colorblind users need shape/text cues too)

## Spacing & Layout

- [ ] Consistent spacing system (multiples of 4px or 8px)
- [ ] Container max-width appropriate for content type
- [ ] Responsive breakpoints handle phone, tablet, desktop
- [ ] No horizontal overflow on mobile
- [ ] Flex/grid used appropriately (not absolute positioning hacks)
- [ ] Consistent padding within similar components
- [ ] Adequate whitespace — not cramped, not wastefully empty

## Components

- [ ] Buttons: consistent sizing, padding, border-radius across the app
- [ ] Forms: labels, placeholders, validation states, error messages
- [ ] Cards/containers: consistent shadow, border, radius treatment
- [ ] Modals: backdrop, close mechanism, focus trap, escape key
- [ ] Loading states: skeleton screens, spinners, or progress indicators
- [ ] Empty states: helpful messages when no data exists
- [ ] Error states: clear messaging with recovery actions

## Animations & Interactions

- [ ] Transitions are smooth (0.15s-0.3s for micro, 0.3s-0.5s for larger)
- [ ] No animation on reduced-motion preference (prefers-reduced-motion)
- [ ] Hover effects provide clear feedback
- [ ] Click/tap targets minimum 44x44px on mobile
- [ ] No layout shift during loading or state changes
- [ ] Animations serve a purpose (not decorative noise)

## Accessibility

- [ ] Semantic HTML (nav, main, article, section, button — not div for everything)
- [ ] ARIA labels on interactive elements without visible text
- [ ] Alt text on images (decorative images get alt="")
- [ ] Keyboard navigation works (tab order logical, focus visible)
- [ ] Form inputs have associated labels
- [ ] Skip-to-content link for keyboard users
- [ ] Language attribute on html element

## Performance

- [ ] Images optimized (compressed, appropriate format, lazy loaded)
- [ ] No massive unoptimized assets (check for multi-MB images)
- [ ] CSS/JS not render-blocking unnecessarily
- [ ] External resources loaded efficiently (async, defer, preconnect)
- [ ] No unused large libraries loaded
- [ ] Client-side image compression if user uploads photos

## Code Quality

- [ ] CSS organized (variables, logical grouping, not random ordering)
- [ ] JavaScript handles errors (try/catch on API calls, user feedback)
- [ ] No console.log statements left in production code
- [ ] Event listeners cleaned up where needed
- [ ] State management is clear (not scattered global variables)
- [ ] API calls have timeout handling
- [ ] Sensitive data not stored in localStorage without consideration
