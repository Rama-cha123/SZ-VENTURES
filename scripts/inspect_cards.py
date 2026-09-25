import re

files = ['index.html', 'ventures/index.html', 'portfolio.html', 'new-economy.html', 'new-economy/index.html']

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    header_end = c.find('</header>')
    header_content = c[:header_end] if header_end != -1 else ''
    body_content = c[header_end:] if header_end != -1 else c

    print(f"\n==================== {fpath} ====================")
    # Check if company or venture-card is in header
    snapops_in_header = 'SnapOps' in header_content
    card_in_header = ('class="company"' in header_content and 'snapops' in header_content) or ('class="venture-card"' in header_content and 'snapops' in header_content)
    print(f"SnapOps in header: {snapops_in_header}")
    print(f"SnapOps full card in header: {card_in_header}")

    # Check cards in body
    company_cards = re.findall(r'<a[^>]+class=[\'"][^\'"]*company[^\'"]*[\'"][^>]*href=[\'"][^\'"]*snapops[^\'"]*[\'"]', body_content, re.I)
    venture_cards = re.findall(r'<a[^>]+class=[\'"][^\'"]*venture-card[^\'"]*[\'"][^>]*href=[\'"][^\'"]*snapops[^\'"]*[\'"]', body_content, re.I)
    print(f"Company cards in body: {len(company_cards)}")
    print(f"Venture-cards in body: {len(venture_cards)}")

    # Check immediate parent of SnapOps card in body or header
    for m in re.finditer(r'<a[^>]+href=[\'"][^\'"]*snapops[^\'"]*[\'"][^>]*>', c, re.I):
        start = m.start()
        # look backward for the opening tag of parent
        preceding = c[max(0, start-400):start]
        # find the last opening tag before this
        parent_tag_matches = list(re.finditer(r'<([a-zA-Z0-9\-]+)([^>]*)>', preceding))
        if parent_tag_matches:
            last_parent = parent_tag_matches[-1]
            print(f"  Parent tag before SnapOps link: <{last_parent.group(1)} {last_parent.group(2).strip()[:60]}>")
