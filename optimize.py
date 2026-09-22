import os
from PIL import Image
import glob

# Map image names to output paths
mapping = {
    'industrial_ai_hero': r'c:\Data\Projects\Downloads\sz-ventures\assets\images\verticals\industrial-ai\industrial-ai-hero.webp',
    'manufacturing_hero': r'c:\Data\Projects\Downloads\sz-ventures\assets\images\verticals\manufacturing\manufacturing-hero.webp',
    'bowl_sip_hero': r'c:\Data\Projects\Downloads\sz-ventures\assets\images\verticals\bowl-sip\bowl-sip-hero.webp',
    'creator_house_hero': r'c:\Data\Projects\Downloads\sz-ventures\assets\images\verticals\creator-house\creator-house-hero.webp'
}

artifact_dir = r'C:\Users\abdul\.gemini\antigravity-ide\brain\3aa84af8-5706-401b-8842-d8c0e080a817'

for key, dest in mapping.items():
    # find the file in artifact dir
    files = glob.glob(os.path.join(artifact_dir, f'{key}_*.jpg'))
    if not files:
        print(f"Skipping {key} - no file found")
        continue
    
    # Take newest
    src = max(files, key=os.path.getctime)
    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img = Image.open(src)
    img.save(dest, 'WEBP', quality=80)
    print(f"Optimized {key} to {dest}")

