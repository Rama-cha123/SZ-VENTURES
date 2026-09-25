import sys
import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

start_tag = '<footer class="footer" role="contentinfo">'
start_idx = idx_content.find(start_tag)
if start_idx == -1:
    print('Footer not found in index.html')
    sys.exit(1)
end_idx = idx_content.find('</footer>', start_idx) + len('</footer>')
footer_html = idx_content[start_idx:end_idx]

files = ['new-economy.html', os.path.join('new-economy', 'index.html')]
for f in files:
    try:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if '<footer class="footer"' not in content:
            new_content = content.replace('</main>', footer_html + '\n</main>')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Successfully added footer to {f}')
        else:
            print(f'{f} already has a footer.')
    except Exception as e:
        print(f'Error processing {f}: {e}')
