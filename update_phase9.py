with open('assets/styles/components.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Form focus
css = css.replace('transition: border-color 0.3s var(--ease), box-shadow 0.3s var(--ease);', 
                  'transition: border-color var(--motion-fast) var(--ease-premium), box-shadow var(--motion-fast) var(--ease-premium), outline var(--motion-fast);')

css = css.replace('border-color: var(--gold);\n    box-shadow: 0 0 15px rgba(197, 160, 89, 0.2);',
                  'border-color: var(--gold);\n    box-shadow: 0 0 15px rgba(197, 160, 89, 0.2);\n    outline: 2px solid var(--gold-light);\n    outline-offset: -1px;')

# Interest card
interest_css = '''
/* Phase 9: Contact Interest Cards */
.interest-card {
    transition: border-color var(--motion-medium) var(--ease-premium), box-shadow var(--motion-medium) var(--ease-premium), transform var(--motion-medium) var(--ease-premium);
}
@media (hover: hover) and (pointer: fine) {
    .interest-card:hover {
        border-color: var(--gold);
        box-shadow: 0 8px 24px rgba(220, 180, 110, 0.08);
        transform: translateY(-2px);
    }
}
'''
if 'Phase 9' not in css:
    css += '\n' + interest_css

with open('assets/styles/components.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Updated phase 9 CSS')
