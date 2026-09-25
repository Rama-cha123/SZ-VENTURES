const puppeteer = require('puppeteer');
const path = require('path');

async function captureSections() {
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-animations', '--disable-web-animations']
    });
    const page = await browser.newPage();
    const url = 'http://localhost:3000/creator-house/';
    
    try {
        // Desktop
        await page.setViewport({ width: 1440, height: 900 });
        await page.goto(url, { waitUntil: 'load', timeout: 30000 });
        await new Promise(r => setTimeout(r, 2000)); // wait for renders
        
        // Overflow check
        const overflow = await page.evaluate(() => {
            return document.documentElement.scrollWidth > window.innerWidth;
        });
        console.log(`[Desktop] Horizontal Overflow: ${overflow}`);

        // Header and hero
        const heroEl = await page.$('#hero-section');
        if(heroEl) await heroEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_header_and_hero.png' });

        // Benefits
        const benefitsEl = await page.$('#benefits-section');
        if(benefitsEl) await benefitsEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_benefits.png' });
        
        // Production
        const prodEl = await page.$('#how-it-works');
        if(prodEl) await prodEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_production.png' });

        // Podcast
        const podEl = await page.$('#how-it-works + section');
        if(podEl) await podEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_podcast.png' });

        // Pricing
        const pricingEl = await page.$('#membership');
        if(pricingEl) await pricingEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_desktop_pricing.png' });
        
        // 1280x720 check
        await page.setViewport({ width: 1280, height: 720 });
        const overflow720 = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
        console.log(`[1280x720] Horizontal Overflow: ${overflow720}`);

        // 1024x768 check
        await page.setViewport({ width: 1024, height: 768 });
        const overflow768 = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
        console.log(`[1024x768] Horizontal Overflow: ${overflow768}`);

        // Mobile
        await page.setViewport({ width: 390, height: 844 });
        await new Promise(r => setTimeout(r, 1000));
        const overflowMob = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
        console.log(`[Mobile] Horizontal Overflow: ${overflowMob}`);

        // Mobile hero
        const mobHeroEl = await page.$('#hero-section');
        if(mobHeroEl) await mobHeroEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_mobile_hero.png' });
        
        // Mobile pricing
        const mobPricingEl = await page.$('#membership');
        if(mobPricingEl) await mobPricingEl.screenshot({ path: 'C:\\Users\\abdul\\.gemini\\antigravity\\brain\\12307cf0-1dd1-4e13-aaef-0b5ab42d8a44\\screenshot_mobile_pricing.png' });

    } catch (e) {
        console.error(e);
    } finally {
        await browser.close();
    }
}

captureSections();
