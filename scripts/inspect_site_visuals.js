const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  console.log("Capturing homepage (desktop)...");
  await page.goto('http://127.0.0.1:3000/', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: 'scripts/homepage_desktop.png', fullPage: false });

  console.log("Capturing ventures page (desktop)...");
  await page.goto('http://127.0.0.1:3000/ventures/', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: 'scripts/ventures_desktop.png', fullPage: false });
  await page.screenshot({ path: 'scripts/ventures_full.png', fullPage: true });

  console.log("Capturing homepage (mobile 375x812)...");
  await page.setViewport({ width: 375, height: 812 });
  await page.goto('http://127.0.0.1:3000/', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: 'scripts/homepage_mobile.png', fullPage: false });

  await browser.close();
  console.log("Screenshots saved successfully.");
})().catch(err => {
  console.error(err);
  process.exit(1);
});
