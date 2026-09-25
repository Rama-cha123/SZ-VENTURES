/**
 * CREATOR HOUSE — CENTRALIZED ROUTE & ACTION MAP
 * Single source of truth for all links, navigation items, CTA targets, and external endpoints.
 * Conforms strictly to Sections 26-48 of Creator House specifications.
 * Zero dead links, zero placeholder anchors.
 */

(function () {
  'use strict';

  // 1. Core Internal Route Map
  const routes = {
    home: "/",
    spaces: "/creator-house/#spaces",
    membership: "/creator-house/#membership",
    howItWorks: "/creator-house/#journey",
    whyCreatorHouse: "/creator-house/#why",
    creators: "/creator-house/#creators",
    statement: "/creator-house/#statementMoment",
    contact: "/contact.html",
    about: "/about/",
    creatorHouse: "/creator-house/",
    ventures: "/ventures/",
    capabilities: "/capabilities.html",
    projects: "/insights.html",
    privacy: "/privacy.html",
    terms: "/terms.html",
    notFound: "/creator-house/404.html"
  };

  // 2. Portfolio Ventures Map
  const ventures = {
    snapops: "/ventures/snapops/",
    creatorHouse: "/creator-house/",
    bowlAndSip: "/ventures/bowl-and-sip/",
    mirai: "/ventures/mirai-engineering/",
    manufacturing: "/ventures/manufacturing/"
  };

  // 3. Central Action Map for CTAs
  const actions = {
    earlyAccess: "/creator-house/#membership",
    exploreSpace: "/creator-house/#spaces",
    joinCreatorHouse: "/creator-house/#membership",
    exploreMembership: "/creator-house/#membership",
    howItWorks: "/creator-house/#journey",
    contact: "/contact.html"
  };

  // 4. Centralized Navigation Items (consumed by Navbar and Footer)
  const navigation = [
    { id: "nav-ventures", label: "Ventures", href: "/ventures/", external: false },
    { id: "nav-creator-house", label: "Creator House", href: "/creator-house/", active: true, external: false },
    { id: "nav-spaces", label: "Spaces", href: "#spaces", external: false },
    { id: "nav-membership", label: "Membership", href: "#membership", external: false },
    { id: "nav-how-it-works", label: "How It Works", href: "#journey", external: false },
    { id: "nav-contact", label: "Contact", href: "/contact.html", external: false }
  ];

  // 5. Official Social Media Endpoints
  const socialLinks = {
    instagram: "https://www.instagram.com/szventures",
    youtube: "https://www.youtube.com/@szventures",
    linkedin: "https://www.linkedin.com/company/sz-ventures",
    twitter: "https://x.com/szventures"
  };

  // 6. Space Showcase Anchor & Deep-Link Map
  const spacesMap = {
    "studio-a": {
      id: "studio-a",
      name: "Studio A",
      anchor: "#studio-a",
      category: "Cinematic Long-Form & Commercials",
      featureTarget: "#spaces"
    },
    "the-pod": {
      id: "the-pod",
      name: "The Pod",
      anchor: "#the-pod",
      category: "Broadcast Audio & Visual Dialogues",
      featureTarget: "#spaces"
    },
    "reels-lab": {
      id: "reels-lab",
      name: "Reels Lab",
      anchor: "#reels-lab",
      category: "Short-Form Content & Rapid UGC",
      featureTarget: "#spaces"
    },
    "edit-suite": {
      id: "edit-suite",
      name: "Edit Suite",
      anchor: "#edit-suite",
      category: "Color Grading & Post-Production",
      featureTarget: "#spaces"
    },
    "creator-lounge": {
      id: "creator-lounge",
      name: "Creator Lounge",
      anchor: "#creator-lounge",
      category: "Collaboration & Community",
      featureTarget: "#spaces"
    }
  };

  // 7. Creator Use Case Solutions Map
  const useCasesMap = {
    "filmmakers": { id: "filmmakers", label: "Filmmakers", anchor: "#filmmakers", discipline: "Filmmaking" },
    "podcasters": { id: "podcasters", label: "Podcasters", anchor: "#podcasters", discipline: "Podcasting" },
    "influencers": { id: "influencers", label: "Influencers", anchor: "#influencers", discipline: "Short-Form Content" },
    "ugc": { id: "ugc", label: "UGC Creators", anchor: "#ugc", discipline: "UGC Commercials" },
    "brands": { id: "brands", label: "Brands", anchor: "#brands", discipline: "Brand Content" },
    "startups": { id: "startups", label: "Startups", anchor: "#startups", discipline: "Startup Storytelling" }
  };

  // 8. Sticky Header Height Offset (px) for Same-Page Smooth Scrolling
  const NAVBAR_HEIGHT_OFFSET = 76;

  // 9. Smooth Scroll Helper with Offset & History PushState
  function smoothScrollToTarget(targetSelector, updateHash = true) {
    if (!targetSelector) return;
    const cleanId = targetSelector.startsWith('#') ? targetSelector.slice(1) : targetSelector;
    const element = document.getElementById(cleanId);
    
    if (element) {
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - NAVBAR_HEIGHT_OFFSET;

      window.scrollTo({
        top: Math.max(0, offsetPosition),
        behavior: 'smooth'
      });

      if (updateHash && window.history && window.history.pushState) {
        window.history.pushState(null, '', `#${cleanId}`);
      }
      return true;
    }
    return false;
  }

  // 10. Form Submission Storage & Integration Point
  function recordMembershipApplication(formData) {
    const record = {
      ...formData,
      refId: `CH-${Date.now().toString().slice(-6)}`,
      submittedAt: new Date().toISOString()
    };

    try {
      const existing = JSON.parse(localStorage.getItem('ch_applications') || '[]');
      existing.unshift(record);
      localStorage.setItem('ch_applications', JSON.stringify(existing));
      console.info('[Creator House] Application logged:', record);
    } catch (e) {
      console.warn('[Creator House] LocalStorage unavailable:', e);
    }

    // Structured hook for future backend / webhook integration
    if (typeof window.onCreatorHouseFormSubmit === 'function') {
      window.onCreatorHouseFormSubmit(record);
    }

    return record;
  }

  // Export globally
  window.CREATOR_HOUSE_CONFIG = {
    routes,
    ventures,
    actions,
    navigation,
    socialLinks,
    spacesMap,
    useCasesMap,
    NAVBAR_HEIGHT_OFFSET,
    smoothScrollToTarget,
    recordMembershipApplication
  };

})();
