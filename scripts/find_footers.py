import os

directory = r"c:\Data\Projects\Downloads\sz-ventures"
for root, dirs, files in os.walk(directory):
    if 'vendor' in root or '.agents' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if '<h4>Ventures</h4>' in content:
                        print(path)
            except:
                pass
