import os
import re
import chardet

directory = r"c:\Data\Projects\Downloads\sz-ventures"
html_files = []
for root, dirs, files in os.walk(directory):
    if 'vendor' in root or '.agents' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

def process_file(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
    try:
        content = raw.decode(encoding)
    except:
        content = raw.decode('utf-8', errors='ignore')

    if '<footer' not in content:
        return False
        
    footer_start = content.find('<footer')
    footer_end = content.find('</footer>', footer_start)
    if footer_start == -1 or footer_end == -1:
        return False
        
    footer_content = content[footer_start:footer_end]
    
    ventures_col_pattern = r'(<div class="footer-nav-col">\s*<h4>Ventures</h4>\s*<ul>)(.*?)(</ul>\s*</div>)'
    
    match = re.search(ventures_col_pattern, footer_content, re.DOTALL)
    if not match:
        return False
        
    ul_content = match.group(2)
    
    # We want exactly these 3:
    # <li><a href="/ventures/bowl-and-sip/index.html">Bowl &amp; Sip Co.</a></li>
    # <li><a href="/creator-house/">Creator House</a></li>
    # <li><a href="/snapops/">SnapOps</a></li>
    
    # Check if SnapOps is there. If it is there multiple times, we fix it.
    # If it is missing, we add it.
    # Let's just reconstruct the inner ul content entirely to be perfect and uniform.
    
    new_ul_content = '\n          <li><a href="/ventures/bowl-and-sip/index.html">Bowl &amp; Sip Co.</a></li>\n          <li><a href="/creator-house/">Creator House</a></li>\n          <li><a href="/snapops/">SnapOps</a></li>\n         '
    
    if ul_content == new_ul_content:
        return False
        
    new_footer_content = footer_content[:match.start(2)] + new_ul_content + footer_content[match.end(2):]
    
    new_content = content[:footer_start] + new_footer_content + content[footer_end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

changed = []
for f in html_files:
    if process_file(f):
        changed.append(f)
        
print("Changed:", changed)
