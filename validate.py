import html.parser
class LineTrackerHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.warnings = []

    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'param', 'path', 'svg', 'g', 'polygon', 'circle', 'line', 'rect', 'polyline', 'ellipse', 'use', 'title', 'desc']:
            self.tags.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in ['img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'param', 'path', 'svg', 'g', 'polygon', 'circle', 'line', 'rect', 'polyline', 'ellipse', 'use', 'title', 'desc']:
            return
        
        if not self.tags:
            self.warnings.append(f'Warning: Closing tag </{tag}> without opening tag near line {self.getpos()[0]}')
            return
            
        last_tag, last_line = self.tags.pop()
        
        while last_tag != tag and self.tags:
            self.warnings.append(f'Warning: Mismatched tags. Expected </{last_tag}> (opened at {last_line}), got </{tag}> at line {self.getpos()[0]}')
            last_tag, last_line = self.tags.pop()
            
        if last_tag != tag:
            self.warnings.append(f'Warning: Mismatched tags. Unmatched </{tag}> at line {self.getpos()[0]}')

parser = LineTrackerHTMLParser()
with open('creator-house/index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())

for w in parser.warnings:
    print(w)
if not parser.warnings:
    print('Zero structural warnings!')
