with open('assets/styles/components.css', 'r', encoding='utf-8') as f:
    css = f.read()

nav_active_css = '''
  .nav-link.is-active, .nav__link.is-active {
    color: var(--white);
  }
  .nav-link.is-active::after, .nav__link.is-active::after {
    transform: scaleX(1);
  }
  .nav-link:focus-visible, .nav__link:focus-visible,
  .btn:focus-visible, .btn-primary:focus-visible, .btn-secondary:focus-visible, .btn-ghost:focus-visible {
    outline: 2px solid var(--gold);
    outline-offset: 4px;
  }
'''

if 'nav-link.is-active' not in css:
    css = css.replace('.nav-link::after, .nav__link::after {', nav_active_css + '\n.nav-link::after, .nav__link::after {')
    with open('assets/styles/components.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added nav active CSS')
else:
    print('Nav active CSS already exists')
