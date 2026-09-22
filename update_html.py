import re

# Creator House
with open('ventures/creator-house/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '1600861194942-f883de0dfe96?q=85&w=1800&auto=format&fit=crop&ixlib=rb-4.0.3&cs=tinysrgb': '/assets/images/verticals/creator-house/creator-house-hero.webp',
    '1522202176988-66273c2fd55f?q=85&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&cs=tinysrgb': '/assets/images/verticals/creator-house/creator-house-photography.webp',
    '1604014237800-1c9102c219da?q=85&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&cs=tinysrgb': '/assets/images/verticals/creator-house/creator-house-video.webp',
    '1531746020798-e6953c6e8e04?q=85&w=900&auto=format&fit=crop&ixlib=rb-4.0.3&cs=tinysrgb': '/assets/images/verticals/creator-house/creator-house-podcast.webp'
}

for old, new_url in replacements.items():
    text = re.sub(r'https://images.unsplash.com/photo-' + re.escape(old), new_url, text)

with open('ventures/creator-house/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Manufacturing
with open('ventures/manufacturing/index.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?q=80&w=2000&auto=format&fit=crop', '/assets/images/verticals/manufacturing/manufacturing-hero.webp')

with open('ventures/manufacturing/index.html', 'w', encoding='utf-8') as f:
    f.write(text2)

# Bowl & Sip
with open('ventures/bowl-and-sip/index.html', 'r', encoding='utf-8') as f:
    text3 = f.read()

text3 = re.sub(r'https://images\.unsplash\.com/photo-[^\"]+', '/assets/images/verticals/bowl-sip/bowl-sip-hero.webp', text3, count=1)

with open('ventures/bowl-and-sip/index.html', 'w', encoding='utf-8') as f:
    f.write(text3)

print('Updated images')
