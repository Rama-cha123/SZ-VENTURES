const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function extractCSS() {
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    const url = 'http://localhost:3000/creator-house/';
    
    try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
        
        // Wait for Tailwind to inject styles
        await page.waitForFunction(() => {
            return Array.from(document.querySelectorAll('style')).some(s => s.textContent.includes('tailwindcss'));
        }, { timeout: 10000 }).catch(() => console.log('Timeout waiting for tailwind identifier, continuing anyway.'));

        // Extract all injected <style> content except our custom :root stuff which we'll keep
        const styles = await page.evaluate(() => {
            const styleNodes = Array.from(document.querySelectorAll('head style'));
            // Filter out our own custom style block (the one with :root variables)
            const tailwindStyles = styleNodes.filter(s => !s.textContent.includes('--ch-bg:'));
            return tailwindStyles.map(s => s.textContent).join('\n');
        });

        if (styles && styles.trim().length > 0) {
            const cssPath = path.join(__dirname, '..', 'assets', 'styles', 'creator-house-tailwind.css');
            fs.writeFileSync(cssPath, styles, 'utf8');
            console.log('Successfully extracted tailwind CSS: ' + cssPath);
            
            // Now rewrite index.html to remove the script and add the stylesheet link
            const htmlPath = path.join(__dirname, '..', 'creator-house', 'index.html');
            let html = fs.readFileSync(htmlPath, 'utf8');
            
            html = html.replace('<script src="https://cdn.tailwindcss.com"></script>', '');
            
            // We'll also replace the inline config since it's no longer needed at runtime
            html = html.replace(/<script>[\s\S]*?tailwind\.config[\s\S]*?<\/script>/m, 
                '<link rel="stylesheet" href="/assets/styles/creator-house-tailwind.css">');
                
            fs.writeFileSync(htmlPath, html, 'utf8');
            console.log('Successfully updated HTML to use local stylesheet.');
        } else {
            console.log('Failed to extract CSS styles.');
        }

    } catch (e) {
        console.error(e);
    } finally {
        await browser.close();
    }
}

extractCSS();
