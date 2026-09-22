with open('assets/styles/layout.css', 'r', encoding='utf-8') as f:
    css = f.read()

card_icon_css = '''
.card-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(197, 160, 89, 0.1);
  color: var(--gold);
  border-radius: 50%;
  margin-bottom: 1.25rem;
}
.card-icon svg {
  width: 24px !important;
  height: 24px !important;
  max-width: 24px !important;
  max-height: 24px !important;
  flex-shrink: 0;
}
'''

if '.card-icon' not in css:
    css = css.replace('.principle, .value-card {', card_icon_css + '\n.principle, .value-card {')
    with open('assets/styles/layout.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added .card-icon to layout.css')
else:
    print('.card-icon already exists')
