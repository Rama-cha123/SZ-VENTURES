import os

target_nav = '''   <nav class="nav__links" aria-label="Primary">
    <a href="/industrial-technology.html" class="nav__link">Industries</a>
    <a href="/ventures/" class="nav__link">Ventures</a>
    <a href="/creator-house/" class="nav__link">Creator House</a>
    <a href="/capabilities.html" class="nav__link">Capabilities</a>
    <a href="/about/" class="nav__link">About</a>
    <a href="/insights.html" class="nav__link">Insights</a>
    <a href="/contact.html" class="nav__link">Contact</a>
   </nav>'''

files = ['contact.html', 'insights.html', 'philosophy.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Simple extraction between <nav class="nav__links" and </nav>
    start = content.find('<nav class="nav__links"')
    if start != -1:
        end = content.find('</nav>', start) + 6
        if end != -1:
            old_nav = content[start:end]
            content = content.replace(old_nav, target_nav.strip())
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
