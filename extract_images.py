import os, re
images = set()
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            with open(os.path.join(root, f), 'r', encoding='utf-8') as html:
                for match in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html.read()):
                    images.add(match)

for i in sorted(images):
    print(i)
