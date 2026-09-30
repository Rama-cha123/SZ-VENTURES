const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  try {
    const browser = await puppeteer.launch({
      executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 900 });

    const consoleLogs = [];
    const failedRequests = [];

    page.on('console', msg => {
      consoleLogs.push({ type: msg.type(), text: msg.text() });
    });

    page.on('requestfailed', request => {
      failedRequests.push({
        url: request.url(),
        failure: request.failure() ? request.failure().errorText : 'unknown'
      });
    });

    const response = await page.goto('http://127.0.0.1:3000/ventures/', {
      waitUntil: 'networkidle2',
      timeout: 10000
    });

    console.log('HTTP Status:', response.status());

    // Check stylesheets
    const stylesheets = await page.evaluate(() => {
      return Array.from(document.styleSheets).map(s => {
        try {
          return {
            href: s.href,
            rulesCount: s.cssRules ? s.cssRules.length : 0,
            disabled: s.disabled
          };
        } catch (e) {
          return { href: s.href, error: e.message };
        }
      });
    });

    // Check computed styles on key elements
    const elementStyles = await page.evaluate(() => {
      const nav = document.querySelector('.nav');
      const navLogoImg = document.querySelector('.nav-logo-img');
      const hero = document.querySelector('.hero');
      const heroTitle = document.querySelector('.hero__title');
      const menu = document.querySelector('.menu');
      const portfolioList = document.querySelector('.portfolio__list');
      const company = document.querySelector('.company');
      const footer = document.querySelector('.footer-v2');

      const getDetails = (el, name) => {
        if (!el) return { name, exists: false };
        const cs = window.getComputedStyle(el);
        return {
          name,
          exists: true,
          display: cs.display,
          position: cs.position,
          width: cs.width,
          height: cs.height,
          maxWidth: cs.maxWidth,
          gridTemplateColumns: cs.gridTemplateColumns,
          visibility: cs.visibility,
          opacity: cs.opacity,
          color: cs.color,
          fontSize: cs.fontSize
        };
      };

      return {
        nav: getDetails(nav, 'nav'),
        navLogoImg: getDetails(navLogoImg, 'navLogoImg'),
        hero: getDetails(hero, 'hero'),
        heroTitle: getDetails(heroTitle, 'heroTitle'),
        menu: getDetails(menu, 'menu'),
        portfolioList: getDetails(portfolioList, 'portfolioList'),
        company: getDetails(company, 'company'),
        footer: getDetails(footer, 'footer')
      };
    });

    // Save screenshot
    await page.screenshot({ path: 'scripts/debug_screenshot.png', fullPage: true });

    console.log('--- CONSOLE LOGS ---');
    console.log(JSON.stringify(consoleLogs, null, 2));
    console.log('--- FAILED REQUESTS ---');
    console.log(JSON.stringify(failedRequests, null, 2));
    console.log('--- STYLESHEETS ---');
    console.log(JSON.stringify(stylesheets, null, 2));
    console.log('--- ELEMENT STYLES ---');
    console.log(JSON.stringify(elementStyles, null, 2));

    await browser.close();
  } catch (err) {
    console.error('Puppeteer script error:', err);
    process.exit(1);
  }
})();
