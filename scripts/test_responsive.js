const puppeteer = require('puppeteer');

const viewports = [
  { name: 'Mobile 320x640', width: 320, height: 640 },
  { name: 'Mobile 375x812', width: 375, height: 812 },
  { name: 'Mobile 390x844', width: 390, height: 844 },
  { name: 'Mobile 430x932', width: 430, height: 932 },
  { name: 'Tablet 768x1024', width: 768, height: 1024 },
  { name: 'Tablet 1024x768', width: 1024, height: 768 },
  { name: 'Desktop 1280x720', width: 1280, height: 720 },
  { name: 'Desktop 1440x900', width: 1440, height: 900 },
  { name: 'Desktop 1920x1080', width: 1920, height: 1080 },
];

const routes = [
  '/',
  '/ventures/',
  '/operations/',
  '/about/',
  '/contact.html',
  '/ventures/snapops/',
  '/ventures/bowl-and-sip/',
  '/ventures/creator-house/',
  '/ventures/mirai-engineering/',
  '/ventures/manufacturing/'
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  let totalIssues = 0;

  for (const route of routes) {
    console.log(`\n=================== Testing Route: ${route} ===================`);
    
    // Catch console errors
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    for (const vp of viewports) {
      await page.setViewport({ width: vp.width, height: vp.height });
      try {
        await page.goto(`http://127.0.0.1:3000${route}`, { waitUntil: 'domcontentloaded', timeout: 8000 });
        
        // Wait a tick for layouts
        await new Promise(r => setTimeout(r, 100));

        const metrics = await page.evaluate((vpWidth) => {
          const docWidth = document.documentElement.scrollWidth;
          const hasHScroll = docWidth > vpWidth + 1; // 1px tolerance for subpixel
          
          // Check logo dimensions
          const logo = document.querySelector('.nav-logo-img, .nav__brand img');
          let logoW = 0, logoH = 0;
          if (logo) {
            const rect = logo.getBoundingClientRect();
            logoW = Math.round(rect.width);
            logoH = Math.round(rect.height);
          }

          // Check menu is hidden
          const menu = document.querySelector('.menu');
          let menuVisible = false;
          if (menu) {
            const cs = window.getComputedStyle(menu);
            menuVisible = (cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0');
          }

          return { docWidth, hasHScroll, logoW, logoH, menuVisible };
        }, vp.width);

        const status = (!metrics.hasHScroll && (metrics.logoW <= 48) && !metrics.menuVisible) ? 'PASS' : 'WARN';
        if (status === 'WARN') {
          totalIssues++;
          console.log(`  [${status}] ${vp.name}: HScroll=${metrics.hasHScroll} (doc=${metrics.docWidth}px, vp=${vp.width}px), logo=${metrics.logoW}x${metrics.logoH}, menuVisible=${metrics.menuVisible}`);
        } else {
          console.log(`  [PASS] ${vp.name}: OK (logo=${metrics.logoW}x${metrics.logoH}, no hscroll)`);
        }
      } catch (err) {
        console.log(`  [ERR] ${vp.name}: ${err.message}`);
        totalIssues++;
      }
    }

    if (errors.length > 0) {
      console.log(`  Console Errors on ${route}:`, errors);
    }
  }

  await browser.close();
  console.log(`\n=================== Test Finished: ${totalIssues} issues found ===================`);
  process.exit(totalIssues > 0 ? 1 : 0);
})();
