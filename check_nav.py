with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('contact.html', 'r', encoding='utf-8') as f:
    contact_html = f.read()

import re

nav_index = re.search(r'(<nav class="nav__links".*?</nav>)', index_html, re.DOTALL)
nav_contact = re.search(r'(<nav class="nav__links".*?</nav>)', contact_html, re.DOTALL)

print('INDEX NAV LINKS:')
if nav_index:
    print(nav_index.group(1))

print('CONTACT NAV LINKS:')
if nav_contact:
    print(nav_contact.group(1))

