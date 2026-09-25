const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function checkOverflowAndScreenshot(page, url, name, width, height) {
    try {
        await page.setViewport({ width, height });
        await page.goto(url, { waitUntil: 'load', timeout: 30000 });
        
        // Let animations settle
        await new Promise(r => setTimeout(r, 2000));
        
        const overflow = await page.evaluate(() => {
            return document.documentElement.scrollWidth > window.innerWidth;
        });
        console.log(`[${name} @ ${width}x${height}] Horizontal Overflow: ${overflow}`);
        
        const outPath = path.join('C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44', `screenshot_${name}_${width}x${height}.png`);
        await page.screenshot({ path: outPath, fullPage: true });
        console.log(`Saved screenshot to ${outPath}`);
    } catch(e) {
        console.error("Error capturing", name, width, height, e);
    }
}

(async () => {
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-animations', '--disable-web-animations']
    });
    const page = await browser.newPage();
    
    // Creator House
    const chUrl = 'http://localhost:3000/creator-house/';
    await checkOverflowAndScreenshot(page, chUrl, 'creator_house', 1440, 900);
    await checkOverflowAndScreenshot(page, chUrl, 'creator_house', 1024, 768);
    await checkOverflowAndScreenshot(page, chUrl, 'creator_house', 390, 844);
    
    // SnapOps
    const snapUrl = 'http://localhost:3000/snapops/';
    await checkOverflowAndScreenshot(page, snapUrl, 'snapops', 1440, 900);
    await checkOverflowAndScreenshot(page, snapUrl, 'snapops', 1024, 768);
    await checkOverflowAndScreenshot(page, snapUrl, 'snapops', 390, 844);
    
    // About page founder section
    try {
        await page.setViewport({ width: 1440, height: 900 });
        await page.goto('http://localhost:3000/about/', { waitUntil: 'load', timeout: 30000 });
        await new Promise(r => setTimeout(r, 2000));
        const aboutPath = path.join('C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44', `screenshot_about_founder.png`);
        await page.screenshot({ path: aboutPath, fullPage: true });
        console.log(`Saved screenshot to ${aboutPath}`);
    } catch (e) {
        console.error("Error capturing about", e);
    }

    await browser.close();
})();
