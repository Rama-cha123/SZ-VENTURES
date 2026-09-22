import urllib.request
import os

images = {
    'ai-robotics-card.jpg': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=800',
    'industrial-ai-card.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=800',
    'manufacturing-card.jpg': 'https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?q=80&w=800'
}

dest_dir = r'c:\Data\Projects\Downloads\sz-ventures\assets\images\cards'
os.makedirs(dest_dir, exist_ok=True)

for name, url in images.items():
    dest = os.path.join(dest_dir, name)
    print(f'Downloading {name}...')
    urllib.request.urlretrieve(url, dest)

print('All images downloaded successfully.')
