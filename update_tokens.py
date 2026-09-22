with open('assets/styles/tokens.css', 'r', encoding='utf-8') as f:
    css = f.read()

motion_vars = '''
  /* Premium Motion Refinement Tokens */
  --motion-fast: 200ms;
  --motion-medium: 350ms;
  --motion-reveal: 650ms;
  --motion-image: 850ms;
  --ease-premium: cubic-bezier(0.22, 1, 0.36, 1);
'''

if '--motion-fast' not in css:
    css = css.replace(':root {', ':root {\n' + motion_vars)
    with open('assets/styles/tokens.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added motion tokens')
else:
    print('Motion tokens exist')
