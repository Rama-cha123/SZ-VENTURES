with open('assets/styles/layout.css', 'r', encoding='utf-8') as f:
    css = f.read()

arrow_css = '''
.interest-card__arrow {
  display: block;
  width: 28px;
  height: 28px;
  max-width: 28px;
  max-height: 28px;
  flex: 0 0 28px;
  color: currentColor;
}
.interest-card__arrow path {
  vector-effect: non-scaling-stroke;
}
'''

if '.interest-card__arrow' not in css:
    css += '\n' + arrow_css
    with open('assets/styles/layout.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added arrow css')
