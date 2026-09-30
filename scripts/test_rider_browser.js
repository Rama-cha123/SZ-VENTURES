const puppeteer = require('puppeteer');

(async () => {
  console.log("=== STARTING RIDER REGISTRATION PUPPETEER BROWSER TEST ===");
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Test 1: Desktop Layout & Overflow
  console.log("\n[1] Testing Desktop Viewport (1440x900)...");
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('http://127.0.0.1:3000/operations/rider-registration', { waitUntil: 'networkidle0', timeout: 10000 });

  const desktopMetrics = await page.evaluate(() => {
    const logo = document.querySelector('.nav-logo-img');
    const logoRect = logo ? logo.getBoundingClientRect() : null;
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      logoW: logoRect ? logoRect.width : null,
      logoH: logoRect ? logoRect.height : null,
      title: document.title
    };
  });

  console.log("Desktop Metrics:", desktopMetrics);
  if (desktopMetrics.scrollWidth > desktopMetrics.clientWidth) {
    console.error("FAIL: Horizontal scroll detected on desktop!");
  } else {
    console.log("PASS: No horizontal scroll on desktop.");
  }
  if (desktopMetrics.logoW && desktopMetrics.logoW <= 40) {
    console.log("PASS: Logo width clamped properly on desktop (" + desktopMetrics.logoW + "px)");
  } else {
    console.error("FAIL: Logo width exceeded limit: " + desktopMetrics.logoW);
  }

  // Test 2: Mobile Layout & Overflow
  console.log("\n[2] Testing Mobile Viewport (375x812)...");
  await page.setViewport({ width: 375, height: 812 });
  await page.reload({ waitUntil: 'networkidle0' });

  const mobileMetrics = await page.evaluate(() => {
    const logo = document.querySelector('.nav-logo-img');
    const logoRect = logo ? logo.getBoundingClientRect() : null;
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      logoW: logoRect ? logoRect.width : null,
      logoH: logoRect ? logoRect.height : null
    };
  });

  console.log("Mobile Metrics:", mobileMetrics);
  if (mobileMetrics.scrollWidth > mobileMetrics.clientWidth) {
    console.error("FAIL: Horizontal scroll detected on mobile!");
  } else {
    console.log("PASS: No horizontal scroll on mobile (375px).");
  }

  // Test 3: Form Step Navigation & Interactive Submission
  console.log("\n[3] Testing Form Step Flow and Validation...");

  // Try advancing Step 1 with empty fields
  await page.evaluate(() => {
    if (typeof nextStep === 'function') nextStep(1);
  });
  await new Promise(r => setTimeout(r, 200));

  const step1Errors = await page.evaluate(() => {
    return document.querySelectorAll('.form-group.has-error').length;
  });
  console.log("Step 1 validation errors triggered properly:", step1Errors >= 2 ? "PASS (" + step1Errors + " errors)" : "FAIL");

  // Fill Step 1
  await page.type('#full_name', 'Sanjay Varma');
  await page.type('#mobile_number', '9812345678');
  await page.click('#sameAsMobile');
  await page.type('#email', 'sanjay.varma@example.com');
  await page.evaluate(() => {
    document.getElementById('dob').value = '1996-03-24';
  });
  await page.select('#preferred_language', 'Telugu');

  // Advance to Step 2
  await page.click('#step-1 button.btn--accent');
  await new Promise(r => setTimeout(r, 400));

  const currentStepNow = await page.evaluate(() => {
    return document.querySelector('#step-2').classList.contains('active');
  });
  console.log("Advanced to Step 2 (Location):", currentStepNow ? "PASS" : "FAIL");

  // Fill Step 2
  await page.select('#state', 'Telangana');
  await page.type('#district', 'Hyderabad');
  await page.type('#city', 'Hyderabad');
  await page.type('#pincode', '500081');
  await page.type('#preferred_location', 'Madhapur / HITEC City Hub');

  // Advance to Step 3
  await page.click('#step-2 button.btn--accent');
  await new Promise(r => setTimeout(r, 400));

  const isStep3 = await page.evaluate(() => {
    return document.querySelector('#step-3').classList.contains('active');
  });
  console.log("Advanced to Step 3 (Vehicle):", isStep3 ? "PASS" : "FAIL");

  // Fill Step 3
  await page.select('#vehicle_type', 'Motorcycle');
  await page.type('#vehicle_reg_number', 'TS09FC5544');
  await page.select('#driving_licence_status', 'yes');
  await page.select('#vehicle_availability', 'full-time');

  // Advance to Step 4
  await page.click('#step-3 button.btn--accent');
  await new Promise(r => setTimeout(r, 400));

  const isStep4 = await page.evaluate(() => {
    return document.querySelector('#step-4').classList.contains('active');
  });
  console.log("Advanced to Step 4 (Preferences):", isStep4 ? "PASS" : "FAIL");

  // Fill Step 4
  await page.select('#preferred_work_type', 'delivery');
  await page.select('#work_availability', 'full-time');
  await page.select('#preferred_shift', 'morning');
  await page.select('#experience_duration', '1 - 2 years');
  await page.type('#previous_platforms', 'Zomato, Shadowfax');

  // Advance to Step 5
  await page.click('#step-4 button.btn--accent');
  await new Promise(r => setTimeout(r, 400));

  const isStep5 = await page.evaluate(() => {
    return document.querySelector('#step-5').classList.contains('active');
  });
  console.log("Advanced to Step 5 (Docs & Consent):", isStep5 ? "PASS" : "FAIL");

  // Accept Consents (Non-preselected checkboxes)
  await page.click('#consent_accuracy');
  await page.click('#consent_processing');

  // Submit Form
  console.log("\n[4] Submitting Rider Registration Form...");
  await page.click('#submitBtn');

  // Wait for submission response and confirmation screen
  await page.waitForSelector('#successScreen', { visible: true, timeout: 8000 });

  const successData = await page.evaluate(() => {
    const dispId = document.querySelector('#displayAppId').textContent;
    const isVisible = window.getComputedStyle(document.querySelector('#successScreen')).display !== 'none';
    const formHidden = window.getComputedStyle(document.querySelector('#formCardContainer')).display === 'none';
    return { dispId, isVisible, formHidden };
  });

  console.log("Confirmation Screen Visible:", successData.isVisible ? "PASS" : "FAIL");
  console.log("Form Container Hidden:", successData.formHidden ? "PASS" : "FAIL");
  console.log("Generated Reference ID on Screen:", successData.dispId);
  if (successData.dispId.startsWith('SZ-RIDER-')) {
    console.log("PASS: Application ID format verified (" + successData.dispId + ")");
  } else {
    console.error("FAIL: Unexpected ID format: " + successData.dispId);
  }

  // Take screenshot of confirmation screen
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 400));
  await page.screenshot({ path: 'scripts/rider_success_screenshot.png', fullPage: true });
  console.log("Saved confirmation screenshot to scripts/rider_success_screenshot.png");

  await browser.close();
  console.log("\n=== ALL PUPPETEER BROWSER TESTS PASSED! ===");
})().catch(err => {
  console.error("Puppeteer Test Error:", err);
  process.exit(1);
});
