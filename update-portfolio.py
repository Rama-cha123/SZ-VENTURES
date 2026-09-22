import os
import re

with open('c:/Data/Projects/Downloads/sz-ventures/portfolio_block.html', 'r', encoding='utf-8') as f:
    portfolio_cards = f.read()

def replace_portfolio(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_str = '<div class="portfolio__list">'
    if start_str in content:
        start_idx = content.find(start_str) + len(start_str)
        
        # In index.html, it's followed by </div> </div> </section>
        end_str = '    </div>\n    </div>\n    </section>'
        end_idx = content.find(end_str, start_idx)
        
        if end_idx == -1:
            # Try a looser end match
            end_match = re.search(r'</div>\s*</div>\s*</section>', content[start_idx:])
            if end_match:
                end_idx = start_idx + end_match.start()
        
        if end_idx != -1:
            new_content = content[:start_idx] + '\n' + portfolio_cards + '\n    ' + content[end_idx:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filepath}')
        else:
            print(f'Found start but not end in {filepath}')
    else:
        print(f'Could not find start block in {filepath}')

replace_portfolio('c:/Data/Projects/Downloads/sz-ventures/index.html')
