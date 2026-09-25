import os
import re

snapops_company_card = """
  <!-- 06 SnapOps -->
  <a class="company" href="/snapops/" data-no-swup data-aos="fade-up" data-cursor data-tippy-content="Explore SnapOps">
  <div>
  <div class="company__name">SnapOps</div>
  <div style="font-size: var(--fs-300); color: var(--gold-light); margin-top: 0.25rem; font-family: var(--font-display);">Community Services, Simplified.</div>
  </div>
  <div class="company__thesis">A WhatsApp-first concept for connecting communities with nearby services and local businesses.</div>
  <div class="company__sector">New Economy</div>
  <div class="company__metric"><span class="status-badge status-badge--active" style="background:#38bdf8; color:#000;">Launching</span></div>
  <div class="company__cta" style="font-family: var(--font-display); font-size: 0.85rem; color: var(--gold); text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 0.5rem; white-space: nowrap;">Explore The Venture <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
  </a>"""

def repair_file(filepath):
    print(f"\nProcessing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Remove SnapOps from header
    header_end = c.find('</header>')
    if header_end == -1:
        print(f"  No </header> in {filepath}")
        return
    
    header = c[:header_end]
    body = c[header_end:]

    # Remove the rogue company card from header if present
    if '<!-- 06 SnapOps -->' in header:
        # find <!-- 06 SnapOps --> up to its closing </a>
        card_start = header.find('<!-- 06 SnapOps -->')
        card_end = header.find('</a>', card_start) + 4
        # remove any leading indentation or whitespace
        header = header[:card_start].rstrip(' \t') + '\n' + header[card_end:].lstrip(' \t\r\n')
        print(f"  Removed SnapOps company card from header in {filepath}")
    elif 'href="/snapops/"' in header:
        # Check if there is any other SnapOps link in header (like in portfolio dropdown)
        # In portfolio.html, remove the dropdown item
        m = re.search(r'\s*<a href="/snapops/"[^>]*>.*?</a>', header, re.DOTALL)
        if m:
            header = header[:m.start()] + header[m.end():]
            print(f"  Removed SnapOps dropdown item from header in {filepath}")

    # Recombine to work with whole content
    c = header + body

    # 2. Check body: find Creator House card inside the venture grid
    # Looking for: <!-- 05 Creator House -->
    ch_comment = '<!-- 05 Creator House -->'
    idx_ch = c.find(ch_comment)
    if idx_ch != -1:
        # find the end of Creator House card
        idx_ch_end = c.find('</a>', idx_ch) + 4
        # check if SnapOps card is already immediately following
        remainder = c[idx_ch_end:idx_ch_end+400]
        if '<!-- 06 SnapOps -->' not in remainder:
            c = c[:idx_ch_end] + snapops_company_card + c[idx_ch_end:]
            print(f"  Inserted SnapOps card immediately after Creator House card in {filepath}")
        else:
            print(f"  SnapOps card already after Creator House in {filepath}")
    else:
        # In portfolio.html, Creator House is: <h3>Creator House</h3>
        if '<h3>Creator House</h3>' in c:
            idx_ch = c.find('<h3>Creator House</h3>')
            idx_ch_end = c.find('</a>', idx_ch) + 4
            remainder = c[idx_ch_end:idx_ch_end+500]
            if '<h3>SnapOps</h3>' in remainder:
                print(f"  SnapOps venture-card already immediately after Creator House in {filepath}")
            else:
                print(f"  WARNING: Creator House found in {filepath} but SnapOps card not after it!")

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(c)
    print(f"Done repairing {filepath}")

for f in ['index.html', 'ventures/index.html', 'portfolio.html', 'new-economy.html', 'new-economy/index.html']:
    repair_file(f)
