path = r'c:\Data\Projects\Downloads\sz-ventures\creator-house\index.html'
import os

html_content = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
 <title>Creator House | Midnight Creator Club | SZ Ventures</title>
 <meta name="description" content="A private production club for ambitious Gen-Z creators. Premium studios, pro gear, and instant access in Bengaluru.">
 <meta name="theme-color" content="#070708">
 <link rel="canonical" href="https://szventures.com/creator-house/">

 <!-- Typography -->
 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
 <link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700,800&display=swap" rel="stylesheet">

 <!-- Tailwind CSS -->
 <script src="https://cdn.tailwindcss.com"></script>
 <script>
  tailwind.config = {
   theme: {
    extend: {
     fontFamily: {
      display: ['General Sans', 'sans-serif'],
      body: ['Inter', 'sans-serif'],
     },
     colors: {
      ch: {
       bg: '#070708',
       'bg-deep': '#020203',
       surface: '#111114',
       'surface-2': '#18181d',
       'surface-hover': '#202028',
       text: '#f7f4ed',
       muted: '#aaa6b2',
       soft: '#777380',
       gold: '#e0ad4f',
       'gold-light': '#f4cf82',
       'gold-dark': '#9b6b24',
       violet: '#8b5cf6',
       coral: '#ff6b6b',
      }
     }
    }
   }
  }
 </script>
 
 <style>
  :root {
   --ch-bg: #070708;
   --ch-bg-deep: #020203;
   --ch-surface: #111114;
   --ch-surface-2: #18181d;
   --ch-surface-hover: #202028;
   --ch-text: #f7f4ed;
   --ch-muted: #aaa6b2;
   --ch-soft: #777380;
   --ch-gold: #e0ad4f;
   --ch-gold-light: #f4cf82;
   --ch-gold-dark: #9b6b24;
   --ch-violet: #8b5cf6;
   --ch-coral: #ff6b6b;
   --ch-line: rgba(224, 173, 79, 0.22);
   --ch-line-soft: rgba(255, 255, 255, 0.08);
   --ch-glow: rgba(224, 173, 79, 0.14);
  }

  body {
   background-color: var(--ch-bg);
   color: var(--ch-text);
   -webkit-font-smoothing: antialiased;
   overflow-x: hidden;
  }
  
  .text-gradient-gold-violet {
   background: linear-gradient(135deg, var(--ch-gold) 0%, var(--ch-violet) 100%);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
  }
  
  .bg-gradient-radial {
   background: radial-gradient(circle at center, rgba(224,173,79,0.15) 0%, transparent 60%);
  }

  /* Glow Card Effect */
  .glow-card {
   position: relative;
   overflow: hidden;
  }
  .glow-card::before {
   content: "";
   position: absolute;
   top: var(--mouse-y, 50%);
   left: var(--mouse-x, 50%);
   width: 400px;
   height: 400px;
   background: radial-gradient(circle, var(--ch-glow) 0%, transparent 70%);
   transform: translate(-50%, -50%);
   opacity: 0;
   transition: opacity 0.4s ease;
   pointer-events: none;
   z-index: 0;
  }
  .glow-card:hover::before {
   opacity: 1;
  }
  .glow-card > * {
   position: relative;
   z-index: 1;
  }

  /* Marquee */
  .marquee-container {
   display: flex;
   overflow: hidden;
   white-space: nowrap;
   border-top: 1px solid var(--ch-line);
   border-bottom: 1px solid var(--ch-line);
   background-color: var(--ch-bg-deep);
   padding: 1rem 0;
  }
  .marquee-content {
   display: flex;
   animation: marquee 25s linear infinite;
  }
  @keyframes marquee {
   0% { transform: translateX(0); }
   100% { transform: translateX(-50%); }
  }

  /* Clip-path reveal */
  .clip-reveal {
   clip-path: polygon(0 100%, 100% 100%, 100% 100%, 0% 100%);
  }

  @media (prefers-reduced-motion: reduce) {
   .marquee-content { animation-play-state: paused !important; }
   .clip-reveal { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%) !important; }
   .reveal-up { opacity: 1 !important; transform: none !important; transition: none !important; }
   * { animation: none !important; transition: none !important; }
  }

  /* Global Cursor Glow */
  .cursor-glow {
   position: fixed;
   top: 0; left: 0;
   width: 600px; height: 600px;
   background: radial-gradient(circle, rgba(224,173,79,0.06) 0%, transparent 60%);
   border-radius: 50%;
   pointer-events: none;
   transform: translate(-50%, -50%);
   z-index: 9999;
   mix-blend-mode: screen;
   transition: opacity 0.3s;
   opacity: 0;
  }
  @media (min-width: 1024px) {
   body:hover .cursor-glow { opacity: 1; }
  }
 </style>
</head>
<body id="page-top">

 <div class="cursor-glow" id="cursor-glow"></div>

 <!-- 1. HEADER -->
 <header class="fixed top-0 left-0 w-full z-50 bg-ch-bg/80 backdrop-blur-lg border-b border-ch-gold transition-all duration-300">
  <div class="container mx-auto px-6 max-w-[1400px] h-20 flex items-center justify-between">
   <a href="/" class="flex items-center gap-3">
    <img src="../assets/img/logo.png" alt="SZ Ventures" class="h-8 w-auto">
   </a>
   
   <nav class="hidden md:flex items-center gap-8 font-body text-sm font-medium text-ch-muted">
    <a href="/ventures/" class="hover:text-ch-text transition-colors">Ventures</a>
    <a href="/creator-house/" class="text-ch-text transition-colors">Creator House</a>
    <a href="#membership" class="hover:text-ch-text transition-colors">Membership</a>
    <a href="#how-it-works" class="hover:text-ch-text transition-colors">How It Works</a>
    <a href="/contact.html" class="hover:text-ch-text transition-colors">Contact</a>
   </nav>

   <div class="flex items-center gap-4">
    <a href="/contact.html?intent=creator-house" class="hidden md:inline-flex px-6 py-2.5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm hover:bg-ch-gold-light transition-colors">
     CLAIM EARLY-BIRD ACCESS
    </a>
    <!-- Mobile Menu Button -->
    <button class="md:hidden text-ch-text focus:outline-none p-2" aria-label="Toggle menu" id="mobile-menu-btn">
     <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
    </button>
   </div>
  </div>
  
  <!-- Mobile Menu Dropdown -->
  <div id="mobile-menu" class="hidden md:hidden bg-ch-bg-deep border-b border-ch-line-soft px-6 py-6 space-y-4 shadow-2xl">
   <a href="/ventures/" class="block font-body text-base text-ch-muted hover:text-ch-text">Ventures</a>
   <a href="/creator-house/" class="block font-body text-base text-ch-text">Creator House</a>
   <a href="#membership" class="block font-body text-base text-ch-muted hover:text-ch-text">Membership</a>
   <a href="#how-it-works" class="block font-body text-base text-ch-muted hover:text-ch-text">How It Works</a>
   <a href="/contact.html" class="block font-body text-base text-ch-muted hover:text-ch-text">Contact</a>
   <div class="pt-4 mt-2 border-t border-ch-line-soft">
    <a href="/contact.html?intent=creator-house" class="block text-center px-6 py-3 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm">
     CLAIM EARLY-BIRD ACCESS
    </a>
   </div>
  </div>
 </header>

 <main class="pt-20">
  
  <!-- 2. HERO -->
  <section id="hero-section" class="relative min-h-[90vh] flex items-center bg-ch-bg overflow-hidden pt-12 pb-24">
   <div class="absolute inset-0 bg-gradient-radial opacity-40 pointer-events-none"></div>
   
   <div class="container mx-auto px-6 max-w-[1400px] grid lg:grid-cols-2 gap-16 lg:gap-12 items-center relative z-10">
    <!-- Left Copy -->
    <div class="hero-content">
     <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-ch-gold/30 bg-ch-gold/10 text-ch-gold text-xs font-display font-bold uppercase tracking-widest mb-8">
      <span class="w-1.5 h-1.5 rounded-full bg-ch-gold animate-pulse"></span>
      Bengaluru · Founding Drop
     </div>
     
     <h1 class="font-display font-extrabold text-5xl md:text-6xl lg:text-7xl leading-[1.1] tracking-tight mb-8">
      Your Content.<br>
      Your Space.<br>
      <span class="text-gradient-gold-violet">Your Production Engine.</span>
     </h1>
     
     <p class="font-body text-lg md:text-xl text-ch-muted max-w-lg mb-10 leading-relaxed">
      A private production club for ambitious Gen-Z creators. Engineered for reels, high-fidelity podcasts, UGC, and brand content that drives unstoppable creator growth.
     </p>
     
     <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 mb-6">
      <a href="/contact.html?intent=creator-house" class="px-8 py-4 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-base hover:bg-ch-gold-light transition-all shadow-[0_0_20px_rgba(224,173,79,0.3)] hover:scale-105">
       CLAIM EARLY-BIRD ACCESS
      </a>
      <a href="#how-it-works" class="px-8 py-4 rounded-full bg-ch-surface border border-ch-line-soft text-ch-text font-display font-bold text-base hover:bg-ch-surface-hover transition-colors">
       EXPLORE THE SPACE
      </a>
     </div>
     <div class="font-body text-xs text-ch-soft font-medium flex items-center gap-2">
      <svg class="w-4 h-4 text-ch-gold" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path></svg>
      ₹3,499 + taxes/month for the first 300 subscriptions
     </div>
    </div>
    
    <!-- Right Image -->
    <div class="relative hero-image-container">
     <div class="relative rounded-[2rem] overflow-hidden border border-ch-gold shadow-[0_0_50px_rgba(224,173,79,0.15)] clip-reveal" id="hero-img-wrap">
      <div class="absolute inset-0 bg-ch-bg-deep/20 mix-blend-multiply z-10 pointer-events-none"></div>
      <img src="/assets/images/creator-house/creator-house-hero.webp" alt="Midnight Creator Club Studio" class="w-full h-auto object-cover aspect-[4/5] sm:aspect-square lg:aspect-[4/5]" loading="eager">
     </div>
     
     <!-- Badges -->
     <div class="absolute top-6 left-6 z-20 px-4 py-2 bg-ch-surface/90 backdrop-blur border border-ch-line-soft rounded-full text-xs font-display font-bold text-ch-text shadow-lg">4K READY</div>
     <div class="absolute bottom-6 right-6 z-20 px-4 py-2 bg-ch-surface/90 backdrop-blur border border-ch-line-soft rounded-full text-xs font-display font-bold text-ch-text shadow-lg">PODCAST</div>
     <div class="absolute top-1/2 -right-4 -translate-y-1/2 z-20 px-4 py-2 bg-ch-violet text-white border border-ch-line-soft rounded-full text-xs font-display font-bold shadow-[0_0_15px_rgba(139,92,246,0.5)] rotate-3">REELS</div>
     <div class="absolute bottom-24 -left-4 z-20 px-4 py-2 bg-ch-coral text-white border border-ch-line-soft rounded-full text-xs font-display font-bold shadow-[0_0_15px_rgba(255,107,107,0.4)] -rotate-3">UGC</div>
    </div>
   </div>
  </section>

  <!-- 3. MARQUEE -->
  <section class="marquee-container text-ch-gold font-display font-bold text-2xl md:text-3xl tracking-widest uppercase">
   <div class="marquee-content items-center">
    <span class="mx-6">SHOOT</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">EDIT</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">PODCAST</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">REELS</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">UGC</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">COLLABORATE</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">PUBLISH</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">REPEAT</span><span class="text-ch-line mx-4">•</span>
    
    <span class="mx-6">SHOOT</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">EDIT</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">PODCAST</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">REELS</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">UGC</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">COLLABORATE</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6">PUBLISH</span><span class="text-ch-line mx-4">•</span>
    <span class="mx-6 text-ch-text">REPEAT</span><span class="text-ch-line mx-4">•</span>
   </div>
  </section>

  <!-- 4. BENEFITS (CARDS) -->
  <section id="benefits-section" class="py-24 bg-ch-bg-deep relative">
   <div class="container mx-auto px-6 max-w-[1400px]">
    <div class="grid md:grid-cols-3 gap-8">
     
     <!-- Card 1 -->
     <div class="glow-card bg-ch-surface border border-ch-line-soft hover:border-ch-gold/40 rounded-2xl p-10 transition-all duration-300 hover:-translate-y-2 group" id="benefit-card-1">
      <div class="w-12 h-12 rounded-full bg-ch-gold/10 flex items-center justify-center text-ch-gold mb-8 border border-ch-gold/20 group-hover:scale-110 transition-transform">
       <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
      </div>
      <h3 class="font-display font-bold text-2xl text-ch-text mb-4">PLUG &amp; PLAY</h3>
      <p class="font-body text-ch-muted leading-relaxed">Cameras, acoustic treatment and professional lighting ready when you arrive. Just show up and hit record.</p>
     </div>

     <!-- Card 2 -->
     <div class="glow-card bg-ch-surface border border-ch-line-soft hover:border-ch-violet/40 rounded-2xl p-10 transition-all duration-300 hover:-translate-y-2 group" id="benefit-card-2">
      <div class="w-12 h-12 rounded-full bg-ch-violet/10 flex items-center justify-center text-ch-violet mb-8 border border-ch-violet/20 group-hover:scale-110 transition-transform">
       <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
      </div>
      <h3 class="font-display font-bold text-2xl text-ch-text mb-4">VIBE-OPTIMIZED</h3>
      <p class="font-body text-ch-muted leading-relaxed">Creator-ready visual zones specifically designed and lit for reels, interviews, GRWMs and long-form podcasts.</p>
     </div>

     <!-- Card 3 -->
     <div class="glow-card bg-ch-surface border border-ch-line-soft hover:border-ch-coral/40 rounded-2xl p-10 transition-all duration-300 hover:-translate-y-2 group" id="benefit-card-3">
      <div class="w-12 h-12 rounded-full bg-ch-coral/10 flex items-center justify-center text-ch-coral mb-8 border border-ch-coral/20 group-hover:scale-110 transition-transform">
       <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
      </div>
      <h3 class="font-display font-bold text-2xl text-ch-text mb-4">CREATOR NETWORK</h3>
      <p class="font-body text-ch-muted leading-relaxed">Collaborate, exchange feedback and grow alongside other ambitious creators within an exclusive physical club.</p>
     </div>

    </div>
   </div>
  </section>

  <!-- 5. PRODUCTION SECTION -->
  <section id="how-it-works" class="py-32 bg-ch-bg">
   <div class="container mx-auto px-6 max-w-[1400px]">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
     <!-- Left Image (Alternate alignment from hero which had copy on left) -->
     <div class="order-2 lg:order-1 relative production-image">
      <div class="relative rounded-3xl overflow-hidden border border-ch-line-soft shadow-2xl clip-reveal" id="prod-img-wrap">
       <div class="absolute inset-0 bg-ch-bg-deep/10 mix-blend-multiply z-10"></div>
       <img src="/assets/images/creator-house/creator-house-production.webp" alt="Creator Studio Production Setup" class="w-full h-auto object-cover aspect-video lg:aspect-[4/3]" loading="lazy">
      </div>
     </div>
     
     <!-- Right Copy -->
     <div class="order-1 lg:order-2 production-content">
      <div class="font-display font-bold text-ch-gold text-xl mb-4 border-b border-ch-line-soft inline-block pb-1">01</div>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-ch-text mb-8 tracking-tight">Shoot more.<br>Coordinate less.</h2>
      
      <div class="space-y-6 font-body text-lg text-ch-muted">
       <div class="flex items-start gap-4">
        <div class="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-ch-gold/20 flex items-center justify-center text-ch-gold">
         <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
        </div>
        <p><strong class="text-ch-text font-semibold">Studio-ready production.</strong> Forget renting lenses or wrestling with ring lights. Our bays are permanently pre-lit and pre-rigged.</p>
       </div>
       
       <div class="flex items-start gap-4">
        <div class="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-ch-gold/20 flex items-center justify-center text-ch-gold">
         <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
        </div>
        <p><strong class="text-ch-text font-semibold">Short-form and long-form workflows.</strong> Optimize your time with dedicated setups tailored for quick TikTok/Reel batching or deep YouTube essays.</p>
       </div>
       
       <div class="flex items-start gap-4">
        <div class="mt-1 flex-shrink-0 w-6 h-6 rounded-full bg-ch-gold/20 flex items-center justify-center text-ch-gold">
         <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
        </div>
        <p><strong class="text-ch-text font-semibold">Equipment and production support.</strong> Access on-site technical assistance, memory card offloading, and continuous power.</p>
       </div>
      </div>
     </div>
    </div>
   </div>
  </section>

  <!-- 6. PODCAST SECTION -->
  <section class="py-32 bg-ch-bg-deep relative overflow-hidden">
   <!-- Subtle accent glow -->
   <div class="absolute top-1/2 left-1/4 -translate-y-1/2 w-96 h-96 bg-ch-violet/5 blur-[120px] pointer-events-none"></div>
   
   <div class="container mx-auto px-6 max-w-[1400px]">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
     
     <!-- Left Copy -->
     <div class="podcast-content relative z-10">
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-ch-violet/30 bg-ch-violet/10 text-ch-violet text-xs font-display font-bold uppercase tracking-widest mb-8">
       PODCAST · INTERVIEW · DEEP DIVE
      </div>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-ch-text mb-6 tracking-tight">Your voice deserves a better room.</h2>
      <p class="font-body text-lg text-ch-muted leading-relaxed">
       Elevate your audio and visual fidelity. Our acoustically treated podcast suite is engineered for multi-cam interviews, founder stories, and branded conversations. Sit down, hit record, and walk away with perfectly isolated tracks and broadcast-ready angles.
      </p>
     </div>
     
     <!-- Right Image -->
     <div class="podcast-image relative z-10">
      <div class="relative rounded-3xl overflow-hidden border border-ch-violet/20 shadow-[0_0_40px_rgba(139,92,246,0.1)] clip-reveal" id="pod-img-wrap">
       <div class="absolute inset-0 bg-ch-bg/30 mix-blend-multiply z-10"></div>
       <img src="/assets/images/creator-house/creator-house-podcast.webp" alt="Creator Podcast Studio Setup" class="w-full h-auto object-cover aspect-video lg:aspect-[4/3]" loading="lazy">
      </div>
     </div>
     
    </div>
   </div>
  </section>

  <!-- 7. PRICING SECTION -->
  <section id="membership" class="py-32 bg-ch-bg relative">
   <div class="container mx-auto px-6 max-w-5xl">
    
    <div class="glow-card bg-ch-surface border border-ch-violet/30 shadow-[0_0_80px_rgba(139,92,246,0.15)] rounded-[2.5rem] p-8 md:p-16 text-center reveal-up">
     <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-ch-gold/50 bg-ch-gold/20 text-ch-gold text-xs font-display font-bold uppercase tracking-widest mb-8 shadow-[0_0_15px_rgba(224,173,79,0.3)]">
      FOUNDING CREATOR DROP
     </div>
     
     <h2 class="font-display font-extrabold text-4xl md:text-5xl text-ch-text mb-10 tracking-tight">Lock in your space.</h2>
     
     <div class="bg-ch-bg-deep border border-ch-line-soft rounded-3xl p-8 md:p-10 mb-10 max-w-3xl mx-auto relative overflow-hidden">
      <!-- Decor -->
      <div class="absolute -top-10 -right-10 w-32 h-32 bg-ch-violet/20 blur-[40px]"></div>
      <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-ch-gold/20 blur-[40px]"></div>
      
      <div class="flex flex-col items-center justify-center relative z-10">
       <div class="text-ch-soft line-through text-xl md:text-2xl font-display font-medium mb-2 decoration-ch-coral/60 decoration-2">₹4,999 + taxes/month</div>
       <div class="text-ch-gold text-5xl md:text-7xl font-display font-extrabold tracking-tight mb-2">
        ₹3,499 <span class="text-lg md:text-xl text-ch-muted font-body font-normal tracking-normal">+ taxes/month</span>
       </div>
       <div class="mt-4 px-4 py-1.5 rounded bg-ch-coral/10 text-ch-coral text-sm font-display font-bold uppercase tracking-widest border border-ch-coral/20">
        LIMITED TO FIRST 300
       </div>
       <p class="text-ch-soft text-sm mt-3 font-body">Available to the first 300 subscriptions only</p>
      </div>
      
      <div class="mt-10 pt-8 border-t border-ch-line-soft grid sm:grid-cols-2 gap-y-4 gap-x-8 text-left relative z-10">
       <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-ch-violet flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span class="font-body text-sm text-ch-text">12 professionally edited photos/month</span>
       </div>
       <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-ch-violet flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span class="font-body text-sm text-ch-text">3 short-form videos or reels/month</span>
       </div>
       <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-ch-violet flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span class="font-body text-sm text-ch-text">1 long-form video (10–12 mins)</span>
       </div>
       <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-ch-violet flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span class="font-body text-sm text-ch-text">2 Creator House access days/month</span>
       </div>
      </div>
     </div>

     <a href="/contact.html?intent=creator-house" class="inline-flex items-center justify-center w-full md:w-auto px-12 py-5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-lg hover:bg-ch-gold-light hover:scale-105 transition-all shadow-[0_0_30px_rgba(224,173,79,0.25)]">
      CLAIM EARLY-BIRD MEMBERSHIP
     </a>
    </div>

   </div>
  </section>
 </main>

 <!-- Footer -->
 <footer class="border-t border-ch-line-soft bg-ch-bg-deep pt-16 pb-8">
  <div class="container mx-auto px-6 max-w-[1400px]">
   <nav class="footer-nav flex flex-wrap lg:grid lg:grid-cols-3 gap-12 mb-16" aria-label="Footer">
    <div class="footer-nav-col w-full md:w-auto">
     <h4 class="font-display font-bold text-ch-text mb-6 text-lg">Industries</h4>
     <ul class="space-y-4 font-body text-sm text-ch-muted">
      <li><a href="/industrial-technology.html" class="hover:text-ch-gold transition-colors">Industrial Technology</a></li>
      <li><a href="/industrial-technology.html#ai-robotics-data" class="hover:text-ch-gold transition-colors">AI &amp; Robotics Data</a></li>
      <li><a href="/industrial-technology.html#industrial-ai" class="hover:text-ch-gold transition-colors">Industrial AI</a></li>
      <li><a href="/industrial-technology.html#manufacturing" class="hover:text-ch-gold transition-colors">Manufacturing</a></li>
      <li><a href="/new-economy.html" class="hover:text-ch-gold transition-colors">New Economy</a></li>
     </ul>
    </div>
    <div class="footer-nav-col w-full md:w-auto">
     <h4 class="font-display font-bold text-ch-text mb-6 text-lg">Ventures</h4>
     <ul class="space-y-4 font-body text-sm text-ch-muted">
      <li><a href="/ventures/bowl-and-sip/index.html" class="hover:text-ch-gold transition-colors">Bowl &amp; Sip Co.</a></li>
      <li><a href="/creator-house/" class="hover:text-ch-gold transition-colors">Creator House</a></li>
      <li><a href="/snapops/" class="hover:text-ch-gold transition-colors">SnapOps</a></li>
     </ul>
    </div>
    <div class="footer-nav-col w-full md:w-auto">
     <h4 class="font-display font-bold text-ch-text mb-6 text-lg">Company</h4>
     <ul class="space-y-4 font-body text-sm text-ch-muted">
      <li><a href="/about/" class="hover:text-ch-gold transition-colors">About</a></li>
      <li><a href="/ventures/" class="hover:text-ch-gold transition-colors">Ventures</a></li>
      <li><a href="/capabilities.html" class="hover:text-ch-gold transition-colors">Capabilities</a></li>
      <li><a href="/insights.html" class="hover:text-ch-gold transition-colors">Insights</a></li>
      <li><a href="/contact.html" class="hover:text-ch-gold transition-colors">Contact</a></li>
     </ul>
    </div>
   </nav>
   <div class="border-t border-ch-line-soft pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-body text-ch-soft">
    <div>&copy; 2026 SZ Ventures. All rights reserved.</div>
    <div class="flex items-center gap-6">
     <a href="/privacy.html" class="hover:text-ch-text transition-colors">Privacy Policy</a>
     <a href="/terms.html" class="hover:text-ch-text transition-colors">Terms of Service</a>
    </div>
   </div>
  </div>
 </footer>

 <!-- Scripts -->
 <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
 <script>
  // Mobile Menu Toggle
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  btn.addEventListener('click', () => {
   menu.classList.toggle('hidden');
  });

  // Cursor Glow
  const glow = document.getElementById('cursor-glow');
  document.addEventListener('mousemove', (e) => {
   glow.style.left = e.clientX + 'px';
   glow.style.top = e.clientY + 'px';
  });

  // Glow Cards
  document.querySelectorAll('.glow-card').forEach(card => {
   card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
    card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
   });
  });

  // GSAP Animations (Respecting prefers-reduced-motion)
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReducedMotion) {
   gsap.registerPlugin(ScrollTrigger);

   // Staggered Hero Reveal
   gsap.from(".hero-content > *", {
    y: 30,
    opacity: 0,
    duration: 0.8,
    stagger: 0.15,
    ease: "power3.out",
    delay: 0.2
   });

   // Image Clip Reveals
   gsap.fromTo("#hero-img-wrap", 
    { clipPath: "polygon(0 100%, 100% 100%, 100% 100%, 0% 100%)" },
    { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", duration: 1.2, ease: "power4.inOut", delay: 0.4 }
   );
   
   gsap.utils.toArray('.clip-reveal').forEach(img => {
    if(img.id !== 'hero-img-wrap') {
     gsap.fromTo(img, 
      { clipPath: "polygon(0 100%, 100% 100%, 100% 100%, 0% 100%)" },
      { 
       scrollTrigger: { trigger: img, start: "top 85%" },
       clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", 
       duration: 1.2, 
       ease: "power4.inOut" 
      }
     );
    }
   });

   // Generic Fade Ups
   gsap.utils.toArray('.reveal-up').forEach(element => {
    gsap.fromTo(element, 
     { opacity: 0, y: 40 },
     {
      scrollTrigger: {
       trigger: element,
       start: "top 85%",
      },
      opacity: 1,
      y: 0,
      duration: 0.8,
      ease: "power3.out"
     }
    );
   });
  }
 </script>
</body>
</html>
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated creator-house with Midnight Creator Club theme.")

