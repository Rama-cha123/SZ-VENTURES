import glob

html_files = glob.glob('*.html')
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove style.css link
    content = content.replace('  <link rel="stylesheet" href="style.css">\n', '')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print(f'Processed {len(html_files)} files.')
