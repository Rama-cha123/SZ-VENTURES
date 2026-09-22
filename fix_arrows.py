with open('contact.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Add .interest-card__arrow to the three specific SVGs
html = re.sub(
    r'(<a href="#contact-form" class="vc-link">.*?)<svg viewBox="0 0 24 24" aria-hidden="true">',
    r'\1<svg class="interest-card__arrow" viewBox="0 0 24 24" aria-hidden="true">',
    html
)

with open('contact.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated contact.html SVGs')
