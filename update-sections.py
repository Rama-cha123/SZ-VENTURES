import os
import re

with open('c:/Data/Projects/Downloads/sz-ventures/portfolio_block.html', 'r', encoding='utf-8') as f:
    portfolio_cards = f.read()

replacement = f'''  <section class="section portfolio">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow" data-aos="fade">OUR VENTURES</span>
        <h2 data-aos="fade-up">A PORTFOLIO BUILT FOR WHAT'S NEXT.</h2>
      </div>
      <div class="portfolio__list">
{portfolio_cards}
      </div>
    </div>
  </section>'''

def replace_section(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We find <section class="section portfolio"> ... </section>
    pattern = re.compile(r'<section class="section portfolio">.*?</section>', re.DOTALL)
    if pattern.search(content):
        new_content = pattern.sub(replacement.replace('\\', '\\\\'), content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')
    else:
        print(f'Could not find section in {filepath}')

files_to_update = [
    'c:/Data/Projects/Downloads/sz-ventures/ventures/index.html',
    'c:/Data/Projects/Downloads/sz-ventures/new-economy/index.html',
    'c:/Data/Projects/Downloads/sz-ventures/new-economy.html'
]

for f in files_to_update:
    replace_section(f)
