import os
import re

css_file = os.path.join('assets', 'styles', 'components.css')

with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .vertical-card base styles to add glassmorphism
old_card = """.vertical-card {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    transition: border-color 0.3s ease, transform 0.35s ease, box-shadow 0.35s ease;
    scroll-margin-top: 120px;
}"""

new_card = """.vertical-card {
    display: flex;
    flex-direction: column;
    background: var(--glass-bg, rgba(10, 10, 12, 0.6));
    backdrop-filter: blur(16px) saturate(140%);
    -webkit-backdrop-filter: blur(16px) saturate(140%);
    border: 1px solid var(--line-soft, rgba(255, 255, 255, 0.08));
    border-radius: 1rem;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    transition: all 0.4s var(--ease-premium, cubic-bezier(.23,1,.32,1));
    scroll-margin-top: 120px;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05), 0 10px 30px rgba(0, 0, 0, 0.3);
    position: relative;
}
.vertical-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 1rem;
    pointer-events: none;
    background: linear-gradient(to bottom, rgba(255,255,255,0.03) 0%, transparent 100%);
    z-index: 2;
}
"""
content = content.replace(old_card, new_card)

# 2. Update .vertical-card:hover
old_hover = """    .vertical-card:hover {
        border-color: var(--gold, #dcb46e);
        transform: translateY(-5px);
        box-shadow: 0 20px 48px rgba(0, 0, 0, 0.45);
    }"""
new_hover = """    .vertical-card:hover {
        border-color: rgba(220, 180, 110, 0.4);
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 24px 50px rgba(0, 0, 0, 0.6), 0 0 40px rgba(220, 180, 110, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        background: rgba(20, 18, 22, 0.85);
    }"""
content = content.replace(old_hover, new_hover)

# 3. Enhance .vertical-card__image with overlay
old_image = """.vertical-card__image {
    overflow: hidden;
    line-height: 0;
    aspect-ratio: 16 / 9;
}"""
new_image = """.vertical-card__image {
    overflow: hidden;
    line-height: 0;
    aspect-ratio: 16 / 9;
    position: relative;
}
.vertical-card__image::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(10, 10, 12, 0.9) 0%, transparent 50%);
    pointer-events: none;
    z-index: 1;
}"""
content = content.replace(old_image, new_image)

# 4. Change font of heading
old_heading = """.vertical-card__heading {
    font-family: var(--font-display, 'Fraunces', serif);
    font-size: 1.3rem;
    font-weight: 500;
    line-height: 1.2;
    color: var(--white, #fff);
    margin: 0;
}"""
new_heading = """.vertical-card__heading {
    font-family: var(--font-display, "Space Grotesk", sans-serif);
    font-size: 1.35rem;
    font-weight: 600;
    line-height: 1.25;
    color: var(--white, #fff);
    margin: 0;
    letter-spacing: -0.01em;
}"""
content = content.replace(old_heading, new_heading)

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated components.css with improved vertical-card styles.")
