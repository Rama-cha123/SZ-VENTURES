const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto('http://127.0.0.1:3000/operations/rider-registration', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));

  await page.screenshot({ path: 'scripts/rider_form_step1_desktop.png', fullPage: false });
  console.log("Captured Step 1 desktop screenshot.");

  await page.setViewport({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));

  await page.screenshot({ path: 'scripts/rider_form_step1_mobile.png', fullPage: false });
  console.log("Captured Step 1 mobile screenshot.");

  await browser.close();
})().catch(err => {
  console.error(err);
  process.exit(1);
});
