import re

with open('creator-house/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove GSAP CDN links
html = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/gsap/.*?</script>', '', html, flags=re.DOTALL)

# Replace the GSAP initialization script with IntersectionObserver vanilla JS
old_gsap_script_pattern = re.compile(r'// GSAP Animations.*?}\s*', re.DOTALL)
vanilla_js = """
  // Vanilla Intersection Observer Animations
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReducedMotion) {
   // Add CSS classes for staggered reveals
   const style = document.createElement('style');
   style.textContent = `
    .hero-child { opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
    .hero-child.is-visible { opacity: 1; transform: translateY(0); }
    
    .clip-reveal { clip-path: polygon(0 100%, 100% 100%, 100% 100%, 0% 100%); transition: clip-path 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
    .clip-reveal.is-visible { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
    
    .reveal-up { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
    .reveal-up.is-visible { opacity: 1; transform: translateY(0); }
   `;
   document.head.appendChild(style);

   // Apply initial classes
   const heroChildren = document.querySelectorAll('.hero-content > *');
   heroChildren.forEach(el => el.classList.add('hero-child'));

   // Observer callback
   const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
     if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      obs.unobserve(entry.target);
     }
    });
   }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

   // Observe clip reveals
   document.querySelectorAll('.clip-reveal').forEach(el => observer.observe(el));
   
   // Observe generic reveal up
   document.querySelectorAll('.reveal-up').forEach(el => observer.observe(el));
   
   // Animate hero sequentially
   setTimeout(() => {
    heroChildren.forEach((el, index) => {
     setTimeout(() => {
      el.classList.add('is-visible');
     }, 150 * index);
    });
   }, 200);
  }
"""

html = old_gsap_script_pattern.sub(vanilla_js, html)

with open('creator-house/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
