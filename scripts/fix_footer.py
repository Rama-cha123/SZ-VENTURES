import os
import glob
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

def fix_footer(file_path):
    # Detect encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        
    encoding = chardet.detect(raw_data)['encoding']
    if not encoding:
        encoding = 'utf-8'

    try:
        content = raw_data.decode(encoding)
    except Exception as e:
        try:
            content = raw_data.decode('utf-8', errors='ignore')
            encoding = 'utf-8'
        except:
            return False

    if '<footer' not in content:
        return False
        
    # Check if SnapOps is already there inside the Ventures column
    
    # We want to replace the Ventures column with the exact correct one
    pattern = r'(<div class="footer-nav-col">\s*<h4>Ventures</h4>\s*<ul>\s*<li><a href="/ventures/bowl-and-sip/index\.html">Bowl &amp; Sip Co\.</a></li>\s*<li><a href="/creator-house/">Creator House</a></li>\s*)(</ul>\s*</div>)'
    
    replacement = r'\1<li><a href="/snapops/">SnapOps</a></li>\n         \2'
    
    new_content, count = re.subn(pattern, replacement, content)
    
    if count > 0:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
        return True
    return False

changed_files = []
for file in html_files:
    if fix_footer(file):
        changed_files.append(file)

print("Changed files:")
for f in changed_files:
    print(f)
