import os
import re

path = r'c:\Data\Projects\Downloads\sz-ventures\creator-house\index.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# I will parse the entire file and generate a modernized Gen-Z focused template, while preserving the exact 3 images and the pricing.
# We will use Tailwind CSS just like in SnapOps, and general-sans font.

new_html = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
 <title>Creator House ?" Studio & Production Ecosystem | SZ Ventures</title>
 <meta name="description" content="A premium production ecosystem built for creators, models, influencers, UGC creators and digital-first talent. Studio space, equipment and production support in Bengaluru.">
 <meta name="theme-color" content="#070706">
 <link rel="canonical" href="https://szventures.com/creator-house/">

 <meta property="og:type" content="website">
 <meta property="og:image" content="https://szventures.com/assets/images/creator-house/creator-house-hero.webp">
 <meta name="twitter:image" content="https://szventures.com/assets/images/creator-house/creator-house-hero.webp">
 
 <!-- Fonts: Editorial typography, Gen-Z creator vibes -->
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
 <link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700,800&f[]=cabinet-grotesk@700,800,900&display=swap" rel="stylesheet">

 <!-- Tailwind CSS -->
 <script src="https://cdn.tailwindcss.com"></script>
 <script>
  tailwind.config = {
   theme: {
    extend: {
     fontFamily: {
      display: ['Cabinet Grotesk', 'sans-serif'],
      sans: ['General Sans', 'sans-serif'],
      body: ['Inter', 'sans-serif'],
     },
     colors: {
      brand: {
       black: '#070706',
       dark: '#11100e',
       gray: '#2a2825',
       gold: '#D2A957',
       lightGold: '#E6C98A',
       neon: '#C5FF4A'
      }
     }
    }
   }
  }
 </script>
 
 <style>
  body { background-color: theme('colors.brand.black'); color: white; }
  .text-gradient { background: linear-gradient(135deg, #fff 0%, #a0a0a0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .text-gold-gradient { background: linear-gradient(135deg, #E6C98A 0%, #D2A957 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .glass-card { background: rgba(17, 16, 14, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(210, 169, 87, 0.15); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }
  .glass-card:hover { border-color: rgba(210, 169, 87, 0.4); }
  
  .reveal-up { opacity: 0; transform: translateY(40px); }
  @media (prefers-reduced-motion: reduce) {
   .reveal-up { opacity: 1; transform: none; transition: none; }
   * { animation: none !important; transition: none !important; }
  }
  
  .hero-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60vw; height: 60vw; background: radial-gradient(circle, rgba(210,169,87,0.1) 0%, transparent 70%); z-index: -1; filter: blur(60px); pointer-events: none; }
 </style>
</head>
<body class="antialiased overflow-x-hidden relative selection:bg-brand-gold selection:text-black">
 
 <!-- Navbar -->
 <nav class="fixed top-0 left-0 right-0 z-50 bg-brand-black/80 backdrop-blur-md border-b border-white/5 h-20 flex items-center">
  <div class="container mx-auto px-6 max-w-7xl flex justify-between items-center">
   <a href="/" class="flex items-center gap-2 group">
    <img src="../assets/img/logo.png" alt="SZ Ventures" class="h-8 w-auto opacity-90 group-hover:opacity-100 transition-opacity">
   </a>
   <a href="#join" class="px-5 py-2.5 rounded-full bg-brand-gold text-brand-black font-sans font-bold text-sm tracking-wide hover:bg-brand-lightGold transition-colors">
    BECOME A MEMBER
   </a>
  </div>
 </nav>

 <main class="pt-32 pb-24">
  <!-- 1. HERO -->
  <section class="relative container mx-auto px-6 max-w-7xl mb-32">
   <div class="hero-glow"></div>
   <div class="grid lg:grid-cols-2 gap-12 items-center">
    <div class="reveal-up relative z-10">
     <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-brand-gold/30 bg-brand-gold/10 text-brand-gold text-xs font-sans font-bold uppercase tracking-widest mb-6">
      <span class="w-1.5 h-1.5 rounded-full bg-brand-gold animate-pulse"></span>
      Bengaluru
     </div>
     <h1 class="font-display font-extrabold text-5xl md:text-7xl leading-[1.05] tracking-tight mb-6">
      Content <br><span class="text-text-gradient">Creation,</span><br><span class="text-gold-gradient">Elevated.</span>
     </h1>
     <p class="font-body text-lg md:text-xl text-white/60 max-w-lg mb-8 leading-relaxed">
      A premium production ecosystem built for Gen-Z creators, models, and digital-first talent. High-end studios, pro gear, and instant drop-in access.
     </p>
     <a href="#join" class="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-white text-black font-sans font-bold text-base hover:scale-105 transition-transform">
      Claim Early Access
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
     </a>
    </div>
    
    <div class="relative reveal-up delay-200">
     <figure class="relative rounded-[2rem] overflow-hidden border border-white/10 shadow-2xl">
      <img src="/assets/images/creator-house/creator-house-hero.webp" alt="Premium Creator House Studio Setup" class="w-full h-auto object-cover scale-[1.02] hover:scale-100 transition-transform duration-700" loading="eager" fetchpriority="high" decoding="async">
     </figure>
     
     <!-- Floating Badge -->
     <div class="absolute -bottom-6 -left-6 glass-card p-4 rounded-2xl flex items-center gap-4 animate-bounce" style="animation-duration: 4s;">
      <div class="w-12 h-12 rounded-full bg-brand-gold flex items-center justify-center text-black font-bold text-xl">4K</div>
      <div>
       <div class="font-sans font-bold text-sm">Cinematic Setup</div>
       <div class="font-body text-xs text-white/50">Ready to shoot</div>
      </div>
     </div>
    </div>
   </div>
  </section>

  <!-- 2. THE PROBLEM / SOLUTION -->
  <section class="container mx-auto px-6 max-w-7xl mb-32 relative">
   <div class="text-center max-w-3xl mx-auto mb-16 reveal-up">
    <h2 class="font-display font-extrabold text-4xl md:text-5xl tracking-tight mb-6">Stop shooting in <span class="text-white/40">messy bedrooms.</span></h2>
    <p class="font-body text-lg text-white/60">Algorithm-friendly content requires high production value. You shouldn't need to rent gear daily or compromise on lighting.</p>
   </div>
   
   <figure class="rounded-[2rem] overflow-hidden border border-brand-gold/20 mb-16 reveal-up shadow-2xl">
    <img src="/assets/images/creator-house/creator-house-production.webp" alt="Professional creator content production" class="w-full h-auto object-cover" loading="lazy" decoding="async">
   </figure>

   <div class="grid md:grid-cols-3 gap-6 reveal-up">
    <div class="glass-card p-8 rounded-3xl group">
     <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-brand-gold mb-6 group-hover:scale-110 transition-transform">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
     </div>
     <h3 class="font-sans font-bold text-xl mb-3">Plug & Play</h3>
     <p class="font-body text-sm text-white/50">Show up with your phone or SD card. We handle the 4K cameras, acoustic treatment, and professional lighting grids.</p>
    </div>
    
    <div class="glass-card p-8 rounded-3xl group">
     <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-brand-gold mb-6 group-hover:scale-110 transition-transform">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
     </div>
     <h3 class="font-sans font-bold text-xl mb-3">Vibe-Optimized</h3>
     <p class="font-body text-sm text-white/50">Multiple aesthetic zones engineered for high audience retention. Perfect for GRWMs, interviews, and deep dives.</p>
    </div>

    <div class="glass-card p-8 rounded-3xl group">
     <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-brand-gold mb-6 group-hover:scale-110 transition-transform">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
     </div>
     <h3 class="font-sans font-bold text-xl mb-3">Creator Network</h3>
     <p class="font-body text-sm text-white/50">Collaborate with other growing creators, get peer feedback, and cross-pollinate your audience in a physical space.</p>
    </div>
   </div>
  </section>

  <!-- 3. PODCAST ZONE -->
  <section class="container mx-auto px-6 max-w-7xl mb-32">
   <div class="grid lg:grid-cols-2 gap-16 items-center">
    <div class="order-2 lg:order-1 reveal-up">
     <figure class="rounded-[2rem] overflow-hidden border border-brand-gold/20 shadow-2xl">
      <img src="/assets/images/creator-house/creator-house-podcast.webp" alt="Creator House podcast recording setup" class="w-full h-auto object-cover" loading="lazy" decoding="async">
     </figure>
    </div>
    <div class="order-1 lg:order-2 reveal-up">
     <h2 class="font-display font-extrabold text-4xl md:text-5xl tracking-tight mb-6">Drop the mic. <br><span class="text-gold-gradient">We’ll record it.</span></h2>
     <p class="font-body text-lg text-white/60 mb-8">Our broadcast-ready podcast suite features Shure SM7B mics, multi-cam switching, and instant mixing. Sit down, talk your truth, and walk out with ready-to-post assets.</p>
     
     <ul class="space-y-4 font-sans text-sm font-semibold text-white/80">
      <li class="flex items-center gap-3"><svg class="w-5 h-5 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> 4K Multi-cam recording</li>
      <li class="flex items-center gap-3"><svg class="w-5 h-5 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Broadcast-level audio</li>
      <li class="flex items-center gap-3"><svg class="w-5 h-5 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Teleprompter & Live Switching</li>
     </ul>
    </div>
   </div>
  </section>

  <!-- 4. MEMBERSHIP CTA -->
  <section id="join" class="container mx-auto px-6 max-w-5xl mb-16 reveal-up">
   <div class="glass-card rounded-[2.5rem] p-8 md:p-16 text-center border-brand-gold/30 relative overflow-hidden">
    <div class="absolute top-0 right-0 w-64 h-64 bg-brand-gold/10 blur-[80px] rounded-full mix-blend-screen pointer-events-none"></div>
    <div class="absolute bottom-0 left-0 w-64 h-64 bg-brand-gold/10 blur-[80px] rounded-full mix-blend-screen pointer-events-none"></div>
    
    <span class="inline-block px-4 py-1.5 rounded-full bg-brand-gold/15 text-brand-gold font-sans font-bold text-xs tracking-widest uppercase mb-8">Limited Genesis Drop</span>
    <h2 class="font-display font-extrabold text-4xl md:text-5xl mb-6">Create Without Limits</h2>
    <p class="font-body text-white/60 max-w-xl mx-auto mb-10">Stop paying hourly studio rates. Get predictable flat-fee access to premium setups and grow your channel faster.</p>

    <div class="bg-black/50 border border-white/10 rounded-3xl p-8 max-w-2xl mx-auto mb-10">
     <div class="flex flex-col md:flex-row justify-center items-center gap-8 mb-6">
      
      <div class="text-center relative">
       <span class="absolute -top-3 -right-6 px-2 py-0.5 bg-red-500 text-white text-[10px] font-bold uppercase rounded-sm transform rotate-6">Closing Soon</span>
       <div class="font-sans font-semibold text-white/40 uppercase tracking-widest text-xs mb-2">Early-Bird</div>
       <div class="font-display font-bold text-5xl text-brand-gold mb-1">,3,499<span class="text-lg text-white/40 font-sans font-normal">/mo</span></div>
       <div class="font-body text-[10px] text-white/30 uppercase tracking-widest">+ applicable taxes</div>
      </div>
      
      <div class="h-16 w-px bg-white/10 hidden md:block"></div>
      
      <div class="text-center">
       <div class="font-sans font-semibold text-white/40 uppercase tracking-widest text-xs mb-2">Regular Price</div>
       <div class="font-display font-bold text-3xl text-white/40 line-through decoration-brand-gold/50 decoration-2 mb-1">,4,999<span class="text-sm font-sans font-normal">/mo</span></div>
       <div class="font-body text-[10px] text-white/30 uppercase tracking-widest">Applies after first 300</div>
      </div>
      
     </div>
     
     <div class="grid grid-cols-2 gap-4 text-left border-t border-white/10 pt-6">
      <div>
       <div class="font-display font-bold text-2xl text-brand-gold">12</div>
       <div class="font-sans text-xs text-white/60 uppercase tracking-wider font-semibold">Pro Photos/mo</div>
      </div>
      <div>
       <div class="font-display font-bold text-2xl text-brand-gold">3</div>
       <div class="font-sans text-xs text-white/60 uppercase tracking-wider font-semibold">Short-Form Reels/mo</div>
      </div>
     </div>
    </div>

    <!-- The original trigger form logic kept intact, just styled nicely -->
    <a href="/contact.html?intent=creator-house" class="inline-block w-full md:w-auto px-10 py-5 rounded-full bg-brand-gold text-black font-sans font-bold text-lg hover:bg-white hover:scale-105 transition-all shadow-[0_0_40px_rgba(210,169,87,0.3)]">
     CLAIM EARLY-BIRD MEMBERSHIP
    </a>
   </div>
  </section>
 </main>

 <!-- Footer Navigation -->
 <footer class="border-t border-white/5 bg-black pt-16 pb-8">
  <div class="container mx-auto px-6 max-w-7xl">
   <nav class="footer-nav" aria-label="Footer">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-16">
     <div class="footer-nav-col">
      <h4 class="font-sans font-bold text-white mb-6 tracking-wide">Industries</h4>
      <ul class="space-y-3 font-body text-sm text-white/50">
       <li><a href="/industrial-technology.html" class="hover:text-brand-gold transition-colors">Industrial Technology</a></li>
       <li><a href="/industrial-technology.html#ai-robotics-data" class="hover:text-brand-gold transition-colors">AI &amp; Robotics Data</a></li>
       <li><a href="/industrial-technology.html#industrial-ai" class="hover:text-brand-gold transition-colors">Industrial AI</a></li>
       <li><a href="/industrial-technology.html#manufacturing" class="hover:text-brand-gold transition-colors">Manufacturing</a></li>
       <li><a href="/new-economy.html" class="hover:text-brand-gold transition-colors">New Economy</a></li>
      </ul>
     </div>
     <div class="footer-nav-col">
      <h4 class="font-sans font-bold text-white mb-6 tracking-wide">Ventures</h4>
      <ul class="space-y-3 font-body text-sm text-white/50">
       <li><a href="/ventures/bowl-and-sip/index.html" class="hover:text-brand-gold transition-colors">Bowl &amp; Sip Co.</a></li>
       <li><a href="/creator-house/" class="hover:text-brand-gold transition-colors">Creator House</a></li>
       <li><a href="/snapops/" class="hover:text-brand-gold transition-colors">SnapOps</a></li>
      </ul>
     </div>
     <div class="footer-nav-col">
      <h4 class="font-sans font-bold text-white mb-6 tracking-wide">Company</h4>
      <ul class="space-y-3 font-body text-sm text-white/50">
       <li><a href="/about/" class="hover:text-brand-gold transition-colors">About</a></li>
       <li><a href="/ventures/" class="hover:text-brand-gold transition-colors">Ventures</a></li>
       <li><a href="/capabilities.html" class="hover:text-brand-gold transition-colors">Capabilities</a></li>
       <li><a href="/insights.html" class="hover:text-brand-gold transition-colors">Insights</a></li>
       <li><a href="/contact.html" class="hover:text-brand-gold transition-colors">Contact</a></li>
      </ul>
     </div>
    </div>
   </nav>
   <div class="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-body text-white/40">
    <div>&copy; 2026 SZ Ventures. All rights reserved.</div>
    <div class="flex items-center gap-4">
     <a href="#" class="hover:text-white">Privacy</a>
     <a href="#" class="hover:text-white">Terms</a>
    </div>
   </div>
  </div>
 </footer>

 <!-- GSAP & ScrollTrigger -->
 <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
 <script>
  gsap.registerPlugin(ScrollTrigger);
  
  // Respect reduced motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReducedMotion) {
   gsap.utils.toArray('.reveal-up').forEach(element => {
    gsap.to(element, {
     scrollTrigger: {
      trigger: element,
      start: "top 85%",
      toggleActions: "play none none reverse"
     },
     opacity: 1,
     y: 0,
     duration: 0.8,
     ease: "power3.out"
    });
   });
  }
 </script>
</body>
</html>
"""

new_html = new_html.replace(",3,499", "&#8377;3,499")
new_html = new_html.replace(",4,999", "&#8377;4,999")

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated creator-house")
