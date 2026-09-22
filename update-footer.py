import os
import re

footer_replacement = '''            <div class="footer-nav-col">
              <h4>Industries</h4>
              <ul>
                <li><a href="/industrial-technology.html">Industrial Technology</a></li>
                <li><a href="/industrial-technology.html#ai-robotics-data">AI & Robotics Data</a></li>
                <li><a href="/industrial-technology.html#industrial-ai">Industrial AI</a></li>
                <li><a href="/industrial-technology.html#manufacturing">Manufacturing</a></li>
                <li><a href="/new-economy.html">New Economy</a></li>
              </ul>
            </div>
            <div class="footer-nav-col">
              <h4>Ventures</h4>
              <ul>
                <li><a href="/ventures/bowl-and-sip/index.html">Bowl &amp; Sip Co.</a></li>
                <li><a href="/creator-house/">Creator House</a></li>
              </ul>
            </div>'''

def update_footer(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to match the first two footer-nav-cols: Industries and Ventures.
    # A robust way is to match from `<div class="footer-nav-col">` that has `<h4>Industries</h4>`
    # up to the end of the `<h4>Ventures</h4>` block.
    
    pattern = re.compile(r'<div class="footer-nav-col">\s*<h4>Industries</h4>.*?</ul>\s*</div>\s*<div class="footer-nav-col">\s*<h4>Ventures</h4>.*?</ul>\s*</div>', re.DOTALL | re.IGNORECASE)
    
    if pattern.search(content):
        new_content = pattern.sub(footer_replacement.replace('\\', '\\\\'), content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            # print(f'Updated footer in {filepath}')
    else:
        pass # print(f'Could not match footer in {filepath}')

count = 0
for root, dirs, files in os.walk('c:/Data/Projects/Downloads/sz-ventures'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            update_footer(filepath)
            count += 1
            
print(f'Processed {count} files for footer update.')
