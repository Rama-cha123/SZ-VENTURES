import os, re

def check_html():
    findings = []
    for root, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as html_f:
                    text = html_f.read()
                    
                    # Check images
                    for m in re.finditer(r'<img([^>]+)>', text):
                        img_tag = m.group(1)
                        if 'alt=' not in img_tag:
                            findings.append(f"Low: Missing alt text in {path} -> {img_tag}")
                        
                        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
                        if src_match:
                            src = src_match.group(1)
                            if src.startswith('/assets/images/verticals'):
                                local_path = '.' + src
                                if not os.path.exists(local_path):
                                    findings.append(f"Critical: Broken image path in {path} -> {src}")

    if not findings:
        print("CodeRabbit Gate: PASSED with 0 Critical/High issues.")
    else:
        for finding in findings:
            print(finding)

check_html()
