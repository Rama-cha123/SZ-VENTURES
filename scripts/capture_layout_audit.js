const puppeteer = require('puppeteer-core');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const outDir = path.resolve(__dirname, '..');

async function run() {
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // 1. Homepage Desktop Viewport (1440x900)
    await page.setViewport({ width: 1440, height: 900 });
    await page.goto('http://localhost:3000/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 1500)); // allow AOS failsafe to settle

    // Hero audit
    const heroInfo = await page.evaluate(() => {
      const hero = document.querySelector('.hero');
      const title = document.querySelector('.hero__title');
      const sub = document.querySelector('.hero__sub');
      const actions = document.querySelector('.hero__actions');
      const btns = actions ? Array.from(actions.querySelectorAll('a')).map(a => a.textContent.trim()) : [];
      const titleStyle = title ? window.getComputedStyle(title) : null;
      const subStyle = sub ? window.getComputedStyle(sub) : null;

      const titleRect = title ? title.getBoundingClientRect() : null;
      const actionsRect = actions ? actions.getBoundingClientRect() : null;

      return {
        titleFontSize: titleStyle ? titleStyle.fontSize : null,
        titleLineHeight: titleStyle ? titleStyle.lineHeight : null,
        subFontSize: subStyle ? subStyle.fontSize : null,
        titleBottom: titleRect ? titleRect.bottom : null,
        actionsBottom: actionsRect ? actionsRect.bottom : null,
        actionsVisibleIn900h: actionsRect ? actionsRect.bottom <= 900 : false,
        buttons: btns
      };
    });

    console.log('Homepage Hero Audit:', JSON.stringify(heroInfo, null, 2));

    await page.screenshot({ path: path.join(outDir, 'audit_homepage_desktop_fold.png') });

    // Scroll down to trigger any animations smoothly and screenshot full page
    await page.evaluate(async () => {
      window.scrollTo(0, document.body.scrollHeight / 2);
      await new Promise(r => setTimeout(r, 600));
      window.scrollTo(0, document.body.scrollHeight);
      await new Promise(r => setTimeout(r, 600));
      window.scrollTo(0, 0);
      await new Promise(r => setTimeout(r, 400));
    });

    await page.screenshot({ path: path.join(outDir, 'audit_homepage_desktop_full.png'), fullPage: true });

    // 2. Ventures page audit
    await page.goto('http://localhost:3000/ventures/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 1500));

    const venturesInfo = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('.company, .venture-card'));
      return cards.map((c, i) => {
        const nameEl = c.querySelector('.company__name, h3');
        const style = window.getComputedStyle(c);
        const rect = c.getBoundingClientRect();
        return {
          index: i,
          name: nameEl ? nameEl.textContent.trim() : 'Unknown',
          display: style.display,
          visibility: style.visibility,
          opacity: style.opacity,
          top: Math.round(rect.top + window.scrollY),
          left: Math.round(rect.left),
          width: Math.round(rect.width),
          height: Math.round(rect.height)
        };
      });
    });

    console.log('Ventures Cards Audit (count=' + venturesInfo.length + '):', JSON.stringify(venturesInfo, null, 2));

    await page.screenshot({ path: path.join(outDir, 'audit_ventures_desktop_full.png'), fullPage: true });

    // 3. Operations page audit
    await page.goto('http://localhost:3000/operations/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 1500));

    const opsInfo = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('.ops-card'));
      return cards.map((c, i) => {
        const titleEl = c.querySelector('.ops-card__title');
        const style = window.getComputedStyle(c);
        const rect = c.getBoundingClientRect();
        return {
          index: i,
          title: titleEl ? titleEl.textContent.trim() : 'Unknown',
          opacity: style.opacity,
          top: Math.round(rect.top + window.scrollY),
          left: Math.round(rect.left),
          width: Math.round(rect.width),
          height: Math.round(rect.height)
        };
      });
    });

    console.log('Operations Cards Audit (count=' + opsInfo.length + '):', JSON.stringify(opsInfo, null, 2));

    await page.screenshot({ path: path.join(outDir, 'audit_operations_desktop_full.png'), fullPage: true });

    // 4. Mobile Viewport (375x812)
    await page.setViewport({ width: 375, height: 812, isMobile: true });
    await page.goto('http://localhost:3000/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({ path: path.join(outDir, 'audit_homepage_mobile_fold.png') });

    await page.goto('http://localhost:3000/ventures/', { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({ path: path.join(outDir, 'audit_ventures_mobile_fold.png') });

    console.log('ALL SCREENSHOTS CAPTURED SUCCESSFULLY!');
  } finally {
    await browser.close();
  }
}

run().catch(err => {
  console.error('Audit Error:', err);
  process.exit(1);
});
