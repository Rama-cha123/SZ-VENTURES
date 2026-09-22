import os
import re

portfolio_grid = '''          <div class="portfolio-index-grid">
            <a class="venture-card" href="/industrial-technology.html#ai-robotics-data" data-no-swup data-reveal>
              <span class="vc-sector">Industrial Technology</span>
              <h3>AI & Robotics Data</h3>
              <p class="vc-desc">Real-world data acquisition and operational infrastructure supporting AI and robotics training.</p>
              <span class="vc-link">Explore <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none"/></svg></span>
            </a>
            <a class="venture-card" href="/industrial-technology.html#industrial-ai" data-no-swup data-reveal data-delay="1">
              <span class="vc-sector">Industrial Technology</span>
              <h3>Industrial AI</h3>
              <p class="vc-desc">Applied AI and intelligent systems for physical and industrial environments.</p>
              <span class="vc-link">Explore <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none"/></svg></span>
            </a>
            <a class="venture-card" href="/industrial-technology.html#manufacturing" data-no-swup data-reveal>
              <span class="vc-sector">Industrial Technology</span>
              <h3>Manufacturing</h3>
              <p class="vc-desc">Manufacturing and physical-production capabilities serving institutional and commercial requirements.</p>
              <span class="vc-link">Explore <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none"/></svg></span>
            </a>
            <a class="venture-card" href="/ventures/bowl-and-sip/index.html" data-no-swup data-reveal data-delay="1">
              <span class="vc-sector">New Economy</span>
              <h3>Bowl &amp; Sip Co.</h3>
              <p class="vc-desc">A health-conscious food and lifestyle venture.</p>
              <span class="vc-link">Explore <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none"/></svg></span>
            </a>
            <a class="venture-card" href="/creator-house/" data-no-swup data-reveal>
              <span class="vc-sector">New Economy</span>
              <h3>Creator House</h3>
              <p class="vc-desc">A creator-first production and ecosystem venture.</p>
              <span class="vc-link">Explore <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none"/></svg></span>
            </a>
          </div>'''

def update_portfolio_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(r'<div class="portfolio-index-grid">.*?</div>\s*</div>\s*</section>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(portfolio_grid.replace('\\', '\\\\') + '\n        </div>\n      </section>', content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')
    else:
        print(f'Could not match portfolio-index-grid in {filepath}')

update_portfolio_page('c:/Data/Projects/Downloads/sz-ventures/portfolio.html')
