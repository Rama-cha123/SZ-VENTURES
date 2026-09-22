with open('assets/styles/components.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css = '''
.js [data-reveal] {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity var(--motion-reveal) var(--ease-premium), transform var(--motion-reveal) var(--ease-premium);
    will-change: opacity, transform;
}
.js [data-reveal].is-visible {
    opacity: 1;
    transform: none;
}
[data-reveal][data-delay="1"] { transition-delay: 0.08s; }
[data-reveal][data-delay="2"] { transition-delay: 0.16s; }
[data-reveal][data-delay="3"] { transition-delay: 0.24s; }
[data-reveal][data-delay="4"] { transition-delay: 0.32s; }
'''

import re
css = re.sub(r'\.js \[data-reveal\] \{.*?\[data-reveal\]\[data-delay="4"\].*?\}', new_css.strip(), css, flags=re.DOTALL)
with open('assets/styles/components.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Updated data-reveal CSS')
