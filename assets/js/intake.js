function initForms() {
    const partnerForm = document.getElementById('partnerForm');
    if (!partnerForm) return;

    // Prevent duplicate initialization
    if (partnerForm.getAttribute('data-intake-initialized') === 'true') return;
    partnerForm.setAttribute('data-intake-initialized', 'true');

    // Store idempotency key on the form so it persists across retries
    // but can be cleared after a successful submission.
    let idempotencyKey = crypto.randomUUID();
    let currentPayloadHash = '';

    partnerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btn = partnerForm.querySelector('button[type="submit"]');
        if (btn.disabled) return;
        
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span>Submitting...</span>';
        btn.disabled = true;

        const formData = new FormData(partnerForm);
        const data = Object.fromEntries(formData.entries());
        data.source = 'partnership_inquiry';
        
        // Handle multiple checkboxes/selects correctly
        for (const [key, value] of formData.entries()) {
            const allValues = formData.getAll(key);
            if (allValues.length > 1) {
                data[key] = allValues;
            }
        }

        // Check if the payload changed. If it did, generate a new UUID.
        const newPayloadHash = JSON.stringify(data);
        if (newPayloadHash !== currentPayloadHash) {
            idempotencyKey = crypto.randomUUID();
            currentPayloadHash = newPayloadHash;
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        try {
            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Idempotency-Key': idempotencyKey
                },
                body: JSON.stringify(data),
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            
            let result;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                result = await response.json();
            } else {
                throw new Error("Server returned an invalid response type.");
            }

            if (response.ok) {
                // Success
                const statusSpan = document.createElement('span');
                statusSpan.textContent = 'Successfully Submitted ✓';
                statusSpan.setAttribute('aria-live', 'polite');
                btn.innerHTML = '';
                btn.appendChild(statusSpan);
                
                partnerForm.reset();
                // Clear the UUID and hash so the next submission is treated as new
                idempotencyKey = crypto.randomUUID();
                currentPayloadHash = '';

                setTimeout(() => {
                    btn.innerHTML = originalText;
                }, 3000);
            } else {
                throw new Error(result.message || 'Submission failed');
            }
        } catch (error) {
            console.error('Submission error:', error);
            const errorMsg = error.name === 'AbortError' ? 'Request timed out' : error.message;
            
            const errorSpan = document.createElement('span');
            errorSpan.textContent = `Error: ${errorMsg}`;
            errorSpan.setAttribute('aria-live', 'assertive');
            btn.innerHTML = '';
            btn.appendChild(errorSpan);
            
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 4000);
        } finally {
            setTimeout(() => {
                btn.disabled = false;
            }, 4000);
        }
    });
}

// Initial load
document.addEventListener('DOMContentLoaded', initForms);

