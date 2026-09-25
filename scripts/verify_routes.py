import urllib.request
import urllib.error
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

routes = [
    ('/', 200),
    ('/creator-house/', 200),
    ('/creator-house', 200),
    ('/about/', 200),
    ('/about', 200),
    ('/ventures/', 200),
    ('/ventures', 200),
    ('/snapops/', 200),
    ('/snapops', 200),
    ('/portfolio', 200),
    ('/portfolio.html', 200),
    ('/assets/images/creator-house/creator-house-hero.webp', 200),
    ('/assets/images/creator-house/creator-house-production.webp', 200),
    ('/assets/images/creator-house/creator-house-podcast.webp', 200),
    ('/assets/images/founder/sridhar-chakkravarthy.webp', 200),
    ('/assets/images/founder/sridhar-chakkravarthy.png', 200),
]

print("=== ROUTE HTTP STATUS CHECKS ===")
all_passed = True
for path, expected_code in routes:
    url = f"http://localhost:3000{path}"
    try:
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req) as resp:
            code = resp.status
            content_type = resp.headers.get('Content-Type', '')
            status_str = "PASS" if code == expected_code else "FAIL"
            print(f"[{status_str}] {path:55} -> {code} ({content_type})")
            if code != expected_code:
                all_passed = False
    except urllib.error.HTTPError as e:
        status_str = "PASS" if e.code == expected_code else "FAIL"
        print(f"[{status_str}] {path:55} -> {e.code} (HTTPError)")
        if e.code != expected_code:
            all_passed = False
    except Exception as ex:
        print(f"[ERROR] {path:55} -> {ex}")
        all_passed = False

print("\n=== CREATOR HOUSE CONTENT VERIFICATION ===")
ch_url = "http://localhost:3000/creator-house/"
req = urllib.request.Request(ch_url, method='GET')
with urllib.request.urlopen(req) as resp:
    ch_html = resp.read().decode('utf-8')

# 1. Images
hero_count = ch_html.count('/assets/images/creator-house/creator-house-hero.webp')
prod_count = ch_html.count('/assets/images/creator-house/creator-house-production.webp')
pod_count = ch_html.count('/assets/images/creator-house/creator-house-podcast.webp')
comm_count = ch_html.count('/assets/images/creator-house/creator-house-community.webp')
print(f"Hero image count (img/meta): {hero_count}")
print(f"Production image count: {prod_count}")
print(f"Podcast image count: {pod_count}")
print(f"Community image count (should be 0): {comm_count}")

# Check exact <img> tags
img_tags = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', ch_html)
ch_imgs = [src for src in img_tags if 'creator-house' in src]
print(f"Creator House <img> tags: {ch_imgs}")

# 2. Pricing and CTA
has_4999 = '4,999' in ch_html
has_3499 = '3,499' in ch_html
has_300 = '300 Subscriptions' in ch_html or '300 subscriptions' in ch_html
has_cta = 'CLAIM EARLY-BIRD MEMBERSHIP' in ch_html
print(f"Visible ₹4,999: {has_4999}")
print(f"Visible ₹3,499: {has_3499}")
print(f"Visible 300 subscriptions: {has_300}")
print(f"Primary CTA 'CLAIM EARLY-BIRD MEMBERSHIP': {has_cta}")

# 3. Metadata
title_match = re.search(r'<title>(.*?)</title>', ch_html)
desc_match = re.search(r'<meta name="description" content="(.*?)">', ch_html)
canonical_match = re.search(r'<link rel="canonical" href="(.*?)">', ch_html)
print(f"Title: {title_match.group(1) if title_match else 'None'}")
print(f"Canonical: {canonical_match.group(1) if canonical_match else 'None'}")

print("\n=== SNAPS OPS CONTENT VERIFICATION ===")
snap_url = "http://localhost:3000/snapops/"
with urllib.request.urlopen(urllib.request.Request(snap_url)) as resp:
    snap_html = resp.read().decode('utf-8')

fake_terms = ['100k', '100 Thousand', '350+', '350 Communities', '2.5M', '2.5 Million', 'Priya', 'Vikram', 'Rajesh', 'Ananya']
found_fake = [t for t in fake_terms if t in snap_html]
print(f"Fake metrics/testimonials found: {found_fake} (should be empty)")
has_principles = 'Our Core Launch Principles' in snap_html
has_use_cases = 'Illustrative Use Cases' in snap_html
has_launch_updates_cta = '/contact.html?intent=snapops' in snap_html
dead_links = re.findall(r'href="#"', snap_html)
print(f"Has Launch Principles: {has_principles}")
print(f"Has Illustrative Use Cases: {has_use_cases}")
print(f"Has '/contact.html?intent=snapops' CTAs: {has_launch_updates_cta}")
print(f"Dead href='#' count: {len(dead_links)} (should be 0)")

print("\n=== ABOUT PAGE FOUNDER VERIFICATION ===")
about_url = "http://localhost:3000/about/"
with urllib.request.urlopen(urllib.request.Request(about_url)) as resp:
    about_html = resp.read().decode('utf-8')

has_founder_name = 'Sridhar Chakkravarthy' in about_html
has_founder_role = 'Founder — SZ Ventures Private Limited' in about_html
has_linkedin = 'https://www.linkedin.com/in/sridharchakkravarthy/' in about_html
founder_img = re.search(r'<img[^>]+founder__portrait[^>]*>', about_html)
print(f"Founder name present: {has_founder_name}")
print(f"Founder role present: {has_founder_role}")
print(f"LinkedIn URL present: {has_linkedin}")
print(f"Founder image markup: {founder_img.group(0) if founder_img else 'None'}")

print("\n=== FORM / API ENDPOINT TEST ===")
api_url = "http://localhost:3000/api/submit"
payload = {
    "source": "partnership_inquiry",
    "full_name": "Verification Bot",
    "email": "verify@szventures.com",
    "phone": "+91 98765 43210",
    "message": "Automated verification test of API submission endpoint."
}
req = urllib.request.Request(
    api_url, 
    data=json.dumps(payload).encode('utf-8'),
    headers={
        'Content-Type': 'application/json',
        'X-Idempotency-Key': f'verify-{json.dumps(payload, sort_keys=True).__hash__()}'
    },
    method='POST'
)
try:
    with urllib.request.urlopen(req) as resp:
        resp_data = json.loads(resp.read().decode('utf-8'))
        print(f"API Response: {resp.status} - {resp_data}")
except Exception as ex:
    print(f"API Error: {ex}")
