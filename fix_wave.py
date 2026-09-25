import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    skip = False
    for skip_dir in ['node_modules', '.git', 'ventures', '.agents', 'vendor-']:
        if skip_dir in root:
            skip = True
            break
    if skip: continue
    for file in files:
        if file.endswith('.html') and not file.startswith(('original_', 'temp_')):
            html_files.append(os.path.join(root, file))

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        continue

    # Fix: move wave canvas outside hero__bg
    old = '<div class="hero__gridlines"></div>\n<canvas id="sz-wave-canvas" aria-hidden="true"></canvas>\n</div>'
    new = '<div class="hero__gridlines"></div></div>\n<canvas id="sz-wave-canvas" aria-hidden="true"></canvas>'
    
    if old in content:
        content = content.replace(old, new)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Fixed {f}')
