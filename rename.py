import os
import glob

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'SZX' in content:
            new_content = content.replace('SZX', 'SZ')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

if __name__ == "__main__":
    for root, dirs, files in os.walk('.'):
        if 'vendor-' in root or '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html') or file.endswith('.js') or file.endswith('.css') or file.endswith('.sql'):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)
    print("Done")
