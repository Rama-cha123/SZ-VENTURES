import os
import re

path = r'c:\Data\Projects\Downloads\sz-ventures\ventures\snapops\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# The current logo block looks like this:
# <div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-105 group-hover:shadow-brand-secondary/50 transition-all duration-300">
#  <i class="ph ph-lightning text-xl font-bold"></i>
# </div>

new_logo_html = """<div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-105 group-hover:shadow-brand-secondary/50 transition-all duration-300 relative overflow-hidden">
       <svg viewBox="0 0 24 24" class="w-6 h-6 fill-none stroke-white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
        <path d="M13 8L9.5 13h4l-1.5 5" class="stroke-brand-accent"/>
       </svg>
      </div>"""

# Replace in header
content = re.sub(
    r'<div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white shadow-lg\s*group-hover:scale-105 group-hover:shadow-brand-secondary/50 transition-all duration-300">\s*<i class="ph ph-lightning text-xl font-bold"></i>\s*</div>',
    new_logo_html,
    content
)

# Replace in footer
# The footer has slightly different classes:
# <div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white">
#  <i class="ph ph-lightning text-xl font-bold"></i>
# </div>

new_footer_logo = """<div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white relative overflow-hidden">
         <svg viewBox="0 0 24 24" class="w-6 h-6 fill-none stroke-white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
          <path d="M13 8L9.5 13h4l-1.5 5" class="stroke-brand-accent"/>
         </svg>
        </div>"""

content = re.sub(
    r'<div class="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center text-white">\s*<i class="ph ph-lightning text-xl font-bold"></i>\s*</div>',
    new_footer_logo,
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SnapOps logos")
