import os
import re
from bs4 import BeautifulSoup

pages = [
    'creator-house/index.html',
    'ventures/snapops/index.html',
    'ventures/bowl-and-sip/index.html',
    'industrial-technology.html',
    'ventures/index.html',
    'index.html',
    'about/index.html'
]

for p in pages:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            print(f'\n--- {p} ---')
            # img tags
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                print(f"IMG: {src}")
            # style background-image
            for el in soup.find_all(style=re.compile(r'background-image')):
                print(f"BG: {el.get('style')}")
            # inline scripts or anything else with .webp or .jpg
            matches = re.findall(r'[\'"]([^\'"]+\.(?:webp|jpg|jpeg|png|svg))[\'"]', content)
            print(f"REGEX ASSETS: {set(matches)}")
