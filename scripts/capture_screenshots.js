const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACT_DIR = 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44';
const PORT = 9222;

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

async function main() {
  const tmpDir = path.join(process.cwd(), 'tmp_chrome_profile');
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

  console.log('Chrome process spawned, waiting for CDP...');
  let targets = null;
  for (let i = 0; i < 20; i++) {
    await sleep(500);
    try {
      targets = await getJson(`http://127.0.0.1:${PORT}/json`);
      if (targets && targets.length > 0) break;
    } catch (e) {}
  }
  if (!targets) throw new Error('Failed to connect to Chrome CDP endpoint after retries');

  const pageTarget = targets.find(t => t.type === 'page') || targets[0];
  console.log('Connected to target:', pageTarget.webSocketDebuggerUrl);

  const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
  await client.init();

  await client.send('Page.enable');
  await client.send('DOM.enable');
  await client.send('Runtime.enable');

  const viewports = [
    { name: 'desktop_1440x900', width: 1440, height: 900, deviceScaleFactor: 1 },
    { name: 'tablet_1024x768', width: 1024, height: 768, deviceScaleFactor: 1 },
    { name: 'mobile_390x844', width: 390, height: 844, deviceScaleFactor: 2, isMobile: true }
  ];

  const results = [];

  for (const vp of viewports) {
    console.log(`\n=== Testing Viewport: ${vp.name} (${vp.width}x${vp.height}) ===`);
    await client.send('Emulation.setDeviceMetricsOverride', {
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: vp.deviceScaleFactor,
      mobile: !!vp.isMobile
    });

    await client.send('Page.navigate', { url: 'http://localhost:3000/' });
    await sleep(2000);

    // Reveal all AOS elements and scroll directly to Creator House & SnapOps
    const evalRes = await client.send('Runtime.evaluate', {
      expression: `(() => {
        // Trigger AOS animation instantly
        document.querySelectorAll('[data-aos]').forEach(el => {
          el.classList.add('aos-animate');
          el.style.opacity = '1';
          el.style.transform = 'none';
        });

        const snapCard = document.querySelector('a[href="/snapops/"].company');
        const chCard = document.querySelector('a[href="/creator-house/"].company');
        const header = document.querySelector('header');
        const list = document.querySelector('.portfolio__list');

        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        const hasHorizontalOverflow = scrollWidth > clientWidth;

        // Scroll so Creator House and SnapOps are visible
        if (chCard) {
          const topPos = chCard.getBoundingClientRect().top + window.pageYOffset - 120;
          if (window.lenis) {
            window.lenis.scrollTo(topPos, { immediate: true });
          } else {
            window.scrollTo(0, topPos);
          }
        }

        let snapRect = null;
        let chRect = null;
        let headerRect = null;

        if (snapCard) {
          const r = snapCard.getBoundingClientRect();
          snapRect = { top: r.top, left: r.left, width: r.width, height: r.height };
        }
        if (chCard) {
          const r = chCard.getBoundingClientRect();
          chRect = { top: r.top, left: r.left, width: r.width, height: r.height };
        }
        if (header) {
          const r = header.getBoundingClientRect();
          headerRect = { top: r.top, left: r.left, width: r.width, height: r.height };
        }

        const isSnapChildOfList = snapCard ? list.contains(snapCard) : false;
        const isSnapInHeader = snapCard ? header.contains(snapCard) : false;
        const snapFollowsCh = (snapCard && chCard) ? (chCard.nextElementSibling === snapCard) : false;

        return {
          hasSnapCard: !!snapCard,
          hasChCard: !!chCard,
          isSnapChildOfList,
          isSnapInHeader,
          snapFollowsCh,
          hasHorizontalOverflow,
          scrollWidth,
          clientWidth,
          snapRect,
          chRect,
          headerRect
        };
      })()`,
      returnByValue: true
    });

    const info = evalRes.result.value;
    console.log('Layout Evaluation:', JSON.stringify(info, null, 2));

    await sleep(500);

    // Capture screenshot
    const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
    const imgBuffer = Buffer.from(screenshot.data, 'base64');

    const filename = `screenshot_homepage_${vp.name}.png`;
    const localPath = path.join(process.cwd(), filename);
    const artifactPath = path.join(ARTIFACT_DIR, filename);

    fs.writeFileSync(localPath, imgBuffer);
    fs.writeFileSync(artifactPath, imgBuffer);
    console.log(`Saved screenshot to ${localPath} and ${artifactPath}`);

    results.push({
      viewport: vp.name,
      ...info,
      screenshot: filename
    });
  }

  // Also test other pages: /ventures/, /portfolio, /new-economy, /new-economy/
  const otherPages = [
    { url: 'http://localhost:3000/ventures/', name: 'ventures' },
    { url: 'http://localhost:3000/portfolio', name: 'portfolio' },
    { url: 'http://localhost:3000/new-economy', name: 'new_economy' },
    { url: 'http://localhost:3000/new-economy/', name: 'new_economy_slash' }
  ];

  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  for (const page of otherPages) {
    console.log(`\n=== Testing Page: ${page.url} ===`);
    await client.send('Page.navigate', { url: page.url });
    await sleep(1500);

    const evalRes = await client.send('Runtime.evaluate', {
      expression: `(() => {
        const snapCard = document.querySelector('a[href="/snapops/"].company') || document.querySelector('a[href="/snapops/"].venture-card');
        const chCard = document.querySelector('a[href="/creator-house/"].company') || document.querySelector('a[href="/creator-house/"].venture-card');
        const header = document.querySelector('header');
        
        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        const hasHorizontalOverflow = scrollWidth > clientWidth;

        const isSnapInHeader = snapCard && header ? header.contains(snapCard) : false;
        const snapFollowsCh = (snapCard && chCard) ? (chCard.nextElementSibling === snapCard) : false;

        if (snapCard) snapCard.scrollIntoView({ block: 'center' });

        return {
          hasSnapCard: !!snapCard,
          hasChCard: !!chCard,
          isSnapInHeader,
          snapFollowsCh,
          hasHorizontalOverflow,
          scrollWidth,
          clientWidth
        };
      })()`,
      returnByValue: true
    });

    const info = evalRes.result.value;
    console.log(`Page ${page.name} Evaluation:`, JSON.stringify(info, null, 2));

    await sleep(500);

    const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
    const imgBuffer = Buffer.from(screenshot.data, 'base64');
    const filename = `screenshot_${page.name}.png`;
    const localPath = path.join(process.cwd(), filename);
    const artifactPath = path.join(ARTIFACT_DIR, filename);

    fs.writeFileSync(localPath, imgBuffer);
    fs.writeFileSync(artifactPath, imgBuffer);
    console.log(`Saved screenshot to ${localPath}`);

    results.push({
      page: page.name,
      ...info,
      screenshot: filename
    });
  }

  client.close();
  chromeProc.kill();
  console.log('\nAll browser tests and screenshots completed successfully!');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
