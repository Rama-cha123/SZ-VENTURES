import os, hashlib, json
from PIL import Image

# Paths
brain_dir = r'C:/Users/abdul/.gemini/antigravity/brain/12307cf0-1dd1-4e13-aaef-0b5ab42d8a44'
assets_dir = r'C:/Data/Projects/Downloads/sz-ventures/assets/images/creator-house'

# Mapping of source JPEG filenames (in brain) to target WebP filenames
files = {
    'creator_house_hero_1790092324322.jpg': 'creator-house-hero.webp',
    'creator_house_production_1790092366909.jpg': 'creator-house-production.webp',
    'creator_house_podcast_1790092397318.jpg': 'creator-house-podcast.webp',
    'creator_house_community_1790092418340.jpg': 'creator-house-community.webp',
}

# Ensure target directory exists
os.makedirs(assets_dir, exist_ok=True)

report = []
for src_name, dst_name in files.items():
    src_path = os.path.join(brain_dir, src_name)
    dst_path = os.path.join(assets_dir, dst_name)
    if not os.path.exists(src_path):
        report.append({"file": dst_name, "status": "source_missing", "source": src_path})
        continue
    # Open JPEG and convert to WebP
    try:
        with Image.open(src_path) as img:
            img = img.convert('RGB')  # ensure no alpha issues
            img.save(dst_path, format='WEBP', quality=90)
    except Exception as e:
        report.append({"file": dst_name, "status": "convert_error", "error": str(e)})
        continue
    # Gather metadata
    try:
        with open(dst_path, 'rb') as f:
            data = f.read()
            sha256 = hashlib.sha256(data).hexdigest()
            size = os.path.getsize(dst_path)
        with Image.open(dst_path) as img2:
            fmt = img2.format
            width, height = img2.size
        report.append({"file": dst_name, "status": "ok", "format": fmt, "width": width, "height": height, "size": size, "sha256": sha256})
    except Exception as e:
        report.append({"file": dst_name, "status": "metadata_error", "error": str(e)})

print(json.dumps(report, indent=2))
