import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime
import uuid

PORT = 3000
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")

PRODUCT_PRICES = {
    "1": 349,
    "2": 299,
    "3": 399,
    "4": 199,
    "5": 149
}

ALLOWED_EXTENSIONS = {
    '.html', '.css', '.js', '.png', '.jpg', '.webp', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.json'
}

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def check_access(self):
        # Decode path to prevent encoded traversal attacks
        decoded_path = urllib.parse.unquote(self.path).split('?')[0]
        
        # Default to index.html for root
        if decoded_path == '/' or decoded_path == '\\':
            return True
            
        # Check explicit extension allow-list
        _, ext = os.path.splitext(decoded_path)
        if ext and ext.lower() not in ALLOWED_EXTENSIONS:
            return False
            
        # explicitly block data and .env regardless of extension spoofing
        if '/data/' in decoded_path.lower() or '\\data\\' in decoded_path.lower() or '/.env' in decoded_path.lower():
            return False
            
        return True

    def do_GET(self):
        if not self.check_access():
            self.send_error(403, "Forbidden")
            return
        if self.resolve_clean_url():
            return
        super().do_GET()
        
    def do_HEAD(self):
        if not self.check_access():
            self.send_error(403, "Forbidden")
            return
        if self.resolve_clean_url():
            return
        super().do_HEAD()

    def resolve_clean_url(self):
        parsed = urllib.parse.urlsplit(self.path)
        
        # Redirect /index.html to /
        if parsed.path.endswith('/index.html'):
            new_path = parsed.path[:-10]
            if new_path == '':
                new_path = '/'
            if parsed.query:
                new_path += '?' + parsed.query
            self.send_response(301)
            self.send_header('Location', new_path)
            self.end_headers()
            return True
            
        # Special case canonical routes
        clean_path = parsed.path.rstrip('/')
        if clean_path == '/creator-house':
            self.path = '/creator-house/index.html'
            return False
        if clean_path == '/snapops':
            self.path = '/ventures/snapops/index.html'
            return False
        if clean_path == '/about':
            self.path = '/about/index.html'
            return False
        if clean_path == '/ventures':
            self.path = '/ventures/index.html'
            return False
        if clean_path == '/portfolio':
            self.path = '/portfolio.html'
            return False
        local_path = self.translate_path(parsed.path)
        if not os.path.exists(local_path) and not os.path.splitext(local_path)[1]:
            if os.path.isfile(local_path + '.html'):
                self.path = urllib.parse.urlunsplit(parsed._replace(path=parsed.path + '.html'))
        return False

    def do_POST(self):
        if self.path == '/api/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Check for idempotency key
                idem_key = self.headers.get('X-Idempotency-Key')
                if not idem_key:
                    raise ValueError("Missing X-Idempotency-Key header")
                    
                source = data.get('source', 'unknown').replace('/', '_').replace('\\', '_')
                

                # Backend Validation: Partnership Inquiry
                if source == 'partnership_inquiry':
                    required_fields = ['full_name', 'email', 'phone', 'message']
                    for field in required_fields:
                        if not data.get(field) or not str(data.get(field)).strip():
                            raise ValueError(f"Missing required field: {field}")
                    email = str(data.get('email', '')).strip()
                    if '@' not in email or '.' not in email.split('@')[-1]:
                        raise ValueError("Invalid email format")
                    if len(str(data.get('message', ''))) > 5000:
                        raise ValueError("Message exceeds maximum length")

                # Backend Validation: Bowl & Sip Checkout
                if source == 'bowl_and_sip_order':
                    items = data.get('items', [])
                    calculated_subtotal = 0
                    for item in items:
                        item_id = str(item.get('id'))
                        qty = item.get('qty', 1)
                        if item_id in PRODUCT_PRICES:
                            calculated_subtotal += PRODUCT_PRICES[item_id] * qty
                        else:
                            raise ValueError(f"Invalid product ID: {item_id}")
                    
                    calculated_tax = round(calculated_subtotal * 0.05)
                    calculated_delivery = 49
                    calculated_total = calculated_subtotal + calculated_tax + calculated_delivery
                    
                    if int(data.get('total', 0)) != calculated_total:
                        raise ValueError(f"Total mismatch. Client: {data.get('total')}, Server: {calculated_total}")

                    data['subtotal'] = calculated_subtotal
                    data['tax'] = calculated_tax
                    data['total'] = calculated_total
                    data['status'] = 'payment_pending_integration'
                
                filename = f"{source}_data.json"
                filepath = os.path.join(DATA_DIR, filename)
                
                if not os.path.exists(DATA_DIR):
                    os.makedirs(DATA_DIR)
                    
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        try:
                            file_data = json.load(f)
                        except json.JSONDecodeError:
                            file_data = []
                else:
                    file_data = []
                    
                # True Idempotency Check
                data_hash = json.dumps(data, sort_keys=True)
                for past_entry in file_data:
                    if past_entry.get('idempotency_key') == idem_key:
                        past_data = past_entry.copy()
                        past_data.pop('timestamp', None)
                        past_data.pop('id', None)
                        past_data.pop('idempotency_key', None)
                        
                        if json.dumps(past_data, sort_keys=True) == data_hash:
                            # Valid retry, return the original ID
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({'status': 'success', 'message': 'Data saved successfully (cached)', 'id': past_entry.get('id')}).encode('utf-8'))
                            return
                        else:
                            # Mismatched payload for same key!
                            raise ValueError("Idempotency conflict: key exists with different payload")

                data['timestamp'] = datetime.now().isoformat()
                generated_id = str(uuid.uuid4())[:8].upper()
                data['id'] = generated_id
                data['idempotency_key'] = idem_key
                file_data.append(data)
                
                with open(filepath, 'w') as f:
                    json.dump(file_data, f, indent=4)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'message': 'Data saved successfully', 'id': generated_id}).encode('utf-8'))
                
            except ValueError as ve:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(ve)}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    Handler = CustomHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
