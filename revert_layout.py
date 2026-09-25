import os

files = ['new-economy.html', os.path.join('new-economy', 'index.html')]

for f in files:
    try:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()

        # Revert changes
        content = content.replace('<div class="portfolio__list" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">', '<div class="portfolio__list">')
        
        content = content.replace('<a class="company" style="display: flex; flex-direction: column; align-items: flex-start; gap: 1.25rem; height: 100%;"', '<a class="company"')
        
        content = content.replace('<div class="company__cta" style="margin-top: auto; ', '<div class="company__cta" style="')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Reverted {f}")
    except Exception as e:
        print(f"Error: {e}")
