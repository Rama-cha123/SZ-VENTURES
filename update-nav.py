import os, re

nav_desktop_pattern = re.compile(r'(<a href="[^"]*?/ventures/?[^"]*"[^>]*>\s*Ventures\s*</a>)', re.IGNORECASE)
nav_mobile_pattern = re.compile(r'(<a href="[^"]*?/ventures/?[^"]*"[^>]*>\s*Ventures\s*<span>\d+</span>\s*</a>)', re.IGNORECASE)

count = 0

for root, dirs, files in os.walk('c:/Data/Projects/Downloads/sz-ventures'):
    if 'node_modules' in root or '.git' in root or 'creator-house' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            
            if 'Creator House' not in content or 'class="nav__link">Creator House' not in content:
                content = nav_desktop_pattern.sub(
                    r'\1\n   <a href="/creator-house/" class="nav__link">Creator House</a>', 
                    content
                )
            
            if 'data-menu-link>Creator House' not in content:
                content = nav_mobile_pattern.sub(
                    r'\1\n   <a href="/creator-house/" data-menu-link>Creator House <span>★</span></a>',
                    content
                )
                
            if orig != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                
print(f'Navigation updated in {count} files.')
