import re
import os

filepath = 'c:\\Data\\Projects\\Downloads\\sz-ventures\\prototype-hero.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Scoped CSS for the prototype
scoped_css = """
 <style>
   /* PROTOTYPE HERO CSS */
   .proto-hero {
     position: relative;
     min-height: 100vh;
     overflow: hidden;
     display: flex;
     align-items: center;
     background: #080808;
   }
   .proto-layer {
     position: absolute;
     inset: -5%; /* Bleed to allow parallax */
     width: 110%;
     height: 110%;
     background-size: cover;
     background-position: center;
     pointer-events: none;
     will-change: transform;
   }
   .proto-layer--bg {
     background-image: url('/assets/images/cards/manufacturing-card.jpg');
     opacity: 0.2;
     filter: blur(4px) contrast(1.2);
     z-index: 1;
   }
   .proto-layer--mid {
     background-image: url('/assets/images/cards/industrial-ai-card.jpg');
     opacity: 0.3;
     mix-blend-mode: screen;
     z-index: 2;
     /* Mask to create depth separation */
     mask-image: radial-gradient(circle at center, black 0%, transparent 70%);
     -webkit-mask-image: radial-gradient(circle at center, black 0%, transparent 70%);
   }
   .proto-overlay {
     position: absolute;
     inset: 0;
     background: linear-gradient(to bottom, rgba(10,10,12,0.3) 0%, rgba(10,10,12,0.9) 80%, rgba(10,10,12,1) 100%);
     z-index: 3;
     pointer-events: none;
   }
   .proto-content {
     position: relative;
     z-index: 4;
     width: 100%;
   }

   /* Reduced motion & Mobile Fallback */
   @media (prefers-reduced-motion: reduce), (pointer: coarse) {
     .proto-layer { inset: 0; width: 100%; height: 100%; transition: none !important; transform: none !important; }
   }
 </style>
"""

content = content.replace('</head>', scoped_css + '\n</head>')

# 2. Hero Replacement
new_hero = """
 <!-- 01 PROTOTYPE HERO SECTION -->
 <section class="proto-hero" id="top" data-proto-hero>
   <div class="proto-layer proto-layer--bg" data-depth="0.02" data-scroll-speed="0.1"></div>
   <div class="proto-layer proto-layer--mid" data-depth="0.06" data-scroll-speed="0.3"></div>
   <div class="proto-overlay"></div>
   
   <div class="hero__inner container proto-content" data-depth="0.01" data-scroll-speed="-0.2">
     <div class="hero__meta" data-aos="fade">
       <span class="pill">SZ VENTURES</span>
     </div>
     <h1 class="hero__title display" data-aos="fade-up" data-aos-duration="900" style="font-size: clamp(3rem, 6vw, 5rem);">
       <span class="line">BUILDING BUSINESSES</span>
       <span class="line">ACROSS INDUSTRY</span>
       <span class="line"><em class="serif-accent">& THE NEW ECONOMY.</em></span>
     </h1>
     <p class="hero__sub" data-aos="fade-up" data-aos-delay="150" data-aos-duration="900">
       SZ Ventures builds, operates and develops businesses at the intersection of industrial technology, AI, manufacturing, consumer markets and the new economy.
     </p>
     <div class="hero__actions" data-aos="fade-up" data-aos-delay="300" data-aos-duration="900">
       <a href="/contact.html" class="btn btn--accent" data-magnetic data-cursor><span>Start a Conversation</span><span class="btn__arrow" aria-hidden="true">→</span></a>
       <a href="#portfolio" class="btn btn--ghost" data-cursor><span>Explore Our Portfolio</span></a>
     </div>
   </div>
 </section>
"""

# Replace existing hero
content = re.sub(
    r'<!-- 01 HERO SECTION -->.*?</section>', 
    new_hero, 
    content, 
    flags=re.DOTALL
)

# 3. Inject GSAP Script
gsap_script = """
<script>
document.addEventListener('DOMContentLoaded', () => {
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.matchMedia('(pointer: coarse)').matches;
  
  if (isReducedMotion || isMobile) return; // Fallback active

  const hero = document.querySelector('[data-proto-hero]');
  if (!hero) return;

  const layers = gsap.utils.toArray('.proto-layer, .proto-content');
  
  // 1. Pointer Depth Tracking (Mouse Move)
  let cx = window.innerWidth / 2;
  let cy = window.innerHeight / 2;
  
  hero.addEventListener('mousemove', (e) => {
    const px = (e.clientX - cx) / cx; // -1 to 1
    const py = (e.clientY - cy) / cy; // -1 to 1
    
    layers.forEach(layer => {
      const depth = parseFloat(layer.getAttribute('data-depth')) || 0;
      gsap.to(layer, {
        x: px * depth * 100,
        y: py * depth * 100,
        rotationX: py * depth * -10,
        rotationY: px * depth * 10,
        duration: 1,
        ease: 'power2.out'
      });
    });
  });

  hero.addEventListener('mouseleave', () => {
    gsap.to(layers, { x: 0, y: 0, rotationX: 0, rotationY: 0, duration: 1.5, ease: 'power2.out' });
  });

  // 2. Scroll Parallax (GSAP ScrollTrigger)
  if (window.ScrollTrigger) {
    layers.forEach(layer => {
      const speed = parseFloat(layer.getAttribute('data-scroll-speed')) || 0;
      gsap.to(layer, {
        yPercent: speed * 100,
        ease: 'none',
        scrollTrigger: {
          trigger: hero,
          start: 'top top',
          end: 'bottom top',
          scrub: true
        }
      });
    });
  }
});
</script>
"""

content = content.replace('</body>', gsap_script + '\n</body>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Prototype built successfully.")
