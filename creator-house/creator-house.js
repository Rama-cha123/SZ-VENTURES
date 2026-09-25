/**
 * CREATOR HOUSE — GEN-Z CINEMATIC SCROLLING & INTERACTION ENGINE
 * Continuous narrative scrolling: IDEA → SPACE → SHOOT → EDIT → COLLABORATE → PUBLISH → JOIN
 * Conforms to Sections 26–48 of the Functional Specification:
 * - 100% real assigned actions on every button/card/link
 * - Centralized route/action configuration consumption
 * - 7-field structured membership form with real success state & localStorage persistence
 * - Deep-link hash navigation for spaces and creator use-cases
 * - Smooth anchor scrolling with 76px sticky navbar offset
 * - Mobile menu drawer with scroll-lock and clean navigation
 */

document.addEventListener('DOMContentLoaded', () => {
  const data = window.CREATOR_HOUSE_DATA;
  const config = window.CREATOR_HOUSE_CONFIG || {};

  if (!data) {
    console.error('[Creator House] Data not loaded.');
    return;
  }

  // 1. DYNAMIC RENDERING OF ALL SECTIONS
  renderMarquee(data.marqueeItems);
  renderFeatures(data.valueProps, config);
  renderJourney(data.journeySteps);
  renderSpaces(data.spaces, config);
  renderCreators(data.useCases, config);

  // 2. INITIALIZE INTERACTION CONTROLLERS
  initNavigation(config);
  initAnchorRouting(config);
  initCustomCursor();
  initMagneticButtons();
  initUnifiedScrollEngine();
  initModalHandlers(data, config);
  handleInitialUrlHash(data, config);
});

/* =========================================================================
   RENDER FUNCTIONS
   ========================================================================= */

function renderMarquee(items) {
  const track = document.getElementById('marqueeTrack');
  if (!track) return;

  const fullList = [...items, ...items, ...items, ...items];
  const bulletColors = ['text-lime', 'text-violet', 'text-blue', 'text-coral'];

  track.innerHTML = fullList.map((item, index) => {
    const colorClass = bulletColors[index % bulletColors.length];
    return `
      <div class="ch-marquee__item">
        <span>${item}</span>
        <span class="${colorClass}">•</span>
      </div>
    `;
  }).join('');
}

function renderFeatures(features, config) {
  const container = document.getElementById('featuresGrid');
  if (!container) return;

  const icons = {
    camera: `📷`,
    layout: `🎙`,
    users: `👥`,
    cpu: `⚡`
  };

  // Specific destinations per feature card as per Section 30
  const featureRoutes = [
    { target: '#spaces', label: 'EXPLORE SPACES' },       // Plug & Play -> /spaces#production
    { target: '#spaces', label: 'EXPLORE STAGES' },       // Vibe-Optimized Spaces -> /spaces
    { target: '#creators', label: 'VIEW COMMUNITY' },     // Creator Network -> /community (#creators)
    { target: '#spaces', label: 'PRODUCTION SUITES' }     // Production Support -> /services (#spaces)
  ];

  container.innerHTML = features.slice(0, 4).map((item, index) => {
    const route = featureRoutes[index] || { target: '#spaces', label: 'LEARN MORE' };
    return `
      <div class="ch-why-card is-hidden" data-card-index="${index}">
        <div>
          <div class="ch-why-card__icon">${icons[item.icon] || '⚡'}</div>
          <h3 class="ch-why-card__title">${item.title}</h3>
          <p class="ch-why-card__desc">${item.description}</p>
        </div>
        <div class="ch-why-card__footer">
          <a href="${route.target}" class="ch-why-card__link ch-smooth-scroll" aria-label="${item.title}: ${route.label}">
            <span>${route.label}</span>
            <span class="ch-arrow-icon">➔</span>
          </a>
          <span class="ch-why-card__num">${item.id}</span>
        </div>
      </div>
    `;
  }).join('');
}

function renderJourney(steps) {
  const container = document.getElementById('journeyPipeline');
  if (!container) return;

  const circleClasses = [
    'ch-journey-circle--01',
    'ch-journey-circle--02',
    'ch-journey-circle--03',
    'ch-journey-circle--04',
    'ch-journey-circle--05'
  ];

  container.innerHTML = steps.slice(0, 5).map((step, idx) => `
    <div class="ch-journey-node" data-node-step="${idx + 1}">
      <div class="ch-journey-node__top">
        <div class="ch-journey-circle ${circleClasses[idx % circleClasses.length]}">${step.step}</div>
        <div class="ch-journey-arrow">
          <div class="ch-journey-arrow__fill"></div>
        </div>
      </div>
      <h3 class="ch-journey-node__name">${step.title}</h3>
      <p class="ch-journey-node__desc">${step.subtitle || step.description}</p>
    </div>
  `).join('');
}

function renderSpaces(spaces, config) {
  const container = document.getElementById('spacesGrid');
  if (!container) return;

  const tagsBySpace = {
    'studio-a': ['VIDEO', 'FILM', 'CAMPAIGNS'],
    'the-pod': ['PODCAST', 'INTERVIEWS'],
    'reels-lab': ['REELS', 'UGC', 'SHORTS'],
    'edit-suite': ['EDITING', 'COLOR', 'AUDIO'],
    'creator-lounge': ['COMMUNITY', 'LOUNGE', 'EVENTS']
  };

  container.innerHTML = spaces.map(space => {
    const tags = tagsBySpace[space.id] || ['PRODUCTION', '4K'];
    return `
      <div class="ch-space-card-4 open-space-card" data-space-id="${space.id}" id="card-${space.id}" tabindex="0" role="button" aria-label="Explore ${space.name}">
        <div class="ch-space-card-4__media">
          <img src="${space.image}" alt="${space.name}" class="ch-space-card-4__img" loading="lazy">
        </div>
        <div class="ch-space-card-4__body">
          <h3 class="ch-space-card-4__name">${space.name}</h3>
          <div class="ch-space-card-4__sub">${space.tagline}</div>
          <div class="ch-space-card-4__tags">
            ${tags.map(t => `<span class="ch-space-tag">${t}</span>`).join('')}
          </div>
          <a href="#${space.id}" class="ch-space-card-4__cta open-space-modal" data-space-id="${space.id}" aria-label="Explore ${space.name} Specifications">
            <span>EXPLORE SPACE</span>
            <span class="ch-arrow-icon">➔</span>
          </a>
        </div>
      </div>
    `;
  }).join('');
}

function renderCreators(useCases, config) {
  const gridContainer = document.getElementById('creatorsGrid');
  if (!gridContainer) return;

  const icons = {
    filmmakers: `📷`,
    podcasters: `🎙`,
    influencers: `👤`,
    ugc: `📹`,
    brands: `💎`,
    startups: `📈`
  };

  const previews = {
    filmmakers: {
      badge: 'FILMMAKERS',
      title: 'Precision lighting, silence, and cine-grade optics.',
      desc: 'Studio A provides an Aputure-rigged cyclorama, soundproof STC 55 isolation, and cinema-line cameras ready to roll in minutes.',
      img: '/assets/images/creator-house/creator-house-production.webp',
      btn: 'Book Filmmaking Stage →',
      discipline: 'Filmmaking'
    },
    podcasters: {
      badge: 'PODCASTERS',
      title: 'Broadcast visual fidelity and pristine vocal clarity.',
      desc: 'The Pod delivers radio-studio acoustic isolation, multi-cam 4K automated switching, and flattering warm key lighting for long-form dialogues.',
      img: '/assets/images/creator-house/creator-house-podcast.webp',
      btn: 'Book Podcast Suite →',
      discipline: 'Podcasting'
    },
    influencers: {
      badge: 'INFLUENCERS',
      title: 'Batch a month of viral hooks in a single afternoon.',
      desc: 'Jump between three dynamic aesthetic sets in Reels Lab, utilize teleprompters for flawless delivery, and offload instantly over 10Gbps fiber.',
      img: '/assets/images/creator-house/creator-house-hero.webp',
      btn: 'Book Reels Lab →',
      discipline: 'Short-Form Content'
    },
    ugc: {
      badge: 'UGC CREATORS',
      title: 'Commercial product quality on an agile schedule.',
      desc: 'Deliver sponsor-ready ad creatives with motorized overhead unboxing rigs, color-accurate CRI 98+ lighting, and lifestyle props.',
      img: '/assets/images/creator-house/creator-house-production.webp',
      btn: 'Book UGC Setup →',
      discipline: 'UGC Commercials'
    },
    brands: {
      badge: 'BRANDS',
      title: 'Production infrastructure without the agency markup.',
      desc: 'Scale internal content creation, shoot CEO keynotes, customer case studies, and brand campaigns in a controlled, premium environment.',
      img: '/assets/images/creator-house/creator-house-community.webp',
      btn: 'Book Brand Production →',
      discipline: 'Brand Content'
    },
    startups: {
      badge: 'STARTUPS',
      title: 'Punch above your weight with studio-grade content.',
      desc: 'Demo day video recordings, product launch walkthroughs with motorized turntable rigs, and executive storytelling without building an internal studio.',
      img: '/assets/images/creator-house/creator-house-hero.webp',
      btn: 'Book Startup Pass →',
      discipline: 'Startup Storytelling'
    }
  };

  gridContainer.innerHTML = useCases.slice(0, 6).map((uc, index) => `
    <div class="ch-creator-box ${index === 0 ? 'is-active' : ''}" data-creator-id="${uc.id}" role="button" tabindex="0" aria-label="Select ${uc.label} workflow">
      <div class="ch-creator-box__icon">${icons[uc.id] || '⚡'}</div>
      <h3 class="ch-creator-box__name">${uc.label}</h3>
      <p class="ch-creator-box__desc">${uc.tagline}</p>
    </div>
  `).join('');

  // Setup click and keyboard listener for categories
  const boxes = gridContainer.querySelectorAll('.ch-creator-box');
  
  function selectUseCase(id, updateHash = true) {
    boxes.forEach(b => {
      if (b.getAttribute('data-creator-id') === id) {
        b.classList.remove('is-inactive');
        b.classList.add('is-active');
      } else {
        b.classList.remove('is-active');
        b.classList.add('is-inactive');
      }
    });

    const current = previews[id] || previews.filmmakers;
    const badgeEl = document.getElementById('previewCategoryBadge');
    const titleEl = document.getElementById('previewCategoryTitle');
    const descEl = document.getElementById('previewCategoryDesc');
    const imgEl = document.getElementById('previewCategoryImg');
    const btnEl = document.getElementById('previewCategoryBtn');

    if (badgeEl) badgeEl.textContent = current.badge;
    if (titleEl) titleEl.textContent = current.title;
    if (descEl) descEl.textContent = current.desc;
    if (btnEl) {
      btnEl.textContent = current.btn;
      btnEl.setAttribute('data-discipline', current.discipline);
    }
    if (imgEl) {
      imgEl.style.opacity = '0';
      setTimeout(() => {
        imgEl.src = current.img;
        imgEl.style.opacity = '1';
      }, 150);
    }

    if (updateHash && window.history && window.history.pushState) {
      window.history.pushState(null, '', `#${id}`);
    }
  }

  boxes.forEach(box => {
    const id = box.getAttribute('data-creator-id');
    box.addEventListener('click', () => selectUseCase(id, true));
    box.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        selectUseCase(id, true);
      }
    });
  });

  // Expose selectUseCase for deep linking
  window.selectCreatorUseCase = selectUseCase;
}

/* =========================================================================
   NAVIGATION & MOBILE DRAWER (SECTION 28 & 45)
   ========================================================================= */
function initNavigation(config) {
  const nav = document.getElementById('chNav');
  const toggle = document.getElementById('chNavToggle');
  const drawer = document.getElementById('chMobileDrawer');
  const drawerLinks = drawer ? drawer.querySelectorAll('a, button') : [];

  // Sticky header background state
  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }, { passive: true });

  // Mobile menu toggle
  if (toggle && drawer) {
    function openDrawer() {
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      drawer.classList.remove('open');
      drawer.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', () => {
      if (drawer.classList.contains('open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    // Close when clicking any menu item & restore scrolling immediately
    drawerLinks.forEach(item => {
      item.addEventListener('click', () => {
        closeDrawer();
      });
    });

    // Close with Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        closeDrawer();
      }
    });
  }
}

/* =========================================================================
   SAME-PAGE ANCHOR SMOOTH SCROLLING (SECTION 42)
   ========================================================================= */
function initAnchorRouting(config) {
  const offset = (config && config.NAVBAR_HEIGHT_OFFSET) || 76;

  document.addEventListener('click', (e) => {
    const anchor = e.target.closest('a[href^="#"], .ch-smooth-scroll');
    if (!anchor) return;

    const href = anchor.getAttribute('href') || anchor.getAttribute('data-scroll-target');
    if (!href || href === '#' || href === '#!') return;

    const targetId = href.startsWith('#') ? href.slice(1) : href;
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      e.preventDefault();
      const topPos = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;

      window.scrollTo({
        top: Math.max(0, topPos),
        behavior: 'smooth'
      });

      if (window.history && window.history.pushState) {
        window.history.pushState(null, '', `#${targetId}`);
      }

      // Restore body overflow if mobile drawer was open
      const drawer = document.getElementById('chMobileDrawer');
      if (drawer && drawer.classList.contains('open')) {
        drawer.classList.remove('open');
        document.body.style.overflow = '';
      }
    }
  });
}

/* =========================================================================
   INITIAL URL HASH ROUTING & DEEP-LINKING (SECTION 31 & 32)
   ========================================================================= */
function handleInitialUrlHash(data, config) {
  const hash = window.location.hash ? window.location.hash.slice(1).toLowerCase() : '';
  if (!hash) return;

  setTimeout(() => {
    // 1. Check if hash matches a Space (e.g. #studio-a, #the-pod)
    const matchedSpace = data.spaces.find(s => s.id === hash);
    if (matchedSpace) {
      if (config && config.smoothScrollToTarget) {
        config.smoothScrollToTarget('#spaces', false);
      }
      openSpaceDetailModal(matchedSpace, data);
      return;
    }

    // 2. Check if hash matches a Creator Use-Case (e.g. #filmmakers, #podcasters)
    const matchedUseCase = data.useCases.find(uc => uc.id === hash);
    if (matchedUseCase && typeof window.selectCreatorUseCase === 'function') {
      if (config && config.smoothScrollToTarget) {
        config.smoothScrollToTarget('#creators', false);
      }
      window.selectCreatorUseCase(hash, false);
      return;
    }

    // 3. Check if hash matches #apply or #membership
    if (hash === 'apply') {
      openReservationModal('Founding Membership', config);
      return;
    }

    // 4. Default smooth scroll for sections
    const sec = document.getElementById(hash);
    if (sec && config && config.smoothScrollToTarget) {
      config.smoothScrollToTarget(hash, false);
    }
  }, 350);
}

/* =========================================================================
   UNIFIED CINEMATIC SCROLL ENGINE & VELOCITY TRACKER
   ========================================================================= */
function initUnifiedScrollEngine() {
  let lastScrollY = window.scrollY;
  let scrollVelocity = 0;
  let smoothVelocity = 0;

  // Cache interactive elements
  const mobileProgress = document.getElementById('mobileProgress');
  const progressItems = document.querySelectorAll('.ch-progress-item');
  const sections = ['hero', 'why', 'journey', 'spaces', 'statementMoment', 'membership'];
  const sectionElements = sections.map(id => document.getElementById(id)).filter(Boolean);

  // Hero elements
  const heroLeft = document.getElementById('heroLeftContent');
  const heroStageBg = document.getElementById('heroStageBg');
  const floatingNodes = document.querySelectorAll('#heroFloatingNodes .ch-stage__node-pill');

  // Marquee
  const marqueeTrack = document.getElementById('marqueeTrack');
  let marqueePos = 0;
  let isMarqueeHovered = false;
  if (marqueeTrack) {
    marqueeTrack.addEventListener('mouseenter', () => isMarqueeHovered = true);
    marqueeTrack.addEventListener('mouseleave', () => isMarqueeHovered = false);
  }

  // Section 01: Split Text
  const splitIdea = document.getElementById('splitIdea');
  const splitPublish = document.getElementById('splitPublish');
  const splitTimelineLine = document.getElementById('splitTimelineLine');
  const whyHeader = document.getElementById('whyHeader');

  // Section 02: Journey Line
  const journeySection = document.getElementById('journey');
  const journeyFills = document.querySelectorAll('.ch-journey-arrow__fill');

  // Section 03: Horizontal Track Navigation
  const spacesContainer = document.getElementById('horizontalTrackContainer');
  const prevBtn = document.getElementById('spacesPrevBtn');
  const nextBtn = document.getElementById('spacesNextBtn');
  if (prevBtn && spacesContainer) {
    prevBtn.addEventListener('click', () => spacesContainer.scrollBy({ left: -340, behavior: 'smooth' }));
  }
  if (nextBtn && spacesContainer) {
    nextBtn.addEventListener('click', () => spacesContainer.scrollBy({ left: 340, behavior: 'smooth' }));
  }

  // Section 05: Statement Hero Text
  const statementHeroText = document.getElementById('statementHeroText');
  const statementMoment = document.getElementById('statementMoment');

  // Section 06: Odometer & Membership
  const pricingCard = document.getElementById('pricingCard');
  const odometerPrice = document.getElementById('odometerPrice');
  const checkItems = document.querySelectorAll('.ch-membership-check-item');
  let odometerStarted = false;

  // Staggered reveal for feature cards via IntersectionObserver
  const featuresGrid = document.getElementById('featuresGrid');
  if (featuresGrid && 'IntersectionObserver' in window) {
    const cardsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const cards = featuresGrid.querySelectorAll('.ch-why-card');
          cards.forEach((card, idx) => {
            setTimeout(() => {
              card.classList.remove('is-hidden');
              card.classList.add('is-revealed');
            }, idx * 120);
          });
          cardsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    cardsObserver.observe(featuresGrid);
  }

  // Odometer & Benefits reveal via IntersectionObserver
  if (pricingCard && 'IntersectionObserver' in window) {
    const pricingObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !odometerStarted) {
          odometerStarted = true;
          animateOdometer(odometerPrice, 3499, 1100);
          checkItems.forEach((item, idx) => {
            setTimeout(() => {
              item.classList.add('is-revealed');
            }, 100 + idx * 80);
          });
          pricingObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    pricingObserver.observe(pricingCard);
  }

  // Main RAF Scroll & Physics Loop
  function tick() {
    const currentScrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const totalProgress = docHeight > 0 ? currentScrollY / docHeight : 0;

    // Calculate Scroll Velocity with smoothing
    scrollVelocity = currentScrollY - lastScrollY;
    smoothVelocity += (scrollVelocity - smoothVelocity) * 0.12;
    lastScrollY = currentScrollY;

    // 1. Mobile & Desktop Progress Updates
    if (mobileProgress) {
      mobileProgress.style.width = `${Math.min(totalProgress * 100, 100)}%`;
    }

    // Active Section Spy
    let currentActiveIndex = 0;
    sectionElements.forEach((sec, idx) => {
      const top = sec.offsetTop - 300;
      if (currentScrollY >= top) currentActiveIndex = idx;
    });

    progressItems.forEach((item, idx) => {
      if (idx === currentActiveIndex) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // 2. Hero Scroll Parallax (Phases 1, 2)
    if (currentScrollY < 900) {
      const heroProgress = Math.min(currentScrollY / 700, 1);
      
      if (heroLeft) {
        const scaleVal = 1 - heroProgress * 0.08;
        const opacityVal = 1 - heroProgress * 0.35;
        heroLeft.style.transform = `scale(${scaleVal}) translateY(${heroProgress * 40}px)`;
        heroLeft.style.opacity = `${opacityVal}`;
      }

      if (heroStageBg) {
        heroStageBg.style.transform = `scale(${1 + heroProgress * 0.12})`;
      }

      floatingNodes.forEach(node => {
        const speed = parseFloat(node.getAttribute('data-speed')) || 1;
        const drift = heroProgress * 55 * speed;
        node.style.transform = `translateY(${-drift}px)`;
      });
    }

    // 3. Dynamic Velocity-Responsive Marquee
    if (marqueeTrack) {
      const baseSpeed = isMarqueeHovered ? 0.3 : 1.2;
      const dynamicSpeed = baseSpeed + Math.min(Math.abs(smoothVelocity) * 0.25, 7);
      marqueePos -= dynamicSpeed;
      if (marqueePos <= -marqueeTrack.scrollWidth / 2) {
        marqueePos = 0;
      }
      marqueeTrack.style.transform = `translateX(${marqueePos}px)`;
    }

    // 4. "Everything Between Idea and Publish" Split Movement
    if (whyHeader) {
      const whyRect = whyHeader.getBoundingClientRect();
      const inView = whyRect.top < window.innerHeight && whyRect.bottom > 0;
      if (inView) {
        const progress = Math.max(0, Math.min(1, (window.innerHeight - whyRect.top) / (window.innerHeight + whyRect.height)));
        if (splitIdea) splitIdea.style.transform = `translateX(${-progress * 18}px)`;
        if (splitPublish) splitPublish.style.transform = `translateX(${progress * 18}px)`;
        if (splitTimelineLine) splitTimelineLine.style.width = `${Math.min(progress * 120, 100)}%`;
      }
    }

    // 5. Creator Journey Extending Progress Line
    if (journeySection && journeyFills.length > 0) {
      const journeyRect = journeySection.getBoundingClientRect();
      if (journeyRect.top < window.innerHeight && journeyRect.bottom > 0) {
        const p = Math.max(0, Math.min(1, (window.innerHeight - journeyRect.top) / (window.innerHeight + journeyRect.height * 0.7)));
        journeyFills.forEach((fill, idx) => {
          const stepThreshold = (idx + 1) / (journeyFills.length + 1);
          if (p >= stepThreshold) {
            fill.style.width = '100%';
          } else {
            const stepProgress = Math.max(0, (p - (idx / (journeyFills.length + 1))) * (journeyFills.length + 1));
            fill.style.width = `${Math.min(stepProgress * 100, 100)}%`;
          }
        });
      }
    }

    // 6. Statement Moment Typography Scale
    if (statementMoment && statementHeroText) {
      const stRect = statementMoment.getBoundingClientRect();
      if (stRect.top < window.innerHeight && stRect.bottom > 0) {
        const p = Math.max(0, Math.min(1, (window.innerHeight - stRect.top) / (window.innerHeight + stRect.height)));
        const scaleVal = 0.95 + p * 0.1;
        statementHeroText.style.transform = `scale(${Math.min(scaleVal, 1.05)})`;
      }
    }

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);
}

/* =========================================================================
   ODOMETER NUMBER ANIMATION
   ========================================================================= */
function animateOdometer(element, targetNumber, duration) {
  if (!element) return;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const currentVal = Math.floor(ease * targetNumber);

    element.textContent = `₹${currentVal.toLocaleString('en-IN')}`;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = `₹${targetNumber.toLocaleString('en-IN')}`;
    }
  }

  requestAnimationFrame(update);
}

/* =========================================================================
   MAGNETIC BUTTONS (DESKTOP) (SECTION 38)
   ========================================================================= */
function initMagneticButtons() {
  const isTouch = window.matchMedia('(hover: none) or (pointer: coarse)').matches;
  if (isTouch) return;

  const buttons = document.querySelectorAll('.ch-btn--lime, .ch-btn--primary, .ch-btn--outline, .ch-hero__showreel-btn, .ch-arrow-btn');

  buttons.forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = `translate(${x * 0.25}px, ${y * 0.25}px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0px, 0px)';
    });
  });
}

/* =========================================================================
   CONTEXT-AWARE CUSTOM CURSOR (DESKTOP)
   ========================================================================= */
function initCustomCursor() {
  const dot = document.getElementById('chCursorDot');
  const ring = document.getElementById('chCursorRing');
  if (!dot || !ring) return;

  const isTouch = window.matchMedia('(hover: none) or (pointer: coarse)').matches;
  if (isTouch) {
    dot.style.display = 'none';
    ring.style.display = 'none';
    return;
  }

  let mouseX = -100, mouseY = -100;
  let ringX = -100, ringY = -100;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
  });

  function renderCursor() {
    ringX += (mouseX - ringX) * 0.18;
    ringY += (mouseY - ringY) * 0.18;
    ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
    requestAnimationFrame(renderCursor);
  }
  requestAnimationFrame(renderCursor);

  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest('a, button, .ch-space-card-4, .ch-btn, .ch-why-preview, .ch-hero__showreel-btn, input, select, textarea');
    if (!target) {
      document.body.className = '';
      return;
    }

    if (target.closest('.ch-why-preview') || target.closest('.ch-hero__showreel-btn')) {
      document.body.className = 'cursor-play';
      ring.querySelector('span').textContent = 'PLAY';
    } else if (target.closest('.ch-space-card-4')) {
      document.body.className = 'cursor-explore';
      ring.querySelector('span').textContent = 'EXPLORE';
    } else if (target.tagName === 'IMG' || target.closest('.ch-membership-col-right')) {
      document.body.className = 'cursor-view';
      ring.querySelector('span').textContent = 'VIEW';
    } else if (target.classList.contains('ch-btn') || target.tagName === 'BUTTON') {
      document.body.className = 'cursor-cta';
      ring.querySelector('span').textContent = 'CLICK';
    } else {
      document.body.className = 'cursor-hover';
    }
  });

  document.addEventListener('mouseout', (e) => {
    const target = e.target.closest('a, button, .ch-space-card-4, .ch-btn, .ch-why-preview, .ch-hero__showreel-btn, input, select, textarea');
    if (target) {
      document.body.className = '';
    }
  });
}

/* =========================================================================
   MODAL HANDLERS & 7-FIELD MEMBERSHIP APPLICATION (SECTION 33 & 37)
   ========================================================================= */
function initModalHandlers(data, config) {
  const backdrop = document.getElementById('chModalBackdrop');
  const modalContent = document.getElementById('chModalContent');
  const closeBtn = document.getElementById('chModalClose');
  if (!backdrop || !modalContent || !closeBtn) return;

  function closeModal() {
    backdrop.classList.remove('active');
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && backdrop.classList.contains('active')) closeModal();
  });

  // Global trigger for reservation modal
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.open-reserve-modal');
    if (!trigger) return;
    e.preventDefault();
    const discipline = trigger.getAttribute('data-discipline') || 'Filmmaking';
    openReservationModal(discipline, config);
  });

  // Global trigger for space details
  document.addEventListener('click', (e) => {
    const cardOrBtn = e.target.closest('.open-space-card, .open-space-modal, .ch-stage__node-pill');
    if (!cardOrBtn) return;

    const spaceId = cardOrBtn.getAttribute('data-space-id');
    const space = data.spaces.find(s => s.id === spaceId);
    if (space) {
      e.preventDefault();
      openSpaceDetailModal(space, data);
    }
  });

  // Global trigger for showreel modal
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.open-showreel-modal');
    if (!trigger) return;
    e.preventDefault();
    openShowreelModal(config);
  });
}

function openShowreelModal(config) {
  const backdrop = document.getElementById('chModalBackdrop');
  const modalContent = document.getElementById('chModalContent');
  if (!backdrop || !modalContent) return;

  modalContent.innerHTML = `
    <div style="position: relative; width: 100%; aspect-ratio: 16/9; background: #000; border-radius: var(--radius-md); overflow: hidden; margin-bottom: 1.5rem;">
      <img src="/assets/images/creator-house/creator-house-production.webp" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.88;" alt="Creator House Showreel Tour">
      <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(0,0,0,0.55); padding: 1rem; text-align: center;">
        <div style="width: 64px; height: 64px; border-radius: 50%; background: var(--ch-lime); color: #070709; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 1rem; box-shadow: 0 0 30px var(--ch-lime-glow);">▶</div>
        <span style="font-family: var(--font-display); font-weight: 800; font-size: 1.25rem; color: #fff; letter-spacing: 0.05em;">CREATOR HOUSE // PRODUCTION SHOWREEL 2026</span>
        <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--ch-lime); margin-top: 0.4rem;">4K CINEMA GEAR • ACOUSTIC SUITES • BENGALURU</span>
      </div>
    </div>
    <p style="color: var(--ch-text-secondary); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
      Take a 90-second tour through Creator House's pre-lit stages, soundproof broadcast studios, and 10Gbps fiber-linked color suites built specifically for creators, podcasters, and brands.
    </p>
    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
      <button class="ch-btn ch-btn--lime open-reserve-modal ch-btn--block-mobile" data-discipline="Showreel Tour" style="flex: 1;">
        Schedule an In-Person Studio Tour →
      </button>
    </div>
  `;

  backdrop.classList.add('active');
  backdrop.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function openSpaceDetailModal(space, data) {
  const backdrop = document.getElementById('chModalBackdrop');
  const modalContent = document.getElementById('chModalContent');
  if (!backdrop || !modalContent) return;

  // Update hash safely
  if (window.history && window.history.pushState) {
    window.history.pushState(null, '', `#${space.id}`);
  }

  modalContent.innerHTML = `
    <div style="position: relative; width: 100%; height: 260px; border-radius: var(--radius-md); overflow: hidden; margin-bottom: 2rem; background: #000;">
      <img src="${space.image}" alt="${space.name}" style="width: 100%; height: 100%; object-fit: cover;">
      <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(18, 18, 23, 0.95) 100%);"></div>
      <div style="position: absolute; bottom: 1.5rem; left: 1.5rem; right: 1.5rem;">
        <div class="ch-badge-index" style="margin-bottom: 0.25rem;"><span class="num">${space.id.toUpperCase()}</span> // FACILITIES</div>
        <h2 style="font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #fff;">${space.name}</h2>
      </div>
    </div>

    <p style="color: var(--ch-text-secondary); font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem;">
      ${space.summary}
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 1.25rem; background: #0B0B0E; border-radius: var(--radius-sm); border: 1px solid var(--ch-border); margin-bottom: 2rem;">
      <div>
        <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--ch-lime); text-transform: uppercase;">Dimensions</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: #fff;">${space.dimensions}</div>
      </div>
      <div>
        <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--ch-lime); text-transform: uppercase;">Capacity</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: #fff;">${space.capacity}</div>
      </div>
    </div>

    <div style="margin-bottom: 2rem;">
      <h4 style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--ch-lime); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1rem;">
        Infrastructure & Technical Rigging
      </h4>
      <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.75rem;">
        ${space.specs.map(spec => `
          <li style="display: flex; align-items: center; gap: 0.75rem; font-size: 0.9rem; color: #e5e5ea;">
            <span style="width: 5px; height: 5px; border-radius: 50%; background: var(--ch-lime); flex-shrink: 0;"></span>
            <span>${spec}</span>
          </li>
        `).join('')}
      </ul>
    </div>

    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
      <button class="ch-btn ch-btn--lime open-reserve-modal ch-btn--block-mobile" data-discipline="${space.name}" style="flex: 1;">
        REQUEST SPACE ACCESS →
      </button>
      <button class="ch-btn ch-btn--outline ch-btn--block-mobile" onclick="document.getElementById('chModalBackdrop').classList.remove('active'); document.body.style.overflow='';">
        Back to Spaces
      </button>
    </div>
  `;

  backdrop.classList.add('active');
  backdrop.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

/**
 * 7-Field Membership Application Form (Section 33)
 * Fields: Name, Email, Phone, Creator type, Primary content type, Instagram/YouTube/portfolio, Message
 * CTA: "REQUEST ACCESS →"
 * Success: "You're on the list."
 */
function openReservationModal(defaultDiscipline = 'Founding Membership', config) {
  const backdrop = document.getElementById('chModalBackdrop');
  const modalContent = document.getElementById('chModalContent');
  if (!backdrop || !modalContent) return;

  const creatorTypes = [
    { value: 'Filmmaker', label: 'Filmmaker / Commercial Director' },
    { value: 'Podcaster', label: 'Podcaster / Broadcast Host' },
    { value: 'Influencer', label: 'Influencer / Content Creator' },
    { value: 'UGC Creator', label: 'UGC Creator / Specialist' },
    { value: 'Brand Content Team', label: 'Brand / Agency Content Team' },
    { value: 'Startup Founder', label: 'Startup Founder / Marketer' },
    { value: 'Other', label: 'Independent Artist / Other' }
  ];

  const contentTypes = [
    { value: 'Long-Form Video', label: 'Long-Form Cinematic Video / YouTube' },
    { value: 'Podcast Audio & Video', label: 'Multi-Cam Podcast / Dialogue' },
    { value: 'Short-Form Reels/TikTok', label: 'Vertical Reels / TikTok / Shorts' },
    { value: 'Commercial Ads & UGC', label: 'Commercial Ads / UGC Campaigns' },
    { value: 'Multi-Cam Live Stream', label: 'Live Broadcast / Product Launches' },
    { value: 'Post-Production Only', label: 'Color Grading / Sound Mixing / Post' }
  ];

  modalContent.innerHTML = `
    <div class="ch-badge-index" style="margin-bottom: 0.75rem;">
      <span class="num">DROP 01</span>
      <span>FOUNDING CREATOR APPLICATION</span>
    </div>
    <h2 style="font-family: var(--font-display); font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; color: #FFFFFF;">
      Claim Early-Bird Membership
    </h2>
    <p style="color: var(--ch-text-secondary); font-size: 0.95rem; line-height: 1.5; margin-bottom: 1.75rem;">
      Lock in priority access to Bengaluru's premier creator infrastructure at <strong style="color: #fff;">₹3,499/mo</strong>. Applications are reviewed on a rolling basis.
    </p>

    <form id="chReservationForm" novalidate>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;" class="ch-form-2col">
        <div class="ch-form-group">
          <label class="ch-form-label" for="chName">Name *</label>
          <input class="ch-form-input" type="text" id="chName" required placeholder="Maya Chen" autocomplete="name">
          <span class="ch-form-error" id="chNameError" style="display: none; color: var(--ch-coral); font-size: 0.75rem; margin-top: 0.25rem;">Please enter your name</span>
        </div>

        <div class="ch-form-group">
          <label class="ch-form-label" for="chEmail">Email *</label>
          <input class="ch-form-input" type="email" id="chEmail" required placeholder="maya@creator.studio" autocomplete="email">
          <span class="ch-form-error" id="chEmailError" style="display: none; color: var(--ch-coral); font-size: 0.75rem; margin-top: 0.25rem;">Please enter a valid email</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;" class="ch-form-2col">
        <div class="ch-form-group">
          <label class="ch-form-label" for="chPhone">Phone *</label>
          <input class="ch-form-input" type="tel" id="chPhone" required placeholder="+91 98765 43210" autocomplete="tel">
          <span class="ch-form-error" id="chPhoneError" style="display: none; color: var(--ch-coral); font-size: 0.75rem; margin-top: 0.25rem;">Please enter your phone number</span>
        </div>

        <div class="ch-form-group">
          <label class="ch-form-label" for="chCreatorType">Creator Type *</label>
          <select class="ch-form-select" id="chCreatorType" required>
            ${creatorTypes.map(ct => `
              <option value="${ct.value}" ${defaultDiscipline.toLowerCase().includes(ct.value.toLowerCase().split(' ')[0]) ? 'selected' : ''}>
                ${ct.label}
              </option>
            `).join('')}
          </select>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;" class="ch-form-2col">
        <div class="ch-form-group">
          <label class="ch-form-label" for="chContentType">Primary Content Type *</label>
          <select class="ch-form-select" id="chContentType" required>
            ${contentTypes.map(ct => `<option value="${ct.value}">${ct.label}</option>`).join('')}
          </select>
        </div>

        <div class="ch-form-group">
          <label class="ch-form-label" for="chPortfolio">Instagram / YouTube / Portfolio *</label>
          <input class="ch-form-input" type="text" id="chPortfolio" required placeholder="@channel or youtube.com/@...">
          <span class="ch-form-error" id="chPortfolioError" style="display: none; color: var(--ch-coral); font-size: 0.75rem; margin-top: 0.25rem;">Please enter your handle or portfolio URL</span>
        </div>
      </div>

      <div class="ch-form-group">
        <label class="ch-form-label" for="chMessage">Message (Optional)</label>
        <textarea class="ch-form-input" id="chMessage" rows="3" placeholder="Tell us about what you produce, your gear requirements, or preferred studio access timing..." style="resize: vertical; min-height: 70px;"></textarea>
      </div>

      <button type="submit" class="ch-btn ch-btn--lime ch-btn--block-mobile" id="chSubmitBtn" style="width: 100%; margin-top: 0.75rem; padding: 1.1rem;">
        <span>REQUEST ACCESS →</span>
      </button>

      <p style="text-align: center; color: var(--ch-text-muted); font-size: 0.75rem; margin-top: 0.75rem;">
        No payment required today. Locking your spot gives priority early-bird slot access.
      </p>
    </form>
  `;

  backdrop.classList.add('active');
  backdrop.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  const form = document.getElementById('chReservationForm');
  const submitBtn = document.getElementById('chSubmitBtn');

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();

    // Basic Validation
    const nameEl = document.getElementById('chName');
    const emailEl = document.getElementById('chEmail');
    const phoneEl = document.getElementById('chPhone');
    const portfolioEl = document.getElementById('chPortfolio');
    const creatorTypeEl = document.getElementById('chCreatorType');
    const contentTypeEl = document.getElementById('chContentType');
    const messageEl = document.getElementById('chMessage');

    let isValid = true;

    [nameEl, emailEl, phoneEl, portfolioEl].forEach(field => {
      const err = document.getElementById(`${field.id}Error`);
      if (!field.value.trim() || (field.type === 'email' && !field.value.includes('@'))) {
        if (err) err.style.display = 'block';
        field.style.borderColor = 'var(--ch-coral)';
        isValid = false;
      } else {
        if (err) err.style.display = 'none';
        field.style.borderColor = '';
      }
    });

    if (!isValid) return;

    // Loading state feedback (Section 37)
    submitBtn.classList.add('is-loading');

    const appData = {
      name: nameEl.value.trim(),
      email: emailEl.value.trim(),
      phone: phoneEl.value.trim(),
      creatorType: creatorTypeEl.value,
      contentType: contentTypeEl.value,
      portfolio: portfolioEl.value.trim(),
      message: messageEl.value.trim()
    };

    // Record data via centralized application recorder
    let recorded = {};
    if (config && typeof config.recordMembershipApplication === 'function') {
      recorded = config.recordMembershipApplication(appData);
    } else {
      recorded = { ...appData, refId: `CH-${Date.now().toString().slice(-6)}` };
    }

    setTimeout(() => {
      modalContent.innerHTML = `
        <div style="text-align: center; padding: 2rem 0;">
          <div style="width: 64px; height: 64px; border-radius: 50%; background: rgba(200, 255, 0, 0.15); color: var(--ch-lime); display: flex; align-items: center; justify-content: center; font-size: 1.85rem; margin: 0 auto 1.5rem auto; border: 1px solid var(--ch-lime); box-shadow: 0 0 25px var(--ch-lime-glow);">✓</div>
          <div class="ch-badge-index" style="margin-bottom: 0.5rem;"><span class="num">APPLICATION RECORDED</span> // ${recorded.refId || 'DROP 01'}</div>
          <h2 style="font-family: var(--font-display); font-size: 2.25rem; font-weight: 800; margin-bottom: 1rem; color: #FFFFFF;">
            You're on the list.
          </h2>
          <p style="color: var(--ch-text-secondary); font-size: 1.05rem; line-height: 1.6; max-width: 480px; margin: 0 auto 1.5rem auto;">
            Welcome to the roster, <strong style="color: #fff;">${escapeHtml(recorded.name)}</strong>. Your application for <span style="color: var(--ch-lime);">${escapeHtml(recorded.creatorType)}</span> access has been received.
          </p>
          <div style="background: #0B0B0E; border: 1px solid var(--ch-border); border-radius: var(--radius-sm); padding: 1.25rem; max-width: 440px; margin: 0 auto 2rem auto; text-align: left; font-size: 0.85rem; color: var(--ch-text-secondary);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
              <span>Reference Number:</span>
              <strong style="color: #fff; font-family: var(--font-mono);">${recorded.refId}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
              <span>Confirmation Email:</span>
              <strong style="color: #fff;">${escapeHtml(recorded.email)}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>Drop Rate Status:</span>
              <span style="color: var(--ch-lime); font-weight: 700;">Locked at ₹3,499/mo</span>
            </div>
          </div>
          <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <button class="ch-btn ch-btn--lime ch-btn--block-mobile" id="closeSuccessBtn">
              BACK TO CREATOR HOUSE →
            </button>
          </div>
        </div>
      `;

      const closeSuccessBtn = document.getElementById('closeSuccessBtn');
      if (closeSuccessBtn) {
        closeSuccessBtn.addEventListener('click', () => {
          backdrop.classList.remove('active');
          document.body.style.overflow = '';
        });
      }
    }, 450);
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>"']/g, (m) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[m]);
}
