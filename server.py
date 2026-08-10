import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = 8000
DATA_DIR = "data"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming JSON
                data = json.loads(post_data.decode('utf-8'))
                
                # Determine source and target file
                source = data.get('source', 'unknown').replace('/', '_').replace('\\', '_')
                filename = f"{source}_data.json"
                filepath = os.path.join(DATA_DIR, filename)
                
                # Create data dir if not exists
                if not os.path.exists(DATA_DIR):
                    os.makedirs(DATA_DIR)
                    
                # Load existing data    
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        try:
                            file_data = json.load(f)
                        except json.JSONDecodeError:
                            file_data = []
                else:
                    file_data = []
                    
                # Append new data with timestamp
                data['timestamp'] = datetime.now().isoformat()
                file_data.append(data)
                
                # Write back
                with open(filepath, 'w') as f:
                    json.dump(file_data, f, indent=4)
                    
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'message': 'Data saved successfully'}).encode('utf-8'))
                
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
    # Allow address reuse so restarting server is quick
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
