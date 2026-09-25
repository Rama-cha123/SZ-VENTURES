/* =====================================================================
   SZ VENTURES — AMBIENT PARTICLES & WAVE MESH
   Golden floating particles + flowing wireframe wave at hero bottom
   ===================================================================== */

(function () {
  'use strict';

  // ─── FLOATING PARTICLES ──────────────────────────────────────────
  function initParticles() {
    const canvas = document.getElementById('sz-particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height;
    const particles = [];
    const PARTICLE_COUNT = 80;

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    class Particle {
      constructor() { this.reset(true); }
      reset(initial) {
        this.x = Math.random() * width;
        this.y = initial ? Math.random() * height : height + 20;
        this.size = Math.random() * 2.5 + 0.5;
        this.speedX = (Math.random() - 0.5) * 0.3;
        this.speedY = -(Math.random() * 0.4 + 0.1);
        this.opacity = 0;
        this.maxOpacity = Math.random() * 0.6 + 0.2;
        this.fadeIn = true;
        this.life = 0;
        this.maxLife = Math.random() * 600 + 300;
        this.glow = Math.random() > 0.7;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.life++;

        if (this.fadeIn) {
          this.opacity += 0.008;
          if (this.opacity >= this.maxOpacity) this.fadeIn = false;
        }
        if (this.life > this.maxLife - 60) {
          this.opacity -= 0.01;
        }
        if (this.opacity <= 0 || this.y < -20 || this.x < -20 || this.x > width + 20) {
          this.reset(false);
        }
      }
      draw(ctx) {
        if (this.opacity <= 0) return;
        ctx.save();
        ctx.globalAlpha = this.opacity;

        if (this.glow) {
          ctx.shadowBlur = 12;
          ctx.shadowColor = 'rgba(220, 180, 110, 0.5)';
        }

        ctx.fillStyle = `rgba(220, 180, 110, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push(new Particle());
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);
      for (const p of particles) {
        p.update();
        p.draw(ctx);
      }
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ─── FLOWING WAVE MESH ──────────────────────────────────────────
  function initWaveMesh() {
    const canvas = document.getElementById('sz-wave-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height;
    let time = 0;

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      width = canvas.width = rect.width;
      height = canvas.height = canvas.offsetHeight || rect.height * 0.45;
    }
    resize();
    window.addEventListener('resize', resize);

    function drawWave(yOffset, amplitude, frequency, speed, alpha, lineWidth) {
      const cols = 60;
      const rows = 18;
      const colW = width / cols;
      const rowH = height / rows;

      ctx.strokeStyle = `rgba(220, 180, 110, ${alpha})`;
      ctx.lineWidth = lineWidth;

      // Horizontal lines
      for (let r = 0; r < rows; r++) {
        ctx.beginPath();
        for (let c = 0; c <= cols; c++) {
          const x = c * colW;
          const baseY = yOffset + r * rowH;
          const wave1 = Math.sin((c / cols) * frequency + time * speed) * amplitude;
          const wave2 = Math.sin((c / cols) * frequency * 0.7 + time * speed * 0.6 + r * 0.3) * amplitude * 0.5;
          const perspY = baseY + wave1 + wave2;
          const perspScale = 0.3 + (r / rows) * 0.7;
          const finalY = height * 0.2 + (perspY - height * 0.2) * perspScale;

          if (c === 0) ctx.moveTo(x, finalY);
          else ctx.lineTo(x, finalY);
        }
        ctx.stroke();
      }

      // Vertical lines
      for (let c = 0; c <= cols; c++) {
        ctx.beginPath();
        for (let r = 0; r < rows; r++) {
          const x = c * colW;
          const baseY = yOffset + r * rowH;
          const wave1 = Math.sin((c / cols) * frequency + time * speed) * amplitude;
          const wave2 = Math.sin((c / cols) * frequency * 0.7 + time * speed * 0.6 + r * 0.3) * amplitude * 0.5;
          const perspY = baseY + wave1 + wave2;
          const perspScale = 0.3 + (r / rows) * 0.7;
          const finalY = height * 0.2 + (perspY - height * 0.2) * perspScale;

          if (r === 0) ctx.moveTo(x, finalY);
          else ctx.lineTo(x, finalY);
        }
        ctx.stroke();
      }

      // Bright nodes at intersections (sparse)
      for (let r = 0; r < rows; r += 3) {
        for (let c = 0; c <= cols; c += 4) {
          const x = c * colW;
          const baseY = yOffset + r * rowH;
          const wave1 = Math.sin((c / cols) * frequency + time * speed) * amplitude;
          const wave2 = Math.sin((c / cols) * frequency * 0.7 + time * speed * 0.6 + r * 0.3) * amplitude * 0.5;
          const perspY = baseY + wave1 + wave2;
          const perspScale = 0.3 + (r / rows) * 0.7;
          const finalY = height * 0.2 + (perspY - height * 0.2) * perspScale;

          ctx.fillStyle = `rgba(245, 215, 150, ${alpha * 1.5})`;
          ctx.beginPath();
          ctx.arc(x, finalY, 1.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);
      drawWave(height * 0.1, 25, Math.PI * 3, 0.015, 0.25, 0.6);
      drawWave(height * 0.15, 20, Math.PI * 2.5, 0.012, 0.15, 0.4);
      time += 1;
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ─── CSS BOKEH DOTS ──────────────────────────────────────────────
  function initBokeh() {
    const container = document.querySelector('.sz-bokeh');
    if (!container) return;
    const DOT_COUNT = 15;

    for (let i = 0; i < DOT_COUNT; i++) {
      const dot = document.createElement('div');
      dot.className = 'sz-bokeh__dot';
      const size = Math.random() * 6 + 3;
      dot.style.width = size + 'px';
      dot.style.height = size + 'px';
      dot.style.left = Math.random() * 100 + '%';
      dot.style.top = (Math.random() * 60 + 40) + '%';
      dot.style.animationDuration = (Math.random() * 15 + 10) + 's';
      dot.style.animationDelay = (Math.random() * 10) + 's';
      container.appendChild(dot);
    }
  }

  // ─── INIT ────────────────────────────────────────────────────────
  function init() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    initParticles();
    initWaveMesh();
    initBokeh();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
