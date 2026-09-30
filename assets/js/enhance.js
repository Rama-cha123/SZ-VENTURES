/* =====================================================================
   SZ VENTURES — ENHANCEMENTS
   Global initialization for third-party UI libraries.

   Loaded as a deferred script AFTER libs.bundle.js (which provides the
   UMD globals: AOS, Lenis, tippy, Popper, Odometer). Each initializer is
   guarded so a missing/blocked library never breaks the page.

   Design notes
   ------------
   - No frameworks. Plain UMD globals, so this is framework-agnostic.
     The whole body drops cleanly into a Next.js Client Component:
         'use client';
         import { useEffect } from 'react';
         useEffect(() => { runInit(); }, []);
   - Honors prefers-reduced-motion everywhere (no motion for users who
     opt out). AOS is disabled, Lenis is skipped, Odometer shows final
     values, Tippy stays (tooltips are non-motion UI).
   - Performance: libraries are concatenated into libs.bundle.(js|css)
     (one request each). AOS uses once:true and passive scroll handling.
   - Additive: existing [data-reveal] / [data-count] behaviors in app.js
     are untouched. These libs light up [data-aos], [data-tippy-content]
     and [data-odometer] respectively.
   ===================================================================== */
(function () {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Global namespace — handy for debugging / future hooks. */
  window.SZ = window.SZ || {};

  /* ------------------------------------------------------------------
     AOS — Animate On Scroll
     Usage: add data-aos="fade-up" (etc.) to any element.
     https://github.com/michalsnik/aos
  ------------------------------------------------------------------ */
  function initAOS() {
    if (typeof window.AOS === 'undefined') return;
    window.AOS.init({
      // Disable entirely for reduced-motion users.
      disable: prefersReduced,
      // Animate only the first time an element enters — cheaper + calmer.
      once: true,
      mirror: false,
      offset: 40,
      duration: 500,            // matches --dur in tokens.css
      easing: 'ease-out-cubic',
      delay: 0,
      anchorPlacement: 'top-bottom',
    });
    window.SZ.refreshAOS = function () {
      if (window.AOS) window.AOS.refresh();
    };
    // Failsafe: guarantee all elements are visible even if scroll events are missed
    setTimeout(function () {
      document.querySelectorAll('[data-aos]:not(.aos-animate)').forEach(function (el) {
        el.classList.add('aos-animate');
      });
    }, 1000);
  }

  /* ------------------------------------------------------------------
     Lenis — smooth scroll  (initialized when the lib is added)
     ------------------------------------------------------------------ */
  function initLenis() {
    if (prefersReduced || typeof window.Lenis === 'undefined') return;
    // Buttery smooth scroll. Lenis drives its own rAF loop (autoRaf) and
    // updates the real window scroll position, so the existing nav
    // condense-on-scroll (app.js) and AOS both keep working untouched.
    const lenis = new window.Lenis({
      autoRaf: true,     // Lenis owns the animation frame loop
      autoToggle: true,  // pause on pages shorter than the viewport (perf)
      anchors: true,     // smooth in-page anchor jumps (e.g. #main skip link)
      duration: 1.1,
    });
    window.SZ.lenis = lenis;
    lenis.on('scroll', function () {
      if (window.AOS) window.AOS.refresh();
    });
    // If async content changes layout, let AOS recompute offsets.
    window.addEventListener('load', function () {
      if (window.SZ && window.SZ.refreshAOS) window.SZ.refreshAOS();
    });
  }

  /* ------------------------------------------------------------------
     Tippy.js — tooltips  (initialized when the lib is added)
     ------------------------------------------------------------------ */
  function initTippy() {
    if (typeof window.tippy === 'undefined') return;
    // Auto-enhance every element carrying data-tippy-content (nav items,
    // buttons, icons). Tooltips are informational, not motion, so they
    // stay enabled under reduced-motion — only the transition is dropped.
    window.tippy('[data-tippy-content]', {
      theme: 'sz',
      animation: prefersReduced ? false : 'shift-away',
      delay: [120, 60],
      duration: [200, 150],
      touch: ['hold', 120],
      maxWidth: 260,
      zIndex: 9999,
    });
  }

  /* ------------------------------------------------------------------
     Odometer — animated counters  (initialized when the lib is added)
     ------------------------------------------------------------------ */
  function initOdometer() {
    const els = document.querySelectorAll('[data-odometer]');
    if (!els.length) return;

    const finalText = (el) =>
      (el.getAttribute('data-count') || '0') + (el.getAttribute('data-suffix') || '');

    // Fallback A: Odometer script blocked -> show final values, no roll.
    if (typeof window.Odometer === 'undefined') {
      els.forEach((el) => { el.textContent = finalText(el); });
      return;
    }
    // Fallback B: reduced motion -> final values, no rolling digits.
    if (prefersReduced) {
      els.forEach((el) => { el.textContent = finalText(el); });
      return;
    }

    els.forEach((el) => {
      const target = parseFloat(el.getAttribute('data-count')) || 0;
      const suffix = el.getAttribute('data-suffix') || '';

      // Split the numeric part (Odometer rolls this) from the non-numeric
      // tail (%, ★, M+, mo…) so the suffix is never part of the animation.
      const num = document.createElement('span');
      const suf = document.createElement('span');
      suf.className = 'm-suffix';
      suf.textContent = suffix;
      el.textContent = '';
      el.appendChild(num);
      el.appendChild(suf);

      const format = Number.isInteger(target) ? '(,ddd)' : '(,ddd).d';
      const od = new window.Odometer({
        el: num, value: 0, format: format, theme: 'default',
      });

      const run = () => od.update(target);
      if (!('IntersectionObserver' in window)) { run(); return; }
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) { run(); io.unobserve(entry.target); }
        });
      }, { threshold: 0.4 });
      io.observe(el);
    });
  }

  /* ---------- Boot ---------- */
  initAOS();
  initLenis();
  initTippy();
  initOdometer();

  // Recalculate positions once async assets (fonts/images) settle, so
  // AOS triggers fire at the right scroll offsets.
  window.addEventListener('load', function () {
    if (window.SZ && window.SZ.refreshAOS) window.SZ.refreshAOS();
  });
})();
