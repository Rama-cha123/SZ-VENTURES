---
name: framer-motion
description: Design, implement, optimize, and review Framer Motion animations in React or Next.js interfaces. Activate for motion components, variants, orchestration, AnimatePresence, layout transitions, scroll interactions, gesture feedback, reduced-motion accessibility, and Framer Motion performance work. Do not activate for static HTML/CSS websites unless the user explicitly requests a React migration.
---

# Framer Motion Integration Guide

This skill governs the integration and management of `framer-motion` inside React or Next.js interfaces.

## 1. Confirm Compatibility
Before using Framer Motion, inspect the project and confirm:
* React or Next.js is actually used.
* `framer-motion` or `motion` is installed.
* The installed package and version.
* Whether components are server or client components.
* Whether an existing motion system already exists.

**If the target is a static HTML/CSS website:**
* Do not install React.
* Do not migrate the site.
* Do not add Framer Motion.
* Use scoped CSS transitions or the existing animation system.
* Explain why Framer Motion is inappropriate for that specific target.

## 2. Preserve Existing Architecture
Do not:
* Replace working animation systems unnecessarily.
* Initialize duplicate smooth-scroll systems.
* Conflict with GSAP, AOS, Lenis or Swup.
* Convert server components into client components without need.
* Add `"use client"` to large component trees.
* Animate global layout properties without performance review.
* Rewrite unrelated components.
* Introduce animation that blocks content visibility.

## 3. Motion Design Standards
Animations should be:
* Purposeful, Smooth, Restrained, Responsive, Accessible, GPU-friendly, and Consistent with the current design system.

**Preferred defaults:**
* Micro-interactions: approximately 150–250ms
* Component transitions: approximately 300–500ms
* Editorial reveals: approximately 500–800ms
* Movement: generally 8–24px
* Hover scaling: generally no more than `1.02–1.04`
* Avoid bounce or elastic effects unless the brand explicitly requires them.

**Animate primarily:**
* `transform`, `opacity`, and carefully controlled `clip-path`.

**Avoid frequent animation of:**
* `width`, `height`, `top`, `left`, large filters, expensive shadows, and layout-triggering properties.

## 4. Reusable Variants
Prefer reusable typed variants rather than repeating animation objects.
Support patterns for:
* Fade and rise, Staggered lists, Page transitions, Modal presence, Drawer transitions, Card hover feedback, Shared layout transitions, Scroll-triggered reveals, and Loading/success/error states.

Keep variants close to their domain or in a clearly named motion utility module. Do not build one oversized universal variants file.

## 5. AnimatePresence
When using `AnimatePresence`:
* Provide stable keys.
* Ensure exit animations can run.
* Avoid unnecessary remounting.
* Use appropriate `mode`.
* Verify focus behavior for dialogs and drawers.
* Ensure removed content does not leave interaction-blocking overlays.
* Test rapid open/close interactions.

## 6. Layout Animations
Use `layout` and `layoutId` carefully. Verify:
* No unexpected content jumps.
* No distorted images or text.
* No collision with responsive layout.
* Stable identifiers.
* Correct behavior during rapid state changes.
* Acceptable performance on lower-end devices.

## 7. Scroll Animation
For scroll-triggered animation:
* Prefer `whileInView` for straightforward reveals.
* Use `viewport={{ once: true }}` when repetition is unnecessary.
* Use `useScroll` and `useTransform` only when continuous progress is required.
* Avoid excessive parallax.
* Avoid registering many independent scroll observers.
* Keep content visible if animation initialization fails.

*Note: Do not add Lenis solely because a component uses Framer Motion. If Lenis already exists, preserve the existing instance and configuration.*

## 8. Accessibility
Always respect reduced-motion preferences. Use:
* `useReducedMotion`
* Reduced-motion CSS fallbacks where necessary.
* Immediate visibility when motion is disabled.
* Proper keyboard focus and Semantic HTML.
* Stable focus during modal and route transitions.

Animation must not be the only method of communicating state. Avoid:
* Flashing effects, large involuntary movement, motion that prevents reading, hover-only functionality, and permanently hidden content when JavaScript fails.

## 9. Performance
Before adding animation, consider:
* Bundle impact, client-component boundaries, re-render frequency, layout thrashing, image size, mobile performance, concurrent animations, and cleanup of subscriptions/controls.

Use `LazyMotion` and `m` components when bundle reduction provides a meaningful benefit. Do not introduce abstraction that is more complex than the animation itself.

## 10. React and Next.js Rules
For Next.js:
* Keep server components as server components whenever possible.
* Create the smallest practical client animation wrapper.
* Do not place `"use client"` at page or layout level without justification.
* Preserve metadata and server-rendered content.
* Avoid hydration mismatches.
* Ensure the initial server-rendered state remains readable.

## 11. Testing
Verify:
* Initial render, entrance animation, exit animation.
* Rapid repeated interactions.
* Mobile behavior, keyboard interaction, reduced-motion mode.
* Component unmounting, route changes.
* No console warnings, hydration errors, or memory leaks.
* Acceptable performance on lower-powered hardware.

## 12. Scope Protection
Do not use this skill to modify the static SZ Ventures public website unless the user explicitly asks to migrate a specific part to React.

For the current static public website:
* Continue using its existing CSS/AOS/GSAP/Lenis architecture.
* Do not install Framer Motion.
* Do not modify the preloader.
* Do not introduce React merely for animations.

The skill may be used for the React/Next.js SZ Ventures AI OS dashboard and portal.

## Reference Patterns
Review the [reference patterns](./references/patterns.md) for implementation examples.
