import os
from PIL import Image

cards_dir = os.path.join(os.getcwd(), 'assets', 'images', 'cards')
os.makedirs(cards_dir, exist_ok=True)

TARGET_W = 800
TARGET_H = 533

def crop_and_resize(src_path, dest_path, crop_anchor='center'):
    img = Image.open(src_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    src_w, src_h = img.size
    target_ratio = TARGET_W / TARGET_H
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider, crop width
        new_w = int(src_h * target_ratio)
        if crop_anchor == 'right':
            left = src_w - new_w
        elif crop_anchor == 'left':
            left = 0
        else:
            left = (src_w - new_w) // 2
        top = 0
        right = left + new_w
        bottom = src_h
    else:
        # Source is taller, crop height
        new_h = int(src_w / target_ratio)
        left = 0
        if crop_anchor == 'bottom':
            top = src_h - new_h
        elif crop_anchor == 'top':
            top = 0
        else:
            top = (src_h - new_h) // 2
        right = src_w
        bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))
    resized = cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    resized.save(dest_path, 'JPEG', quality=90, progressive=True)
    print(f"Generated {dest_path}: {resized.size}")

# 1. Bowl & Sip
bowl_src = os.path.join('assets', 'images', 'verticals', 'bowl-sip', 'bowl-sip-hero.webp')
bowl_dest = os.path.join(cards_dir, 'bowl-and-sip-card.jpg')
crop_and_resize(bowl_src, bowl_dest, crop_anchor='bottom')

# 2. Creator House
creator_src = os.path.join('assets', 'images', 'creator-house', 'creator-house-hero.webp')
creator_dest = os.path.join(cards_dir, 'creator-house-card.jpg')
crop_and_resize(creator_src, creator_dest, crop_anchor='right')

# 3. SnapOps
snap_src = r'C:\Users\bheem\.gemini\antigravity-ide\brain\e5806df9-334a-4a70-b13b-20f67836360f\snapops_local_services_1790438606992.jpg'
snap_dest = os.path.join(cards_dir, 'snapops-card.jpg')
crop_and_resize(snap_src, snap_dest, crop_anchor='center')

print("All 3 venture card images prepared successfully.")
