const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACT_DIR = 'C:\\Users\\bheem\\.gemini\\antigravity-ide\\brain\\e5806df9-334a-4a70-b13b-20f67836360f';
const PORT = 9224;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 1;
    this.callbacks = new Map();
  }

  async init() {
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
    });

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.callbacks.has(msg.id)) {
        const { resolve, reject } = this.callbacks.get(msg.id);
        this.callbacks.delete(msg.id);
        if (msg.error) reject(msg.error);
        else resolve(msg.result);
      }
    };
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.ws.close();
  }
}

async function run() {
  const tmpDir = path.join(process.cwd(), 'tmp_chrome_profile_verify');
  if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

  const chromeProc = spawn(CHROME_PATH, [
    '--headless=new',
    '--disable-gpu',
    `--remote-debugging-port=${PORT}`,
    '--remote-allow-origins=*',
    `--user-data-dir=${tmpDir}`,
    '--no-first-run',
    '--no-default-browser-check'
  ]);

  let targets = null;
  for (let i = 0; i < 20; i++) {
    await sleep(500);
    try {
      targets = await getJson(`http://127.0.0.1:${PORT}/json`);
      if (targets && targets.length > 0) break;
    } catch (e) {}
  }
  if (!targets) throw new Error('Failed to connect to Chrome CDP');

  const pageTarget = targets.find(t => t.type === 'page') || targets[0];
  const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
  await client.init();

  await client.send('Page.enable');
  await client.send('DOM.enable');
  await client.send('Runtime.enable');

  // Disable cache in Chrome network domain
  await client.send('Network.enable');
  await client.send('Network.setCacheDisabled', { cacheDisabled: true });

  const viewports = [
    { name: 'desktop', width: 1440, height: 1100, isMobile: false },
    { name: 'tablet', width: 880, height: 1100, isMobile: false },
    { name: 'mobile', width: 390, height: 844, isMobile: true }
  ];

  const overallResults = {};

  for (const vp of viewports) {
    console.log(`\n=================== Testing Viewport: ${vp.name} (${vp.width}x${vp.height}) ===================`);
    await client.send('Emulation.setDeviceMetricsOverride', {
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: 1,
      mobile: vp.isMobile
    });

    await client.send('Page.navigate', { url: 'http://localhost:3000/' });
    await sleep(2500);

    const evalRes = await client.send('Runtime.evaluate', {
      expression: `(() => {
        // Remove preloader so it never interferes with visuals
        const pre = document.getElementById('preloader');
        if (pre) pre.remove();
        document.body.classList.remove('is-loading');

        // Reveal AOS
        document.querySelectorAll('[data-aos]').forEach(el => {
          el.classList.add('aos-animate');
          el.style.opacity = '1';
          el.style.transform = 'none';
        });

        const cards = Array.from(document.querySelectorAll('.portfolio__list > .company'));
        const cardData = cards.map((card, idx) => {
          const computed = window.getComputedStyle(card);
          const cardRect = card.getBoundingClientRect();

          const nameCol = card.querySelector('.company__name')?.parentElement;
          const thesisCol = card.querySelector('.company__thesis');
          const sectorCol = card.querySelector('.company__sector');
          const metricCol = card.querySelector('.company__metric');
          const ctaCol = card.querySelector('.company__cta');
          const svgEl = ctaCol ? ctaCol.querySelector('svg') : null;

          const nR = nameCol ? nameCol.getBoundingClientRect() : null;
          const tR = thesisCol ? thesisCol.getBoundingClientRect() : null;
          const sR = sectorCol ? sectorCol.getBoundingClientRect() : null;
          const mR = metricCol ? metricCol.getBoundingClientRect() : null;
          const cR = ctaCol ? ctaCol.getBoundingClientRect() : null;
          const svgR = svgEl ? svgEl.getBoundingClientRect() : null;

          return {
            idx: idx + 1,
            name: card.querySelector('.company__name')?.textContent.trim(),
            display: computed.display,
            gridTemplateColumns: computed.gridTemplateColumns,
            cardRect: { left: Math.round(cardRect.left), right: Math.round(cardRect.right), width: Math.round(cardRect.width) },
            col1_name: nR ? { left: Math.round(nR.left), right: Math.round(nR.right), width: Math.round(nR.width) } : null,
            col2_thesis: tR ? { left: Math.round(tR.left), right: Math.round(tR.right), width: Math.round(tR.width) } : null,
            col3_sector: sR ? { left: Math.round(sR.left), right: Math.round(sR.right), width: Math.round(sR.width) } : null,
            col4_metric: mR ? { left: Math.round(mR.left), right: Math.round(mR.right), width: Math.round(mR.width) } : null,
            col5_cta: cR ? { left: Math.round(cR.left), right: Math.round(cR.right), width: Math.round(cR.width) } : null,
            svgArrow: svgR ? { left: Math.round(svgR.left), right: Math.round(svgR.right), width: Math.round(svgR.width), visible: svgR.width > 0 && svgR.right <= Math.round(cardRect.right) } : null
          };
        });

        const list = document.querySelector('.portfolio__list');
        if (list) {
          list.scrollIntoView({ behavior: 'instant', block: 'start' });
        }

        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        const hasHorizontalOverflow = scrollWidth > clientWidth;

        return {
          viewport: '${vp.name}',
          hasHorizontalOverflow,
          scrollWidth,
          clientWidth,
          cards: cardData
        };
      })()`,
      returnByValue: true
    });

    const data = evalRes.result.value;
    overallResults[vp.name] = data;

    console.log(`Results for ${vp.name}:`);
    data.cards.forEach(c => {
      console.log(`[Card ${c.idx}] ${c.name}:`);
      console.log(`   Col 1 Name Left: ${c.col1_name?.left}, Col 2 Thesis Left: ${c.col2_thesis?.left}, Col 3 Sector Left: ${c.col3_sector?.left}, Col 4 Metric Left: ${c.col4_metric?.left}, Col 5 CTA Right: ${c.col5_cta?.right}`);
      console.log(`   Arrow Visible: ${c.svgArrow?.visible} (arrow right: ${c.svgArrow?.right}, card right: ${c.cardRect.right})`);
    });

    await sleep(600);
    const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
    const imgBuffer = Buffer.from(screenshot.data, 'base64');
    const screenshotPath = path.join(ARTIFACT_DIR, `ventures_${vp.name}.png`);
    fs.writeFileSync(screenshotPath, imgBuffer);
    console.log(`Saved screenshot to: ${screenshotPath}`);

    if (vp.name === 'mobile') {
      await client.send('Runtime.evaluate', {
        expression: `(() => {
          const cards = document.querySelectorAll('.portfolio__list > .company');
          if (cards[3]) cards[3].scrollIntoView({ behavior: 'instant', block: 'start' });
        })()`
      });
      await sleep(500);
      const lowerScreenshot = await client.send('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(ARTIFACT_DIR, 'ventures_mobile_lower.png'), Buffer.from(lowerScreenshot.data, 'base64'));
      console.log('Saved ventures_mobile_lower.png');
    }
  }

  // Also check /ventures/ canonical route
  console.log(`\n=================== Testing Canonical Route: /ventures/ ===================`);
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 1100,
    deviceScaleFactor: 1,
    mobile: false
  });
  await client.send('Page.navigate', { url: 'http://localhost:3000/ventures/' });
  await sleep(2500);
  const venturesEval = await client.send('Runtime.evaluate', {
    expression: `(() => {
      const pre = document.getElementById('preloader');
      if (pre) pre.remove();
      document.body.classList.remove('is-loading');
      document.querySelectorAll('[data-aos]').forEach(el => {
        el.classList.add('aos-animate');
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      const cards = Array.from(document.querySelectorAll('.portfolio__list > .company'));
      return cards.map((c, i) => ({
        idx: i + 1,
        name: c.querySelector('.company__name')?.textContent.trim(),
        status: c.querySelector('.status-badge')?.textContent.trim(),
        nameLeft: Math.round(c.querySelector('.company__name')?.parentElement.getBoundingClientRect().left),
        thesisLeft: Math.round(c.querySelector('.company__thesis')?.getBoundingClientRect().left),
        sectorLeft: Math.round(c.querySelector('.company__sector')?.getBoundingClientRect().left),
        metricLeft: Math.round(c.querySelector('.company__metric')?.getBoundingClientRect().left),
        ctaRight: Math.round(c.querySelector('.company__cta')?.getBoundingClientRect().right)
      }));
    })()`,
    returnByValue: true
  });
  console.log('Ventures Page Cards:', JSON.stringify(venturesEval.result.value, null, 2));

  const venturesShot = await client.send('Page.captureScreenshot', { format: 'png' });
  const vBuffer = Buffer.from(venturesShot.data, 'base64');
  const vPath = path.join(ARTIFACT_DIR, 'ventures_canonical_desktop.png');
  fs.writeFileSync(vPath, vBuffer);
  console.log(`Saved screenshot to: ${vPath}`);

  client.close();
  chromeProc.kill();
  console.log('\nVerification script completed successfully.');
  process.exit(0);
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
