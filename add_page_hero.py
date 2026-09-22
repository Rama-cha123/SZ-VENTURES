with open('assets/styles/layout.css', 'r', encoding='utf-8') as f:
    css = f.read()

page_hero_css = '''
/* =========================== PAGE HERO SECTION =========================== */
.page-hero {
  position: relative;
  padding-top: calc(var(--header-h) + 6rem);
  padding-bottom: 3rem;
  overflow: hidden;
}
'''

if '.page-hero' not in css:
    css = css.replace('/* =========================== HERO SECTION =========================== */', page_hero_css + '\n/* =========================== HERO SECTION =========================== */')
    with open('assets/styles/layout.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added .page-hero to layout.css')
else:
    print('.page-hero already exists')
