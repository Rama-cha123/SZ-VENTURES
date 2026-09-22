import urllib.request
import urllib.error
import json
import uuid
import sys
import subprocess
import time
import os
import signal

def check_url(url, method="GET", headers={}, data=None):
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8')) if response.getheader('Content-Type') == 'application/json' else response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8')) if e.getheader('Content-Type') == 'application/json' else e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

print("Starting server.py in background...")
server_proc = subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2) # wait for server to start

try:
    print("--- SECURITY TESTS ---")
    code, body = check_url("http://localhost:3000/.env")
    assert code == 403, f"Expected 403 for .env, got {code}"
    
    code, body = check_url("http://localhost:3000/%2e%65%6e%76")
    assert code == 403, f"Expected 403 for encoded .env, got {code}"
    
    print("--- FORM SUBMISSION TESTS ---")
    idem_key = str(uuid.uuid4())
    headers = {"Content-Type": "application/json", "X-Idempotency-Key": idem_key}
    
    payload = {
        "source": "bowl_and_sip_order",
        "items": [{"id": "1", "qty": 1}],
        "total": 349 + round(349*0.05) + 49
    }
    
    code, body = check_url("http://localhost:3000/api/submit", method="POST", headers=headers, data=payload)
    assert code == 200, f"Expected 200 for checkout, got {code}"
    original_id = body.get('id')
    assert original_id, "Missing ID in response"
    
    code, body2 = check_url("http://localhost:3000/api/submit", method="POST", headers=headers, data=payload)
    assert code == 200, f"Expected 200 for duplicate checkout, got {code}"
    assert body2.get('id') == original_id, f"Expected ID {original_id}, got {body2.get('id')}"
    
    payload_mismatch = payload.copy()
    payload_mismatch["total"] = 9999
    code, body3 = check_url("http://localhost:3000/api/submit", method="POST", headers=headers, data=payload_mismatch)
    assert code == 400, f"Expected 400 for mismatched payload, got {code}"
    
    idem_key_bad = str(uuid.uuid4())
    headers_bad = {"Content-Type": "application/json", "X-Idempotency-Key": idem_key_bad}
    payload_bad = payload.copy()
    payload_bad["total"] = 100
    code, body4 = check_url("http://localhost:3000/api/submit", method="POST", headers=headers_bad, data=payload_bad)
    assert code == 400, f"Expected 400 for spoofed total, got {code}"
    
    print("Restarting server...")
    server_proc.kill()
    server_proc.wait()
    time.sleep(1)
    
    server_proc2 = subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    # After restart, same key should return original ID
    code, body5 = check_url("http://localhost:3000/api/submit", method="POST", headers=headers, data=payload)
    assert code == 200, f"Expected 200 for duplicate after restart, got {code}"
    assert body5.get('id') == original_id, f"Expected ID {original_id}, got {body5.get('id')} after restart"
    
    # New identical order with new key
    idem_key_new = str(uuid.uuid4())
    headers_new = {"Content-Type": "application/json", "X-Idempotency-Key": idem_key_new}
    code, body6 = check_url("http://localhost:3000/api/submit", method="POST", headers=headers_new, data=payload)
    assert code == 200, f"Expected 200 for legitimate new identical order, got {code}"
    assert body6.get('id') != original_id, "New identical order should get a new ID"
    
    print("Checking persistence file...")
    import os
    file_path = "data/bowl_and_sip_order_data.json"
    assert os.path.exists(file_path), "Data file not found"
    with open(file_path, 'r') as f:
        data = json.load(f)
        orders = [x for x in data if x.get('idempotency_key') == idem_key]
        assert len(orders) == 1, f"Expected exactly 1 order with key {idem_key}, found {len(orders)}"
        
    print("ALL TESTS PASSED")
    
finally:
    try:
        server_proc.kill()
    except:
        pass
    try:
        server_proc2.kill()
    except:
        pass
