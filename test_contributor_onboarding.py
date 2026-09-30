import urllib.request
import urllib.error
import json
import uuid
import sys
import os

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
    print("   SZ VENTURES — CONTRIBUTOR ONBOARDING E2E SUITE ", flush=True)
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
    status_clean, html_clean = get_url("/contributor-onboarding")
    check("Route /contributor-onboarding returns 200", status_clean == 200, f"Got {status_clean}")

    status_ops, html_ops = get_url("/operations/contributor-onboarding")
    check("Route /operations/contributor-onboarding returns 200", status_ops == 200, f"Got {status_ops}")

    # 2. Page Content & Copy Integrity
    check("Page has correct Title and Pill", "SZ VENTURES — AI / ROBOTICS CONTRIBUTOR" in html_clean)
    check("Page has required subtitle", "HELP CAPTURE REAL-WORLD WORK" in html_clean)
    check("Page has required description", "paid contributor opportunity. You don't need to know AI. We need people who already work in real-world environments. Takes about 2–3 minutes." in html_clean)
    check("Page has no-guarantee disclaimer", "does not guarantee selection, assignment, or payment" in html_clean)

    # 3. All 6 Sections present
    for sec_num, sec_title in [
        (1, "SECTION 1 — About You"),
        (2, "SECTION 2 — Your Work"),
        (3, "SECTION 3 — Your Workplace"),
        (4, "SECTION 4 — Your Work & Experience"),
        (5, "SECTION 5 — Participation"),
        (6, "SECTION 6 — Final & Consent"),
    ]:
        check(f"Form contains {sec_title}", sec_title in html_clean)

    # 4. Mandatory Consent Statements present in HTML
    check("Consent 1: Information correct", "I confirm that the information provided by me is correct." in html_clean)
    check("Consent 2: Contact consent", "I agree that SZ Ventures may contact me regarding AI/robotics contributor opportunities." in html_clean)
    check("Consent 3: Recording and privacy consent", "I understand that participation in recording activities is subject to workplace permission, applicable safety requirements, and the project-specific consent process. I understand that submitting this form does not guarantee selection or payment." in html_clean)
    check("Submit button copy is accurate", "Submit Contributor Application" in html_clean)

    # 5. Success message copy in HTML
    expected_success = "Thank you for your interest in the SZ Ventures AI & Robotics Contributor Program. Our team will contact shortlisted contributors."
    check("Success card contains exact specified message", expected_success in html_clean)

    # 6. Security Check
    status_sec, _ = get_url("/data/contributor_applications.json")
    check("Direct access to /data/contributor_applications.json is 403 Forbidden", status_sec == 403, f"Got {status_sec}")

    # 7. Valid Application Submission Test
    valid_key = str(uuid.uuid4())
    valid_payload = {
        "source": "ai_robotics_contributor",
        "full_name": "Arjun Verma",
        "mobile_number": "9876543211",
        "whatsapp_number": "9876543211",
        "same_as_mobile": True,
        "is_18_or_older": "Yes",
        "area": "Peenya Industrial Area",
        "work_type": "Metal Work / Fabrication",
        "work_type_other": "",
        "job_role": "Welder",
        "work_location": "Workshop",
        "work_location_other": "",
        "workplace_name": "Precision Fab Works",
        "city": "Bengaluru",
        "owner_aware": "Yes",
        "can_get_permission": "Yes",
        "work_description": "I weld steel frames and structural metal assemblies.",
        "experience_duration": "3–5 years",
        "work_frequency": "Every day",
        "interested_in_recording": "Yes",
        "start_timeline": "Within 7 days",
        "daily_hours": "2–4 hours",
        "comfortable_with_guidelines": "Yes",
        "preferred_contact_method": "WhatsApp",
        "how_heard": "Friend/Referral",
        "how_heard_other": "",
        "consent_accuracy": True,
        "consent_contact": True,
        "consent_recording_privacy": True
    }

    code, resp = post_json("/api/submit", valid_payload, {"X-Idempotency-Key": valid_key})
    check("Valid submission returns 200 OK", code == 200, f"Got {code} {resp}")
    check("Response status is 'success'", resp.get("status") == "success")
    app_id = resp.get("application_id") or resp.get("id")
    check("Response ID has prefix SZ-AIROBOT-", app_id and app_id.startswith("SZ-AIROBOT-"), f"Got {app_id}")
    check("Response returns exact success message", resp.get("message") == expected_success)
    check("Status is 'SUBMITTED'", resp.get("application_status") == "SUBMITTED")

    # 8. Idempotency test (same key + same payload)
    code_retry, resp_retry = post_json("/api/submit", valid_payload, {"X-Idempotency-Key": valid_key})
    check("Duplicate submission with same idempotency key returns 200 OK", code_retry == 200)
    check("Duplicate submission returns identical application ID", (resp_retry.get("application_id") or resp_retry.get("id")) == app_id)

    # 9. Idempotency conflict test
    tampered = valid_payload.copy()
    tampered["full_name"] = "Different Name"
    code_conflict, resp_conflict = post_json("/api/submit", tampered, {"X-Idempotency-Key": valid_key})
    check("Mismatched payload with same key returns 400 conflict", code_conflict == 400)

    # 10. Dedicated endpoint /api/contributor-onboarding test
    code_ded, resp_ded = post_json("/api/contributor-onboarding", valid_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Dedicated endpoint /api/contributor-onboarding returns 200 OK", code_ded == 200)
    ded_id = resp_ded.get("application_id") or resp_ded.get("id")
    check("Dedicated endpoint also generates SZ-AIROBOT- ID", ded_id and ded_id.startswith("SZ-AIROBOT-"))

    # 11. Age Eligibility Restriction (< 18)
    underage_payload = valid_payload.copy()
    underage_payload["is_18_or_older"] = "No"
    code_age, resp_age = post_json("/api/submit", underage_payload, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Under 18 applicant is rejected with 400", code_age == 400 and "18 years" in resp_age.get("message", ""))

    # 12. Missing Required Fields
    for field, label in [("full_name", "Full name"), ("mobile_number", "mobile"), ("area", "area"), ("city", "City")]:
        bad_f = valid_payload.copy()
        bad_f[field] = ""
        code_bf, resp_bf = post_json("/api/submit", bad_f, {"X-Idempotency-Key": str(uuid.uuid4())})
        check(f"Missing {label} returns 400", code_bf == 400)

    # 13. Conditional Other validation
    other_wt_bad = valid_payload.copy()
    other_wt_bad["work_type"] = "Other"
    other_wt_bad["work_type_other"] = ""
    code_owt, resp_owt = post_json("/api/submit", other_wt_bad, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Selecting Other without specifying work type returns 400", code_owt == 400)

    other_loc_bad = valid_payload.copy()
    other_loc_bad["work_location"] = "Other"
    other_loc_bad["work_location_other"] = ""
    code_oloc, resp_oloc = post_json("/api/submit", other_loc_bad, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Selecting Other without specifying work location returns 400", code_oloc == 400)

    # 14. Mandatory Consent Checkboxes Verification
    bad_c1 = valid_payload.copy()
    bad_c1["consent_accuracy"] = False
    code_c1, resp_c1 = post_json("/api/submit", bad_c1, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked accuracy declaration returns 400", code_c1 == 400 and "correct" in resp_c1.get("message", "").lower())

    bad_c2 = valid_payload.copy()
    bad_c2["consent_contact"] = False
    code_c2, resp_c2 = post_json("/api/submit", bad_c2, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked contact consent returns 400", code_c2 == 400 and "contact" in resp_c2.get("message", "").lower())

    bad_c3 = valid_payload.copy()
    bad_c3["consent_recording_privacy"] = False
    code_c3, resp_c3 = post_json("/api/submit", bad_c3, {"X-Idempotency-Key": str(uuid.uuid4())})
    check("Unchecked recording & privacy consent returns 400", code_c3 == 400 and "privacy" in resp_c3.get("message", "").lower())

    # 15. Storage Verification
    data_file = "data/contributor_applications.json"
    check("data/contributor_applications.json was created", os.path.exists(data_file))
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            records = json.load(f)
        check("Storage file contains records", len(records) >= 2)
        latest = records[-1]
        check("Latest record has SZ-AIROBOT- ID", latest.get("id", "").startswith("SZ-AIROBOT-"))
        check("Latest record has SUBMITTED status", latest.get("status") == "SUBMITTED")
        check("Latest record has timestamp", "timestamp" in latest)
        check("Latest record has all 3 consents recorded as True", 
              latest.get("consent_accuracy") is True and 
              latest.get("consent_contact") is True and 
              latest.get("consent_recording_privacy") is True)

    print("\n--------------------------------------------------")
    print(f"RESULTS: {passed} PASSED, {failed} FAILED")
    print("==================================================")
    if failed > 0:
        sys.exit(1)
    else:
        print("ALL CONTRIBUTOR ONBOARDING E2E TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
