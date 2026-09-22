import os
import re

footer_nav_replacement = '''          <nav class="footer-nav" aria-label="Footer">
            <div class="footer-nav-col">
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
            </div>
            <div class="footer-nav-col">
              <h4>Company</h4>
              <ul>
                <li><a href="/about/">About</a></li>
                <li><a href="/ventures/">Ventures</a></li>
                <li><a href="/capabilities.html">Capabilities</a></li>
                <li><a href="/insights.html">Insights</a></li>
                <li><a href="/contact.html">Contact</a></li>
              </ul>
            </div>
          </nav>'''

def update_footer(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We replace from <nav class="footer-nav" to </nav>
    # Note that there's another </nav> in the header, so we match specifically:
    pattern = re.compile(r'<nav class="footer-nav" aria-label="Footer">.*?</nav>', re.DOTALL | re.IGNORECASE)
    
    if pattern.search(content):
        new_content = pattern.sub(footer_nav_replacement.replace('\\', '\\\\'), content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    else:
        pass # print(f'Could not match footer-nav in {filepath}')

count = 0
for root, dirs, files in os.walk('c:/Data/Projects/Downloads/sz-ventures'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            update_footer(filepath)
            count += 1
            
print(f'Processed {count} files for full footer-nav replacement.')
