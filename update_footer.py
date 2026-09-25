import os
import glob

# 1. Update CSS
css_file = os.path.join('assets', 'styles', 'components.css')
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

if '.footer-nav { display: contents; }' not in css_content:
    with open(css_file, 'a', encoding='utf-8') as f:
        f.write('\n\n/* Fix footer navigation layout */\n.footer-nav { display: contents; }\n')
    print('Updated components.css')

# 2. Update HTML files
linkedin_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>'
instagram_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>'
youtube_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33 2.78 2.78 0 0 0 1.94 2c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.33 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>'

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()

        new_content = content
        
        # Replace LinkedIn
        new_content = new_content.replace('>LinkedIn</a>', f'>{linkedin_svg}</a>')
        # Replace Instagram
        new_content = new_content.replace('>Instagram</a>', f'>{instagram_svg}</a>')
        # Replace YouTube
        new_content = new_content.replace('>YouTube</a>', f'>{youtube_svg}</a>')

        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Updated icons in {f}')
    except Exception as e:
        print(f'Error processing {f}: {e}')
