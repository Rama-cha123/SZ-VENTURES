import os
import re

def update_anchors(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We replace:
    # <div style="margin-bottom: 4rem;" data-aos="fade-up">
    #             <span class="eyebrow">AI & ROBOTICS DATA</span>
    
    # This might match the general div structure. Let's do exact replacements.
    content = content.replace('<span class="eyebrow">AI & ROBOTICS DATA</span>', '<span class="eyebrow" id="ai-robotics-data">AI & ROBOTICS DATA</span>')
    content = content.replace('<span class="eyebrow">INDUSTRIAL AI</span>', '<span class="eyebrow" id="industrial-ai">INDUSTRIAL AI</span>')
    content = content.replace('<span class="eyebrow">MANUFACTURING</span>', '<span class="eyebrow" id="manufacturing">MANUFACTURING</span>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
update_anchors('c:/Data/Projects/Downloads/sz-ventures/industrial-technology.html')
update_anchors('c:/Data/Projects/Downloads/sz-ventures/industrial-technology/index.html')

print("Anchors added")
