import os
import re
import chardet

directory = r"c:\Data\Projects\Downloads\sz-ventures"
files_to_fix = [
    "achievements.html",
    "careers.html",
    "contact.html",
    "cookies.html",
    "index.html",
    "insights.html",
    "philosophy.html",
    "portfolio.html",
    "press.html",
    "privacy.html",
    "prototype-hero.html",
    "team.html",
    "terms.html"
]

target_nav = """<nav class="footer-nav" aria-label="Footer">
        <div class="footer-nav-col">
         <h4>Industries</h4>
         <ul>
          <li><a href="/industrial-technology.html">Industrial Technology</a></li>
          <li><a href="/industrial-technology.html#ai-robotics-data">AI &amp; Robotics Data</a></li>
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
          <li><a href="/snapops/">SnapOps</a></li>
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
       </nav>"""

changed = []

for filename in files_to_fix:
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
        
    with open(path, 'rb') as f:
        raw = f.read()
    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
    
    try:
        content = raw.decode(encoding)
    except:
        content = raw.decode('utf-8', errors='ignore')
        
    pattern = r'<nav class="footer-nav"[^>]*>.*?</nav>'
    
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        new_content = content[:match.start()] + target_nav + content[match.end():]
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed.append(filename)

print("Changed files:", changed)
