/**
 * CREATOR HOUSE — DATA STORE
 * Centralized, structured data configuration for Creator House
 * Enables seamless CMS integration and easy content updates.
 */

window.CREATOR_HOUSE_DATA = {
  brand: {
    name: "CREATOR HOUSE",
    parent: "SZ VENTURES",
    tagline: "Your Content. Your Space. Your Production Engine.",
    subtitle: "A premium creator infrastructure and production ecosystem built for ambitious creators, filmmakers, podcasters, influencers, UGC creators, brands, and creative teams.",
    location: "Bengaluru, India",
    statusBadge: "FOUNDING CREATOR ACCESS // LIMITED TO 300 PASSES",
    pricing: {
      currency: "₹",
      amount: "3,499",
      period: "+ taxes / month",
      originalPrice: "₹5,999",
      badge: "FOUNDING CREATOR DROP",
      headline: "LOCK IN YOUR SPACE.",
      subhead: "Direct access to Bengaluru's most advanced creator production infrastructure at exclusive early-adopter pricing."
    }
  },

  marqueeItems: [
    "SHOOT",
    "EDIT",
    "PODCAST",
    "REELS",
    "UGC",
    "COLLABORATE",
    "CREATE",
    "PUBLISH",
    "BROADCAST",
    "DIRECT"
  ],

  valueProps: [
    {
      id: "01",
      title: "PLUG & PLAY",
      description: "Professional cinema cameras, pre-calibrated lighting grids, wireless audio, and acoustic-treated sets ready the moment you walk in. Zero setup time wasted.",
      specs: ["Sony FX3 / FX6 Cine Line", "Aputure 600d & Nova RGB", "Sennheiser & Rode Wireless", "Instant Calibrated Lighting"],
      icon: "camera"
    },
    {
      id: "02",
      title: "VIBE-OPTIMIZED SPACES",
      description: "Every room is purpose-architected for specific content formats: high-retention reels, intimate 4K podcasts, commercial UGC, and long-form visual essays.",
      specs: ["Acoustic Floating Floors", "Motorized Backdrops", "High-CRI 98+ Tunable Light", "Multi-Angle Rigging"],
      icon: "layout"
    },
    {
      id: "03",
      title: "CREATOR NETWORK",
      description: "A private ecosystem of elite digital storytellers, commercial directors, sound engineers, and venture-backed brand partners collaborating under one roof.",
      specs: ["Resident Directors & Editors", "Brand Deal Matchmaking", "Private Screenings", "Cross-Channel Collabs"],
      icon: "users"
    },
    {
      id: "04",
      title: "PRODUCTION SUPPORT",
      description: "Technical assistance on demand. From gaffing and audio monitoring to memory offloading and workflow optimization, our team has your back.",
      specs: ["Dedicated In-House Gaffer", "10Gbps Symmetrical Ingest", "Hardware Color Grading", "Backup Battery & UPS"],
      icon: "cpu"
    }
  ],

  journeySteps: [
    {
      step: "01",
      title: "IDEATE",
      subtitle: "Concepts, scripts & visual treatments",
      description: "Formulate treatments, storyboard shots, and collaborate with creative directors in our soundproof ideation lounge equipped with high-speed reference screens.",
      tag: "PRE-PRODUCTION"
    },
    {
      step: "02",
      title: "SHOOT",
      subtitle: "Professional studio environment",
      description: "Walk into an environment dialed in to your specific color palette and lighting ratio. Multi-cam capture synced with timecode and isolated audio tracks.",
      tag: "PRODUCTION"
    },
    {
      step: "03",
      title: "EDIT",
      subtitle: "High-throughput post-production",
      description: "Offload footage over 10Gbps local fiber into calibrated DaVinci Resolve suites with Apple Pro Display XDR reference monitors and dedicated render blades.",
      tag: "POST-PRODUCTION"
    },
    {
      step: "04",
      title: "COLLABORATE",
      subtitle: "Creators, editors, designers & brands",
      description: "Test cuts with resident creators, get rapid editorial feedback, and tap into sound designers and colorists ready to elevate your visual identity.",
      tag: "OPTIMIZATION"
    },
    {
      step: "05",
      title: "PUBLISH",
      subtitle: "Ready for YouTube, TikTok & global screens",
      description: "Export pristine, algorithm-optimized masters that command attention, increase watch-time retention, and stand out in the most competitive feeds.",
      tag: "DISTRIBUTION"
    }
  ],

  spaces: [
    {
      id: "studio-a",
      name: "STUDIO A",
      tagline: "Main Production Studio",
      category: "Cinematic Long-Form & Commercials",
      image: "/assets/images/creator-house/creator-house-production.webp",
      dimensions: "1,200 sq.ft • 14ft Ceiling Height",
      capacity: "Up to 12 crew members",
      summary: "Full cyclorama studio engineered for commercial shoots, high-concept music videos, and multi-cam talk shows with an overhead motorized lighting truss.",
      specs: [
        "Floor-to-ceiling Cyclorama Infinity Curve",
        "Overhead Motorized DMX-controlled Lighting Grid",
        "3x Sony FX6 Cinema Cameras with GM Primes",
        "Dedicated Sound Isolation Booth & Tech Gallery"
      ]
    },
    {
      id: "the-pod",
      name: "THE POD",
      tagline: "Podcast & Interview Room",
      category: "Broadcast Audio & Visual Dialogues",
      image: "/assets/images/creator-house/creator-house-podcast.webp",
      dimensions: "450 sq.ft • Floating Acoustic Floor",
      capacity: "4 hosts / guests + operator",
      summary: "Broadcast-grade acoustic environment with warm wood diffraction panels, 4K multi-cam automated switching, and warm directional key lighting.",
      specs: [
        "NRC 0.95 Acoustic Absorption & Slatted Wood Wall",
        "4x Shure SM7B Broadcast Mics + Cloudlifters",
        "Blackmagic ATEM Mini Extreme ISO 4K Switcher",
        "Custom Curated Furniture & Warm Amber Lighting"
      ]
    },
    {
      id: "reels-lab",
      name: "REELS LAB",
      tagline: "Short-Form Content Studio",
      category: "TikTok, Shorts & Rapid UGC",
      image: "/assets/images/creator-house/creator-house-hero.webp",
      dimensions: "600 sq.ft • Modular Multi-Set",
      capacity: "Up to 6 creators",
      summary: "Optimized for vertical-first production with ultra-fast set changes, RGB lighting presets, overhead mirrorless top-down rigs, and instant phone teleprompters.",
      specs: [
        "3 Modular Set Corners (Minimalist, Tech-Dark, Warm Living)",
        "Overhead Motorized Top-Down Rig for Product Unboxing",
        "Nanlite PavoTube II 30X Dynamic RGB Systems",
        "Instant Wireless Video Monitoring to iPad Pros"
      ]
    },
    {
      id: "studio-b",
      name: "STUDIO B",
      tagline: "Portrait & Product Studio",
      category: "Commercial Stills & Motion Macro",
      image: "/assets/images/creator-house/creator-house-production.webp",
      dimensions: "550 sq.ft • Continuous White/Black Seamless",
      capacity: "Up to 5 creators",
      summary: "Specialized for commercial product films, editorial fashion portraits, and high-speed motion with motorized turntables and macro probe lenses.",
      specs: [
        "12 Motorized Seamless Paper Backdrops (Curated Palette)",
        "High-Speed Motorized 360 Turntable with Keyframe Sync",
        "Laowa 24mm f/14 Probe Cine Lens Package",
        "Broncolor High-Speed Strobe & Continuous Dual Rig"
      ]
    },
    {
      id: "edit-suite",
      name: "EDIT SUITE",
      tagline: "Post-Production Environment",
      category: "Color Grading, VFX & Sound Mastering",
      image: "/assets/images/creator-house/creator-house-podcast.webp",
      dimensions: "350 sq.ft • Calibrated Dimming Room",
      capacity: "1–3 editors & directors",
      summary: "Critical monitoring room equipped for DaVinci Resolve color grading, Dolby Atmos headphone mastering, and high-bandwidth direct render pipelines.",
      specs: [
        "Dual Apple Pro Display XDR (Reference 1000 nits)",
        "DaVinci Resolve Mini Panel & Tangent Ripple",
        "Genelec 8030C Active Studio Reference Monitors",
        "Direct 10Gbps Ingest to 100TB NVMe RAID Storage"
      ]
    },
    {
      id: "creator-lounge",
      name: "CREATOR LOUNGE",
      tagline: "Collaboration & Community",
      category: "Ideation, Screenings & Networking",
      image: "/assets/images/creator-house/creator-house-community.webp",
      dimensions: "1,500 sq.ft • Open Social Commons",
      capacity: "40+ creators for community events",
      summary: "The beating heart of Creator House. Sip craft cold brew, brainstorm scripts, screen rough cuts on the 120-inch 4K laser projection wall, and meet co-creators.",
      specs: [
        "120-inch 4K Laser Projection Theater for Rough-Cuts",
        "Specialty Espresso Bar & Craft Hydration Station",
        "High-density Gigabit Mesh & Private Call Pods",
        "Weekly Creator Roundtables & Private Brand Showcases"
      ]
    }
  ],

  useCases: [
    {
      id: "filmmakers",
      label: "FILMMAKERS",
      tagline: "Shoot cinematic projects.",
      headline: "Precision lighting, silence, and cine-grade optics.",
      description: "Eliminate the logistical nightmare of renting bare halls and hauling trucks of grip equipment. Studio A gives you an Aputure-rigged cyclorama and cinema-line cameras ready to roll in minutes.",
      keyCapabilities: [
        "14ft High Grid with wireless DMX control",
        "Complete flags, diffusion, C-stands, and boom arms",
        "Acoustic rating STC 55 with zero street noise bleed",
        "Client viewing gallery with wireless director monitors"
      ]
    },
    {
      id: "podcasters",
      label: "PODCASTERS",
      tagline: "Record polished conversations.",
      headline: "Broadcast visual fidelity and pristine vocal clarity.",
      description: "Stop recording podcasts in echoey bedrooms or makeshift offices. The Pod delivers radio-studio isolation, flattering studio illumination, and synced multi-cam 4K feeds recorded to separate SSDs.",
      keyCapabilities: [
        "Shure SM7B broadcast chain with pristine low-noise gain",
        "Multi-angle 4K cameras dialed to cinematic depth of field",
        "Instant ISO recording for multi-track editing",
        "Acoustically tuned environment for broadcast delivery"
      ]
    },
    {
      id: "influencers",
      label: "INFLUENCERS",
      tagline: "Create consistent short-form content.",
      headline: "Batch a month of viral hooks in a single afternoon.",
      description: "High-retention content requires lighting that pops and sets that change. Jump between three dynamic aesthetic sets in Reels Lab, utilize teleprompters for flawless delivery, and offload instantly.",
      keyCapabilities: [
        "One-touch RGB scene presets on wall touchscreens",
        "Ultra-bright eye-level keylights that make skin tones glow",
        "Customizable branded backdrop elements",
        "Instant AirDrop and cloud backup station"
      ]
    },
    {
      id: "ugc",
      label: "UGC CREATORS",
      tagline: "Produce high-volume brand content.",
      headline: "Commercial product quality on an agile schedule.",
      description: "Deliver sponsor-ready ad creatives with macro product details, pristine unboxing angles, and studio audio that outclasses standard creator deliverables.",
      keyCapabilities: [
        "Motorized overhead camera mounts for hands-free unboxings",
        "Color-accurate CRI 98+ lighting for true-to-life product colors",
        "Curated lifestyle props, surfaces, and textured backdrops",
        "High-speed export presets for Meta, TikTok & YouTube Ads"
      ]
    },
    {
      id: "brands",
      label: "BRANDS",
      tagline: "Create campaigns and product stories.",
      headline: "Production infrastructure without the agency markup.",
      description: "Scale internal content creation, shoot CEO keynotes, customer case studies, and brand campaigns in a controlled, confidential, premium environment.",
      keyCapabilities: [
        "Enterprise-level NDAs and secure isolated storage",
        "Full production crew booking on demand",
        "Direct collaboration with vetted creator talent",
        "Executive hospitality and private conference suites"
      ]
    },
    {
      id: "startups",
      label: "STARTUPS",
      tagline: "Build content without building an internal studio.",
      headline: "Punch above your weight with studio-grade content.",
      description: "Building an internal studio costs millions and sits idle 80% of the month. Creator House provides flexible membership so your marketing team can ship world-class launches on demand.",
      keyCapabilities: [
        "Demo day video recordings with zero equipment purchase",
        "Product launch walkthroughs with motorized turntable rigs",
        "Flexible membership shared across your marketing team",
        "Venture ecosystem proximity to investors and partners"
      ]
    }
  ],

  membershipBenefits: [
    {
      title: "2 Full Studio Sessions / Month",
      description: "Guaranteed priority booking in Studio A, Studio B, or Reels Lab with full lighting and camera rigs included."
    },
    {
      title: "Broadcast Podcast Suite Access",
      description: "Acoustically isolated multi-cam podcast recording with Shure broadcast mics and 4K ISO switching."
    },
    {
      title: "Pro Gear Locker Privileges",
      description: "Access to Sony FX cinema cameras, GM primes, wireless mics, Aputure lighting, and motorized sliders at no extra fee."
    },
    {
      title: "10Gbps Symmetrical Ingest Station",
      description: "Offload 200GB camera cards in under 3 minutes directly to high-speed cloud or your portable SSDs."
    },
    {
      title: "Calibrated Edit Suite Access",
      description: "Book time in our soundproof color grading and mastering suite with dual Apple Pro Display XDRs."
    },
    {
      title: "Creator House Member Community",
      description: "Exclusive access to weekly creator roundtables, masterclasses, rough-cut feedback screenings, and brand matchmaking."
    },
    {
      title: "Dedicated On-Site Tech Support",
      description: "An experienced studio technician on site to assist with lighting setup, audio monitoring, and memory management."
    },
    {
      title: "Guest & Crew Access",
      description: "Bring up to 3 crew members or co-creators per session at no additional charge."
    }
  ],

  communityMoments: [
    {
      badge: "SHOOT DAYS",
      title: "Collaborative Multi-Creator Sets",
      description: "Behind-the-scenes magic where creators trade camera skills, test lighting techniques, and co-direct ambitious projects."
    },
    {
      badge: "ROUGH-CUT NIGHTS",
      title: "Friday Feedback Screenings",
      description: "Screen your work-in-progress on the 120-inch theater screen and get candid retention insights before pressing publish."
    },
    {
      badge: "BRAND MIXERS",
      title: "Direct Access to Venture Brands",
      description: "Curated networking dinners connecting Creator House residents with marketing heads from SZ Ventures portfolio companies."
    },
    {
      badge: "MASTERCLASSES",
      title: "Cine-Lighting & Audio Engineering",
      description: "Deep dive technical workshops led by veteran cinematographers, colorists, and viral story architects."
    }
  ],

  socialProofStats: [
    { number: "500+", label: "STUDIO HOURS", detail: "Logged in high-fidelity production" },
    { number: "10Gbps", label: "INGEST SPEED", detail: "Zero-wait local offload infrastructure" },
    { number: "4K / 6K", label: "CINE CAPTURE", detail: "Timecode-synced multi-angle recording" },
    { number: "0 MIN", label: "SETUP FRICTION", detail: "Pre-lit, sound-checked, ready on arrival" }
  ],

  testimonials: [
    {
      quote: "Creator House solves the biggest bottleneck in content: the endless friction of setting up, lighting, and tearing down equipment in a cramped room. You walk in, hit record, and walk away with footage that looks like an A24 production.",
      author: "Resident Filmmaker & Digital Storyteller",
      role: "YouTube / 450K+ Subscribers"
    },
    {
      quote: "The acoustic isolation and pre-lit setups in The Pod cut our podcast recording turnaround from four hours to forty-five minutes. Our guests are consistently blown away by the room.",
      author: "Host & Producer",
      role: "Tech & Venture Dialogue Series"
    }
  ]
};
