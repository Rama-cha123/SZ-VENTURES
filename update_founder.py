with open('about/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change fade-up to fade for the portrait
html = html.replace('data-aos="fade-up" data-aos-duration="900" data-aos-easing="ease-out-cubic"\n          >\n          <div class="founder__portrait-frame">', 
                    'data-aos="fade" data-aos-duration="900" data-aos-easing="ease-out-cubic"\n          >\n          <div class="founder__portrait-frame">')

# Also catch if it's on a single line
html = html.replace('<div class="founder__visual" data-aos="fade-up" data-aos-duration="900"', '<div class="founder__visual" data-aos="fade" data-aos-duration="900"')

with open('about/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated founder portrait entrance')
