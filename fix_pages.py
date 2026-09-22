import re

# Read portfolio.html as template source
with open('portfolio.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract parts
header_match = re.search(r'(<!-- Header Navigation -->.*?</header>)', template, re.DOTALL)
if not header_match:
    print('Failed to find header in portfolio.html')
    exit(1)
header = header_match.group(1)

menu_match = re.search(r'(<!-- Mobile Drawer Menu -->.*?</div>\s*</nav>)', template, re.DOTALL)
menu = menu_match.group(1) if menu_match else ''

footer_match = re.search(r'(<footer class="footer".*?</footer>)', template, re.DOTALL)
if not footer_match:
    print('Failed to find footer in portfolio.html')
    exit(1)
footer = footer_match.group(1)

files_to_fix = ['insights.html', 'philosophy.html', 'contact.html']

for filename in files_to_fix:
    print(f'Fixing {filename}...')
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Header
    content = re.sub(r'<!-- Header Navigation -->.*?</header>', header, content, flags=re.DOTALL)
    
    # Replace Mobile Menu (if exists) or insert it after header
    if '<!-- Mobile Drawer Menu -->' in content:
        content = re.sub(r'<!-- Mobile Drawer Menu -->.*?</div>\s*</nav>', menu, content, flags=re.DOTALL)
    else:
        # Insert menu after header
        content = content.replace('</header>', '</header>\n\n ' + menu)
    
    # Replace main
    content = content.replace('<main id="main">', '<main id="swup" class="transition-fade">')
    content = content.replace('<main>', '<main id="swup" class="transition-fade">')
    
    # Replace Footer
    content = re.sub(r'<footer class="footer".*?</footer>', footer, content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done fixing HTML files')
