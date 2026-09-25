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
            for src in soup.find_all('source'):
                print(f"SOURCE: {src.get('srcset')}")
            for img in soup.find_all('img'):
                print(f"IMG: {img.get('src')}")
