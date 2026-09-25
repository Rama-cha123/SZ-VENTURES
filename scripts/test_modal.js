const puppeteer = require('puppeteer');
const path = require('path');

async function testFormFlow() {
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-animations', '--disable-web-animations']
    });
    const page = await browser.newPage();
    const url = 'http://localhost:3000/creator-house/';
    
    try {
        await page.goto(url, { waitUntil: 'load', timeout: 30000 });
        
        // 1. Click modal trigger
        const triggers = await page.$$('.ch-modal-trigger');
        console.log(`Found ${triggers.length} triggers`);
        
        // Click the first one (Header)
        await triggers[0].click();
        await new Promise(r => setTimeout(r, 500));
        
        // Modal is visible?
        const isVisible = await page.$eval('#ch-modal', el => !el.classList.contains('hidden'));
        console.log(`Modal visible: ${isVisible}`);
        
        // Title Check
        const title = await page.$eval('#ch-modal-title', el => el.textContent);
        console.log(`Modal Title: ${title}`);
        
        // Test escape key
        await page.keyboard.press('Escape');
        await new Promise(r => setTimeout(r, 500));
        const isHidden = await page.$eval('#ch-modal', el => el.classList.contains('hidden'));
        console.log(`Escape closed modal: ${isHidden}`);
        
        // Open again via pricing trigger
        const pricingTrigger = triggers[triggers.length - 1]; // last one
        await pricingTrigger.click();
        await new Promise(r => setTimeout(r, 500));
        
        const title2 = await page.$eval('#ch-modal-title', el => el.textContent);
        console.log(`Second Modal Title: ${title2}`);
        
        // Take a screenshot of the modal (Desktop)
        await page.setViewport({ width: 1440, height: 900 });
        await page.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_modal.png' });
        
        // Mobile screenshot
        await page.setViewport({ width: 390, height: 844 });
        await page.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_mobile_modal.png' });
        
        // Intercept network requests to /api/submit
        let submitStatus = null;
        page.on('response', response => {
            if (response.url().includes('/api/submit')) {
                submitStatus = response.status();
            }
        });
        
        // Fill form
        await page.type('#ch_name', 'Test User');
        await page.type('#ch_email', 'test@example.com');
        await page.type('#ch_phone', '1234567890');
        await page.type('#ch_city', 'Test City');
        await page.select('#ch_category', 'ugc');
        await page.type('#ch_link', 'https://example.com');
        await page.type('#ch_message', 'This is a test');
        await page.click('#ch_consent');
        
        // Submit
        await page.click('#ch_submit_btn');
        console.log('Form submitted');
        
        await new Promise(r => setTimeout(r, 2000));
        
        console.log(`Submit API status: ${submitStatus}`);
        
        const msg = await page.$eval('#ch_form_msg', el => el.textContent);
        console.log(`Form msg: ${msg}`);

    } catch (e) {
        console.error(e);
    } finally {
        await browser.close();
    }
}

testFormFlow();
