import re
import os

files = ['index.html', 'new-economy.html', 'portfolio_block.html', 'ventures/index.html', 'portfolio.html', 'industrial-technology.html']

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # AI & Robotics Data
        content = re.sub(
            r'(<a class="(?:company|venture-card)"[^>]*href="[^"]*ai-robotics-data"[^>]*>)\s*<div>',
            r'\1\n  <div class="company__bg" style="background-image: url(\'/assets/images/cards/ai-robotics-card.jpg\');"></div>\n  <div>',
            content
        )
        
        # Industrial AI
        content = re.sub(
            r'(<a class="(?:company|venture-card)"[^>]*href="[^"]*industrial-ai"[^>]*>)\s*<div>',
            r'\1\n  <div class="company__bg" style="background-image: url(\'/assets/images/cards/industrial-ai-card.jpg\');"></div>\n  <div>',
            content
        )
        
        # Manufacturing
        content = re.sub(
            r'(<a class="(?:company|venture-card)"[^>]*href="[^"]*manufacturing"[^>]*>)\s*<div>',
            r'\1\n  <div class="company__bg" style="background-image: url(\'/assets/images/cards/manufacturing-card.jpg\');"></div>\n  <div>',
            content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Injected backgrounds.")
