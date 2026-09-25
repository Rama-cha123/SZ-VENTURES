import os

files = ['new-economy.html', os.path.join('new-economy', 'index.html')]

for f in files:
    try:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace('<div class="portfolio__list">', '<div class="portfolio__list" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">')
        
        content = content.replace('<a class="company"', '<a class="company" style="display: flex; flex-direction: column; align-items: flex-start; gap: 1.25rem; height: 100%;"')
        
        content = content.replace('<div class="company__cta" style="', '<div class="company__cta" style="margin-top: auto; ')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
    except Exception as e:
        print(f"Error: {e}")
