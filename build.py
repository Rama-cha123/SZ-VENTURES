import os
import sys

def main():
    config_path = os.path.join('assets', 'js', 'supabase-config.js')
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_ANON_KEY', '')

    if supabase_url and supabase_key:
        print("Injecting Supabase environment variables...")
        content = content.replace('%SUPABASE_URL%', supabase_url)
        content = content.replace('%SUPABASE_ANON_KEY%', supabase_key)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Environment variables injected successfully.")
    else:
        print("Warning: SUPABASE_URL or SUPABASE_ANON_KEY environment variables not found.")

if __name__ == '__main__':
    main()
