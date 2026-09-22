import urllib.request
routes = [
    '/', '/contact.html', '/insights.html', '/philosophy.html',
    '/portfolio.html', '/capabilities.html', '/ventures/creator-house/index.html'
]
for r in routes:
    try:
        url = 'http://localhost:3000' + r
        resp = urllib.request.urlopen(url)
        print(f'{r}: {resp.getcode()}')
    except Exception as e:
        print(f'{r}: Error - {e}')
