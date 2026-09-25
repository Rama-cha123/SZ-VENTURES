import os
import re

css_file = os.path.join('assets', 'styles', 'components.css')

with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Change vertical-card-grid to 1 column
content = content.replace('grid-template-columns: repeat(3, 1fr);', 'grid-template-columns: 1fr;\n    max-width: 900px;\n    margin-left: auto;\n    margin-right: auto;')

# Change vertical-card__link to flex-direction: row and align items
old_link = """.vertical-card__link {
    display: flex;
    flex-direction: column;
    flex: 1;
    text-decoration: none;
    color: inherit;
    height: 100%;
}"""
new_link = """.vertical-card__link {
    display: flex;
    flex-direction: row;
    flex: 1;
    text-decoration: none;
    color: inherit;
    height: 100%;
    align-items: center;
}"""
content = content.replace(old_link, new_link)

# Update vertical-card__image for horizontal layout
old_img = """.vertical-card__image {
    overflow: hidden;
    line-height: 0;
    aspect-ratio: 16 / 9;
    position: relative;
}"""
new_img = """.vertical-card__image {
    overflow: hidden;
    line-height: 0;
    aspect-ratio: 16 / 9;
    position: relative;
    width: 45%;
    flex-shrink: 0;
}"""
content = content.replace(old_img, new_img)

# Update image gradient overlay to match row layout
old_img_after = """.vertical-card__image::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(10, 10, 12, 0.9) 0%, transparent 50%);
    pointer-events: none;
    z-index: 1;
}"""
new_img_after = """.vertical-card__image::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, transparent 50%, rgba(10, 10, 12, 0.9) 100%);
    pointer-events: none;
    z-index: 1;
}"""
content = content.replace(old_img_after, new_img_after)

# Update body padding
old_body = """.vertical-card__body {
    padding: 1.75rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}"""
new_body = """.vertical-card__body {
    padding: 2.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
}"""
content = content.replace(old_body, new_body)

# Add media query to stack on mobile
media_query = """
@media (max-width: 768px) {
    .vertical-card__link {
        flex-direction: column;
    }
    .vertical-card__image {
        width: 100%;
    }
    .vertical-card__image::after {
        background: linear-gradient(to top, rgba(10, 10, 12, 0.9) 0%, transparent 50%);
    }
    .vertical-card__body {
        padding: 1.75rem;
    }
}
"""

if "flex-direction: column;" not in content.split(".vertical-card__link")[-1]: # check if we haven't already added it
    content += media_query

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated components.css to make cards horizontal.")
