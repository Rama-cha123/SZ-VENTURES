import os
import sys

def main():
    template_path = os.path.join('assets', 'js', 'supabase-config.js')
    output_path = os.path.join('assets', 'js', 'supabase-config.generated.js')
    
    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        sys.exit(1)
        
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip()

    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_ANON_KEY', '')

    if supabase_url and supabase_key:
        print("Injecting Supabase environment variables into generated config...")
        content = content.replace('%SUPABASE_URL%', supabase_url)
        content = content.replace('%SUPABASE_ANON_KEY%', supabase_key)
    else:
        if '--production' in sys.argv:
            print("ERROR: Production build requires SUPABASE_URL and SUPABASE_ANON_KEY.")
            sys.exit(1)
        print("Warning: SUPABASE_URL or SUPABASE_ANON_KEY environment variables not found.")
        print("Generated config will retain placeholder values.")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Configuration written to {output_path}.")

if __name__ == '__main__':
    main()
