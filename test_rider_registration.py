import urllib.request
import urllib.error
import json
import uuid
import sys
from datetime import datetime, date

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
BASE_URL = "http://localhost:3000"

def post_json(endpoint, payload, headers=None):
    if headers is None:
        headers = {}
    url = f"{BASE_URL}{endpoint}"
    req_headers = {"Content-Type": "application/json"}
    req_headers.update(headers)
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=req_headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode('utf-8'))
        except Exception:
            body = {"error": str(e)}
        return e.code, body

def get_url(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        return e.code, ""

def run_tests():
    print("==================================================", flush=True)
    print("   SZ VENTURES — RIDER REGISTRATION E2E SUITE     ", flush=True)
    print("==================================================", flush=True)
    
    passed = 0
    failed = 0

    def check(test_name, condition, extra=""):
        nonlocal passed, failed
        if condition:
            print(f"[PASS] {test_name}", flush=True)
            passed += 1
        else:
            print(f"[FAIL] {test_name} - {extra}", flush=True)
            failed += 1

    # 1. Route availability checks
    status, html = get_url("/operations/rider-registration")
    check("Route /operations/rider-registration returns 200", status == 200, f"Got {status}")
    check("Page contains clear CTA title", "RIDER ONBOARDING" in html)
    check("Page contains mandatory disclaimer regarding employment", "does not guarantee employment or immediate deployment" in html)
    check("Page contains Section A, B, C, D, E, F fields", "SECTION A" in html and "SECTION B" in html and "SECTION C" in html and "SECTION D" in html and "SECTION E" in html and "SECTION F" in html)
    check("Consent checkboxes are NOT preselected", 'id="consent_accuracy" name="consent_accuracy" required onclick="event.stopPropagation()">' in html and 'checked' not in html[html.find('id="consent_accuracy"'):html.find('id="consent_accuracy"')+80])

    # 2. Entry points checks
    status_ops, html_ops = get_url("/operations/rider-operations")
    check("Rider Operations page contains CTA link to /operations/rider-registration", "/operations/rider-registration" in html_ops and "RIDER ONBOARDING" in html_ops)

    status_all_ops, html_all_ops = get_url("/operations")
    check("Operations index page contains link to /operations/rider-registration", "/operations/rider-registration" in html_all_ops)

    # 3. Security Checks (Blocked /data/)
    sec_status, _ = get_url("/data/rider_registrations.json")
    check("Direct access to /data/rider_registrations.json is 403 Forbidden", sec_status == 403, f"Got {sec_status}")

    sec_status_uploads, _ = get_url("/data/uploads/rider_documents/somefile.jpg")
    check("Direct access to /data/uploads/ is 403 Forbidden", sec_status_uploads == 403, f"Got {sec_status_uploads}")

    # 4. Valid Registration Submission
    valid_key = str(uuid.uuid4())
    valid_payload = {
        "source": "rider_registration",
        "full_name": "Ravi Teja",
        "mobile_number": "9876543210",
        "whatsapp_number": "9876543210",
        "email": "ravi.teja@example.com",
        "dob": "1997-08-20",
        "preferred_language": "Telugu",
        "state": "Telangana",
        "district": "Hyderabad",
        "city": "Hyderabad",
        "pincode": "500034",
        "preferred_location": "Banjara Hills / Jubilee Hills",
        "willing_nearby": "yes",
        "own_vehicle": "yes",
        "vehicle_type": "Motorcycle",
        "vehicle_reg_number": "TS09EK9988",
        "driving_licence_status": "yes",
        "vehicle_availability": "full-time",
        "preferred_work_type": "delivery",
        "work_availability": "full-time",
        "preferred_shift": "morning",
        "joining_date": "Immediate",
        "has_experience": "yes",
        "experience_duration": "1 - 2 years",
        "previous_platforms": "Swiggy, Blinkit",
        "experience_notes": "Expert in route navigation in Banjara Hills",
        "consent_accuracy": True,
        "consent_contact": True,
        "consent_privacy": True,
        "consent_processing": True
    }

    code, resp = post_json("/api/rider-registration", valid_payload, {"X-Idempotency-Key": valid_key})
    check("Valid submission returns 200 OK", code == 200, f"Got {code} {resp}")
    check("Response contains status 'success'", resp.get("status") == "success")
    app_id = resp.get("application_id") or resp.get("id")
    check("Response returns application ID with SZ-RIDER- prefix", app_id and app_id.startswith("SZ-RIDER-"), f"Got {app_id}")
    check("Application status is initial 'SUBMITTED'", resp.get("application_status") == "SUBMITTED")

    # 5. Idempotent Retry Test
    code_retry, resp_retry = post_json("/api/rider-registration", valid_payload, {"X-Idempotency-Key": valid_key})
    check("Duplicate submission with same idempotency key returns 200 OK", code_retry == 200)
    check("Duplicate submission returns identical application ID", (resp_retry.get("application_id") or resp_retry.get("id")) == app_id)
    check("Duplicate submission message notes cached result", "cached" in resp_retry.get("message", "").lower())

    # 6. Idempotency Conflict (different payload, same key)
    tampered_payload = valid_payload.copy()
    tampered_payload["full_name"] = "Different Name"
    code_conflict, resp_conflict = post_json("/api/rider-registration", tampered_payload, {"X-Idempotency-Key": valid_key})
    check("Mismatched payload with same key returns 400 Idempotency Conflict", code_conflict == 400)

    # 7. Missing Required Field Validation (e.g. missing full_name)
    bad_payload_name = valid_payload.copy()
    bad_payload_name["full_name"] = ""
    code_fn, resp_fn = post_json("/api/rider-registration", bad_payload_name, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Missing full_name returns 400", code_fn == 400 and "Full name" in resp_fn.get("message", ""))

    # 8. Mobile Number Validation
    bad_mobile_payload = valid_payload.copy()
    bad_mobile_payload["mobile_number"] = "12345"
    code_mob, resp_mob = post_json("/api/rider-registration", bad_mobile_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Invalid mobile number format returns 400", code_mob == 400 and "mobile number" in resp_mob.get("message", "").lower())

    # 9. PIN Code Validation
    bad_pin_payload = valid_payload.copy()
    bad_pin_payload["pincode"] = "0123"
    code_pin, resp_pin = post_json("/api/rider-registration", bad_pin_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Invalid PIN code format returns 400", code_pin == 400 and "pin code" in resp_pin.get("message", "").lower())

    # 10. Age Eligibility Validation (< 18 years old)
    bad_age_payload = valid_payload.copy()
    bad_age_payload["dob"] = "2015-01-01"
    code_age, resp_age = post_json("/api/rider-registration", bad_age_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Applicant under 18 years old is rejected with 400", code_age == 400 and "18 years" in resp_age.get("message", ""))

    # 11. Conditional Vehicle Validation
    # Motorized vehicle without registration number
    bad_veh_payload = valid_payload.copy()
    bad_veh_payload["vehicle_type"] = "Motorcycle"
    bad_veh_payload["vehicle_reg_number"] = ""
    code_veh, resp_veh = post_json("/api/rider-registration", bad_veh_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Motorized vehicle without registration number returns 400", code_veh == 400)

    # Bicycle does NOT require registration number
    bicycle_payload = valid_payload.copy()
    bicycle_payload["vehicle_type"] = "Bicycle"
    bicycle_payload["vehicle_reg_number"] = ""
    code_bike, resp_bike = post_json("/api/rider-registration", bicycle_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Bicycle applicant does not require vehicle registration (200 OK)", code_bike == 200)

    # Non-vehicle owner does NOT require vehicle registration
    no_veh_payload = valid_payload.copy()
    no_veh_payload["own_vehicle"] = "no"
    code_noveh, resp_noveh = post_json("/api/rider-registration", no_veh_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Non-vehicle owner can register without vehicle reg number (200 OK)", code_noveh == 200)

    # 12. Mandatory Consent Validation
    # Missing accuracy consent
    bad_consent1 = valid_payload.copy()
    bad_consent1["consent_accuracy"] = False
    code_c1, resp_c1 = post_json("/api/rider-registration", bad_consent1, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked accuracy declaration returns 400", code_c1 == 400 and "accurate" in resp_c1.get("message", "").lower())

    # Missing processing consent
    bad_consent2 = valid_payload.copy()
    bad_consent2["consent_processing"] = False
    bad_consent2["consent_privacy"] = False
    code_c2, resp_c2 = post_json("/api/rider-registration", bad_consent2, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked data processing consent returns 400", code_c2 == 400 and "consent" in resp_c2.get("message", "").lower())

    # Missing contact consent
    bad_consent3 = valid_payload.copy()
    bad_consent3["consent_contact"] = False
    code_c3, resp_c3 = post_json("/api/rider-registration", bad_consent3, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked contact consent returns 400", code_c3 == 400 and "contact" in resp_c3.get("message", "").lower())

    # 13. Optional Document Upload Validation
    # Unsupported file type (.exe)
    bad_doc_payload = valid_payload.copy()
    bad_doc_payload["doc_photo"] = {
        "name": "malicious.exe",
        "mime": "application/x-msdownload",
        "size": 1024,
        "data": "TVqQAAMAAAAEAAAA"
    }
    code_doc, resp_doc = post_json("/api/rider-registration", bad_doc_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unsupported document type is rejected with 400", code_doc == 400 and "unsupported" in resp_doc.get("message", "").lower())

    # Valid Document Upload (.jpg simulated base64)
    import base64
    dummy_jpg = base64.b64encode(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB").decode('utf-8')
    good_doc_payload = valid_payload.copy()
    good_doc_payload["doc_photo"] = {
        "name": "profile.jpg",
        "mime": "image/jpeg",
        "size": 24,
        "data": dummy_jpg
    }
    code_good_doc, resp_good_doc = post_json("/api/rider-registration", good_doc_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Valid document upload succeeds with 200 OK", code_good_doc == 200)

    # 14. Verification of database storage
    with open("data/rider_registrations.json", "r") as f:
        records = json.load(f)
    check("Database contains recorded submissions", len(records) >= 3)
    latest = records[-1]
    check("Latest record has status SUBMITTED", latest.get("status") == "SUBMITTED")
    check("Latest record has ISO timestamp", "timestamp" in latest)
    check("Uploaded document in record does not leak raw base64", "data" not in str(latest.get("doc_photo")))

    print("\n--------------------------------------------------")
    print(f"RESULTS: {passed} PASSED, {failed} FAILED")
    print("==================================================")
    if failed > 0:
        sys.exit(1)
    else:
        print("ALL RIDER REGISTRATION E2E TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
