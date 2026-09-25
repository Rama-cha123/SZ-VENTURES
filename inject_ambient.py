import os

html_files = []
for root, dirs, files in os.walk('.'):
    skip = False
    for skip_dir in ['node_modules', '.git', 'ventures']:
        if skip_dir in root:
            skip = True
            break
    if skip: continue
    for file in files:
        if file.endswith('.html') and not file.startswith(('original_', 'temp_')):
            html_files.append(os.path.join(root, file))

# Also include specific venture pages that use the main site layout
# (not standalone venture pages with their own design)

css_link = '<link rel="stylesheet" href="/assets/styles/ambient.css">'
js_script = '<script src="/assets/js/ambient.js" defer></script>'
particles_canvas = '<canvas id="sz-particles-canvas" aria-hidden="true"></canvas>'
bokeh_div = '<div class="sz-bokeh" aria-hidden="true"></div>'
wave_marker = 'id="sz-wave-canvas"'

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        continue

    if 'ambient.css' in content:
        print(f'Skipping {f} (already has ambient)')
        continue

    new_content = content

    # 1. Add CSS link before </head>
    if '</head>' in new_content:
        new_content = new_content.replace('</head>', f' {css_link}\n</head>')

    # 2. Add particle canvas right after <body...>
    if particles_canvas not in new_content:
        # Find the first element after <body>
        import re
        body_match = re.search(r'<body[^>]*>', new_content)
        if body_match:
            insert_pos = body_match.end()
            new_content = new_content[:insert_pos] + f'\n{particles_canvas}\n{bokeh_div}\n' + new_content[insert_pos:]

    # 3. Add wave canvas inside hero section (if hero exists)
    if wave_marker not in new_content and '<section class="hero"' in new_content:
        # Insert wave canvas right after <div class="hero__bg"...>...</div>
        hero_bg_end = new_content.find('</div>', new_content.find('hero__bg'))
        if hero_bg_end != -1:
            hero_bg_end += len('</div>')
            wave_canvas = '\n<canvas id="sz-wave-canvas" aria-hidden="true"></canvas>\n'
            new_content = new_content[:hero_bg_end] + wave_canvas + new_content[hero_bg_end:]

    # 4. Add JS before </body>
    if 'ambient.js' not in new_content and '</body>' in new_content:
        new_content = new_content.replace('</body>', f'{js_script}\n</body>')

    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Updated {f}')
    else:
        print(f'No changes for {f}')
