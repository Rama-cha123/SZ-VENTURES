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

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

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
        if clean_path == '/operations':
            self.path = '/operations/index.html'
            return False
        if clean_path == '/how-we-build':
            self.path = '/how-we-build/index.html'
            return False
        if clean_path == '/contact':
            self.path = '/contact.html'
            return False
        if clean_path == '/portfolio':
            self.path = '/portfolio.html'
            return False
        if clean_path == '/operations/rider-registration':
            self.path = '/operations/rider-registration/index.html'
            return False
            
        local_path = self.translate_path(parsed.path)
        if not os.path.exists(local_path) and not os.path.splitext(local_path)[1]:
            if os.path.isfile(local_path + '.html'):
                self.path = urllib.parse.urlunsplit(parsed._replace(path=parsed.path + '.html'))
            elif os.path.isdir(local_path) and os.path.isfile(os.path.join(local_path, 'index.html')):
                self.path = urllib.parse.urlunsplit(parsed._replace(path=clean_path + '/index.html'))
        elif os.path.isdir(local_path) and os.path.isfile(os.path.join(local_path, 'index.html')) and not parsed.path.endswith('/index.html'):
            self.path = urllib.parse.urlunsplit(parsed._replace(path=clean_path + '/index.html'))
        return False

    def do_POST(self):
        if self.path in ('/api/submit', '/api/rider-registration'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Check for idempotency key
                idem_key = self.headers.get('X-Idempotency-Key')
                if not idem_key:
                    raise ValueError("Missing X-Idempotency-Key header")
                    
                if self.path == '/api/rider-registration':
                    source = 'rider_registration'
                else:
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

                # Backend Validation: Rider Registration
                if source == 'rider_registration':
                    import re
                    # SECTION A: Personal Information
                    required_fields = {
                        'full_name': 'Full name',
                        'mobile_number': 'Mobile number',
                        'dob': 'Date of birth',
                        'state': 'State',
                        'district': 'District',
                        'city': 'City or town',
                        'pincode': 'PIN code',
                        'preferred_location': 'Preferred working location',
                        'willing_nearby': 'Willingness to work in nearby locations',
                        'own_vehicle': 'Vehicle ownership status'
                    }
                    for field_key, field_name in required_fields.items():
                        val = data.get(field_key)
                        if val is None or not str(val).strip():
                            raise ValueError(f"Missing required field: {field_name}")

                    # Validate mobile number: 10 digits starting with 6-9
                    clean_mobile = re.sub(r'[\s\-\+]', '', str(data.get('mobile_number', '')))
                    if clean_mobile.startswith('91') and len(clean_mobile) == 12:
                        clean_mobile = clean_mobile[2:]
                    if not re.match(r'^[6-9]\d{9}$', clean_mobile):
                        raise ValueError("Invalid mobile number. Must be a valid 10-digit Indian mobile number.")
                    data['mobile_number'] = clean_mobile

                    # Optional WhatsApp validation
                    whatsapp = data.get('whatsapp_number')
                    if whatsapp and str(whatsapp).strip():
                        clean_wa = re.sub(r'[\s\-\+]', '', str(whatsapp))
                        if clean_wa.startswith('91') and len(clean_wa) == 12:
                            clean_wa = clean_wa[2:]
                        if not re.match(r'^[6-9]\d{9}$', clean_wa):
                            raise ValueError("Invalid WhatsApp number format. Must be a 10-digit mobile number.")
                        data['whatsapp_number'] = clean_wa

                    # Optional Email validation
                    email = str(data.get('email', '')).strip()
                    if email:
                        if '@' not in email or '.' not in email.split('@')[-1] or len(email) < 5:
                            raise ValueError("Invalid email address format.")
                        data['email'] = email

                    # Validate Date of Birth (Eligibility: Minimum 18 years old)
                    dob_str = str(data.get('dob', '')).strip()
                    try:
                        dob_date = datetime.strptime(dob_str, '%Y-%m-%d')
                        today = datetime.now()
                        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                        if age < 18:
                            raise ValueError("Applicant must be at least 18 years of age to register as a delivery rider.")
                        if age > 75:
                            raise ValueError("Please provide a valid date of birth.")
                    except ValueError as dob_err:
                        if "Applicant must be" in str(dob_err) or "valid date of birth" in str(dob_err):
                            raise
                        raise ValueError("Invalid date of birth format. Expected YYYY-MM-DD.")

                    # SECTION B: Location
                    pincode = str(data.get('pincode', '')).strip()
                    if not re.match(r'^[1-9][0-9]{5}$', pincode):
                        raise ValueError("Invalid PIN code. Must be a valid 6-digit Indian postal code.")
                    data['pincode'] = pincode

                    # SECTION C: Vehicle Information
                    own_vehicle = str(data.get('own_vehicle', '')).strip().lower()
                    if own_vehicle in ('yes', 'true', '1'):
                        data['own_vehicle'] = 'yes'
                        vtype = str(data.get('vehicle_type', '')).strip()
                        if not vtype:
                            raise ValueError("Please select your vehicle type.")
                        data['vehicle_type'] = vtype
                        if vtype.lower() not in ('bicycle', 'cycle'):
                            reg_no = str(data.get('vehicle_reg_number', '')).strip()
                            if not reg_no or len(reg_no) < 4:
                                raise ValueError("Vehicle registration number is required for motorized vehicles.")
                            data['vehicle_reg_number'] = reg_no.upper()
                    else:
                        data['own_vehicle'] = 'no'
                        data['vehicle_reg_number'] = 'Not Applicable'

                    # SECTION E: Document upload validation (optional files)
                    upload_dir = os.path.join(DATA_DIR, "uploads", "rider_documents")
                    os.makedirs(upload_dir, exist_ok=True)
                    allowed_mimes = {'image/jpeg', 'image/png', 'image/webp', 'application/pdf'}
                    doc_fields = ['doc_photo', 'doc_driving_licence', 'doc_rc']
                    for doc_f in doc_fields:
                        doc_val = data.get(doc_f)
                        if doc_val and isinstance(doc_val, dict):
                            mime = doc_val.get('mime', '').lower()
                            size = doc_val.get('size', 0)
                            name = doc_val.get('name', 'document')
                            b64 = doc_val.get('data')
                            if mime and mime not in allowed_mimes:
                                raise ValueError(f"Unsupported file type for {name}: {mime}. Supported: JPG, PNG, WEBP, PDF.")
                            if size > 5 * 1024 * 1024:
                                raise ValueError(f"File {name} exceeds maximum allowed size of 5 MB.")
                            if b64:
                                import base64
                                try:
                                    raw_b = base64.b64decode(b64)
                                    ext = '.pdf' if 'pdf' in mime else ('.png' if 'png' in mime else '.jpg')
                                    safe_name = f"{uuid.uuid4().hex[:12]}_{doc_f}{ext}"
                                    safe_dest = os.path.join(upload_dir, safe_name)
                                    with open(safe_dest, 'wb') as sf:
                                        sf.write(raw_b)
                                    # Never store or expose raw base64 or internal filesystem paths publicly
                                    data[doc_f] = {
                                        'file_name': name,
                                        'mime': mime,
                                        'size_bytes': size,
                                        'stored_file': safe_name,
                                        'status': 'SECURED'
                                    }
                                except Exception as dec_err:
                                    raise ValueError(f"Unable to process file upload for {name}: {str(dec_err)}")

                    # SECTION F: Declaration and Consent (MANDATORY & UNCHECKED BY DEFAULT)
                    consent_acc = data.get('consent_accuracy')
                    if consent_acc not in (True, 'true', '1', 1):
                        raise ValueError("You must confirm that the information provided is accurate.")

                    consent_proc = data.get('consent_processing')
                    if consent_proc not in (True, 'true', '1', 1):
                        raise ValueError("Consent to collection and processing of details for rider onboarding is required.")

                    # Initial Application Status: Strictly SUBMITTED
                    data['status'] = 'SUBMITTED'
                
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
                        past_data.pop('application_id', None)
                        past_data.pop('idempotency_key', None)
                        
                        if json.dumps(past_data, sort_keys=True) == data_hash:
                            # Valid retry, return the original ID
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            ret_id = past_entry.get('id') or past_entry.get('application_id')
                            self.wfile.write(json.dumps({
                                'status': 'success',
                                'message': 'Application received successfully (cached)',
                                'id': ret_id,
                                'application_id': ret_id,
                                'application_status': past_entry.get('status', 'SUBMITTED')
                            }).encode('utf-8'))
                            return
                        else:
                            # Mismatched payload for same key!
                            raise ValueError("Idempotency conflict: key exists with different payload")

                data['timestamp'] = datetime.now().isoformat()
                import random
                if source == 'rider_registration':
                    generated_id = f"SZ-RIDER-{''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=6))}"
                    data['application_id'] = generated_id
                else:
                    generated_id = str(uuid.uuid4())[:8].upper()

                data['id'] = generated_id
                data['idempotency_key'] = idem_key
                file_data.append(data)
                
                with open(filepath, 'w') as f:
                    json.dump(file_data, f, indent=4)

                # Parity storage for rider_registrations.json
                if source == 'rider_registration':
                    alt_filepath = os.path.join(DATA_DIR, "rider_registrations.json")
                    with open(alt_filepath, 'w') as af:
                        json.dump(file_data, af, indent=4)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'message': 'Rider application submitted successfully',
                    'id': generated_id,
                    'application_id': generated_id,
                    'application_status': data.get('status', 'SUBMITTED'),
                    'timestamp': data['timestamp']
                }).encode('utf-8'))
                
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
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    httpd.allow_reuse_address = True
    print(f"Serving at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
