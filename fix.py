import os

# Read ventures/bowl-and-sip/index.html to get the correct path prefix structure
with open('ventures/bowl-and-sip/index.html', 'r', encoding='utf-8') as f:
    template_lines = f.readlines()

header_lines = []
for line in template_lines:
    if '<a href="../capabilities.html"' in line:
        break
    header_lines.append(line)

# Now fix the meta tags for Creator House
for i, line in enumerate(header_lines):
    if '<title>' in line:
        header_lines[i] = ' <title>Creator House Bengaluru | Creator Production Membership by SZ Ventures</title>\n'
    elif 'name="description"' in line:
        header_lines[i] = ' <meta name="description" content="Creator House by SZ Ventures is a premium production ecosystem in Bengaluru for creators, models, influencers and digital-first talent. Explore membership and production-day access.">\n'
    elif 'rel="canonical"' in line:
        header_lines[i] = ' <link rel="canonical" href="https://szventures.com/creator-house/">\n'
    elif 'og:title' in line:
        header_lines[i] = ' <meta property="og:title" content="Creator House Bengaluru | Creator Production Membership">\n'
    elif 'og:description' in line:
        header_lines[i] = ' <meta property="og:description" content="Creator House by SZ Ventures is a premium production ecosystem in Bengaluru for creators, models, influencers and digital-first talent.">\n'
    elif 'og:url' in line:
        header_lines[i] = ' <meta property="og:url" content="https://szventures.com/creator-house/">\n'

with open('creator-house/index.html', 'r', encoding='utf-8') as f:
    ch_lines = f.readlines()

# ch_lines starts at <a href="../capabilities.html"
new_ch_lines = header_lines + ch_lines

with open('creator-house/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_ch_lines)
print('Fixed!')
