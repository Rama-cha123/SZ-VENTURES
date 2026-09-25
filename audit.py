import os
from bs4 import BeautifulSoup
from collections import Counter

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
            soup = BeautifulSoup(f.read(), 'html.parser')
            imgs = soup.find_all('img')
            print(f'\n--- {p} ---')
            sources = [img.get('src') for img in imgs if img.get('src')]
            counts = Counter(sources)
            for src, count in counts.items():
                print(f'{count}x {src}')
