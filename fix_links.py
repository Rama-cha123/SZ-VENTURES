import os
import glob

replacements = {
    '"bowl-sip.html"': '"/ventures/bowl-and-sip/index.html"',
    '"snapops.html"': '"/ventures/snapops/index.html"',
    '"mirai.html"': '"/ventures/mirai-engineering/index.html"',
    '"sz-manufacturing.html"': '"/ventures/manufacturing/index.html"',
    '"terramuse.html"': '"/ventures/terramuse/index.html"'
}

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed links in {filepath}")
