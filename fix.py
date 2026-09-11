import os

files = {
    'ventures/manufacturing/index.html': 'SZ Manufacturing',
    'ventures/mirai-engineering/index.html': 'Mirai Engineering',
    'ventures/snapops/index.html': 'SnapOps'
}

for file_path, venture_name in files.items():
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_header_1 = '''<a href="/index.html" class="nav__brand" data-cursor data-tippy-content="SZX Ventures">
      <img src="../../assets/img/logo.png" alt="SZX Ventures Logo" class="nav-logo-img" aria-hidden="true">
      SZX Ventures
    </a>'''
        old_header_2 = '''<a href="/index.html" class="nav__brand" data-cursor data-tippy-content="SZX Ventures — Venture Studio">
      <img src="../../assets/img/logo.png" alt="SZX Ventures Logo" class="nav-logo-img" aria-hidden="true">
      SZX Ventures
    </a>'''
        
        new_header = f'''<a href="/index.html" class="nav__brand" data-cursor data-tippy-content="Return to Parent Ecosystem">
      <img src="../../assets/img/logo.png" alt="SZX Ventures Logo" class="nav-logo-img" aria-hidden="true" style="opacity: 0.5;">
      <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">
        <span style="line-height: 1.1;">{venture_name}</span>
        <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--gold); margin-top: 0.15rem; font-family: var(--font-body);">A SZX Ventures company</span>
      </div>
    </a>'''
        
        if old_header_1 in content:
            content = content.replace(old_header_1, new_header)
        elif old_header_2 in content:
            content = content.replace(old_header_2, new_header)
        else:
            print(f'Could not find exact old header in {file_path}')
            continue
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file_path}')
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
