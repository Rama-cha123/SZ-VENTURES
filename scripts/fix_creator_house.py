import re
import os

path = r'c:\Data\Projects\Downloads\sz-ventures\creator-house\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace CTAs
# Header CTA
content = content.replace(
    '<a href="/contact.html?intent=creator-house" class="hidden md:inline-flex px-6 py-2.5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm hover:bg-ch-gold-light transition-colors">',
    '<button type="button" class="ch-modal-trigger hidden md:inline-flex px-6 py-2.5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm hover:bg-ch-gold-light transition-colors" data-intent="creator_membership">'
)
content = content.replace(
    'CLAIM EARLY-BIRD ACCESS\n    </a>',
    'CLAIM EARLY-BIRD ACCESS\n    </button>'
)

# Mobile Menu CTA
content = content.replace(
    '<a href="/contact.html?intent=creator-house" class="block text-center px-6 py-3 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm">',
    '<button type="button" class="ch-modal-trigger block w-full text-center px-6 py-3 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-sm" data-intent="creator_membership">'
)

# Hero CTA
content = content.replace(
    '<a href="/contact.html?intent=creator-house" class="px-8 py-4 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-base hover:bg-ch-gold-light transition-all shadow-[0_0_20px_rgba(224,173,79,0.3)] hover:scale-105">',
    '<button type="button" class="ch-modal-trigger px-8 py-4 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-base hover:bg-ch-gold-light transition-all shadow-[0_0_20px_rgba(224,173,79,0.3)] hover:scale-105" data-intent="creator_membership">'
)

# Pricing CTA
content = content.replace(
    '<a href="/contact.html?intent=creator-house" class="inline-flex items-center justify-center w-full md:w-auto px-12 py-5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-lg hover:bg-ch-gold-light hover:scale-105 transition-all shadow-[0_0_30px_rgba(224,173,79,0.25)]">',
    '<button type="button" class="ch-modal-trigger inline-flex items-center justify-center w-full md:w-auto px-12 py-5 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-lg hover:bg-ch-gold-light hover:scale-105 transition-all shadow-[0_0_30px_rgba(224,173,79,0.25)]" data-intent="creator_membership">'
)
content = content.replace(
    'CLAIM EARLY-BIRD MEMBERSHIP\n     </a>',
    'CLAIM EARLY-BIRD MEMBERSHIP\n     </button>'
)

# 2. Append Modal HTML and JS before closing </body>
modal_html = """
 <!-- INTAKE MODAL FOR CREATOR HOUSE -->
 <div id="ch-modal" class="fixed inset-0 z-[10000] hidden items-center justify-center p-4 sm:p-6" role="dialog" aria-modal="true">
  <!-- Backdrop -->
  <div id="ch-modal-backdrop" class="absolute inset-0 bg-ch-bg-deep/90 backdrop-blur-sm transition-opacity"></div>
  
  <!-- Modal Content -->
  <div class="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto bg-ch-surface border border-ch-gold/30 rounded-2xl shadow-[0_0_50px_rgba(224,173,79,0.15)] p-6 md:p-10 z-10" id="ch-modal-content" tabindex="-1">
   
   <button type="button" id="ch-modal-close" class="absolute top-4 right-4 md:top-6 md:right-6 w-10 h-10 flex items-center justify-center rounded-full bg-ch-bg-deep border border-ch-line-soft text-ch-gold hover:bg-ch-surface-hover hover:border-ch-gold transition-colors focus:outline-none focus:ring-2 focus:ring-ch-gold/50" aria-label="Close modal">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
   </button>
   
   <h3 id="ch-modal-title" class="font-display font-bold text-2xl md:text-3xl text-ch-text mb-8 tracking-tight">Creator House Request</h3>
   
   <form id="ch-form" class="space-y-6">
    <input type="hidden" id="ch_intent" name="intent" value="">
    
    <div>
     <label for="ch_name" class="block text-sm font-medium text-ch-muted mb-2">Full Name *</label>
     <input type="text" id="ch_name" name="name" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all">
    </div>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
     <div>
      <label for="ch_email" class="block text-sm font-medium text-ch-muted mb-2">Email *</label>
      <input type="email" id="ch_email" name="email" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all">
     </div>
     <div>
      <label for="ch_phone" class="block text-sm font-medium text-ch-muted mb-2">Phone Number *</label>
      <input type="tel" id="ch_phone" name="phone" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all">
     </div>
    </div>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
     <div>
      <label for="ch_city" class="block text-sm font-medium text-ch-muted mb-2">City *</label>
      <input type="text" id="ch_city" name="city" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all">
     </div>
     <div>
      <label for="ch_category" class="block text-sm font-medium text-ch-muted mb-2">Creator Category *</label>
      <select id="ch_category" name="category" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all appearance-none">
       <option value="" disabled selected>Select Category</option>
       <option value="fashion">Fashion</option>
       <option value="beauty">Beauty</option>
       <option value="fitness">Fitness</option>
       <option value="food">Food</option>
       <option value="ugc">UGC</option>
       <option value="podcast">Podcasts & Interviews</option>
       <option value="personal_brand">Personal Branding</option>
       <option value="product">Product & Brand</option>
       <option value="other">Other</option>
      </select>
     </div>
    </div>
    
    <div>
     <label for="ch_link" class="block text-sm font-medium text-ch-muted mb-2">Instagram, YouTube or Portfolio Link *</label>
     <input type="url" id="ch_link" name="portfolio_link" required class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all">
    </div>
    
    <div>
     <label for="ch_message" class="block text-sm font-medium text-ch-muted mb-2">Message or Production Requirement</label>
     <textarea id="ch_message" name="message" rows="3" class="w-full bg-ch-bg-deep border border-ch-line-soft rounded-lg px-4 py-3 text-ch-text placeholder-ch-soft focus:outline-none focus:ring-2 focus:ring-ch-gold/50 focus:border-ch-gold/50 transition-all resize-y"></textarea>
    </div>
    
    <div class="flex items-start gap-3">
     <input type="checkbox" id="ch_consent" name="consent" required class="mt-1 h-4 w-4 rounded border-ch-line-soft bg-ch-bg-deep text-ch-gold focus:ring-ch-gold/50">
     <label for="ch_consent" class="text-xs text-ch-soft leading-relaxed">
      I consent to SZ Ventures processing my information to evaluate my application and contact me regarding Creator House. I understand this does not guarantee membership.
     </label>
    </div>
    
    <div class="pt-4 border-t border-ch-line-soft">
     <button type="submit" id="ch_submit_btn" class="w-full flex items-center justify-center px-8 py-4 rounded-full bg-ch-gold text-ch-bg-deep font-display font-bold text-base hover:bg-ch-gold-light transition-all focus:outline-none focus:ring-4 focus:ring-ch-gold/30">
      <span>Submit Request</span>
     </button>
    </div>
    
    <div id="ch_form_msg" class="text-center text-sm font-medium min-h-[1.5rem]" aria-live="polite"></div>
   </form>
  </div>
 </div>

 <script>
  (function() {
   const modal = document.getElementById('ch-modal');
   const backdrop = document.getElementById('ch-modal-backdrop');
   const closeBtn = document.getElementById('ch-modal-close');
   const form = document.getElementById('ch-form');
   const intentInput = document.getElementById('ch_intent');
   const title = document.getElementById('ch-modal-title');
   const submitBtn = document.getElementById('ch_submit_btn');
   const msgBox = document.getElementById('ch_form_msg');
   const content = document.getElementById('ch-modal-content');
   let lastFocus = null;

   const titles = {
    'creator_membership': 'Join Creator House',
    'membership_details': 'Request Membership Details',
    'founding_membership': 'Apply for Founding Membership',
    'creator_house_information': 'Request More Information'
   };

   function openModal(triggerElement, intentValue) {
    lastFocus = triggerElement;
    intentInput.value = intentValue || 'creator_membership';
    title.textContent = titles[intentInput.value] || 'Creator House Request';
    msgBox.textContent = '';
    msgBox.className = 'text-center text-sm font-medium min-h-[1.5rem]';
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
    
    // Slight delay to allow display to apply before focus
    setTimeout(() => {
     content.focus();
    }, 50);
   }

   function closeModal() {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
   }

   document.querySelectorAll('.ch-modal-trigger').forEach(btn => {
    btn.addEventListener('click', (e) => {
     e.preventDefault();
     openModal(btn, btn.getAttribute('data-intent'));
    });
   });

   closeBtn.addEventListener('click', closeModal);
   backdrop.addEventListener('click', closeModal);

   window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
     closeModal();
    }
   });

   if (form) {
    form.addEventListener('submit', async (e) => {
     e.preventDefault();
     if (submitBtn.disabled) return;
     
     const payload = {
      form_type: 'creator_house',
      intent: intentInput.value,
      name: document.getElementById('ch_name').value,
      email: document.getElementById('ch_email').value,
      phone: document.getElementById('ch_phone').value,
      city: document.getElementById('ch_city').value,
      category: document.getElementById('ch_category').value,
      portfolio_link: document.getElementById('ch_link').value,
      message: document.getElementById('ch_message').value,
      consent: document.getElementById('ch_consent').checked
     };

     submitBtn.disabled = true;
     const btnSpan = submitBtn.querySelector('span');
     btnSpan.textContent = 'Submitting...';
     msgBox.textContent = '';
     
     // Generate idempotency key for this submission
     const idempotencyKey = crypto.randomUUID ? crypto.randomUUID() : Date.now().toString();

     try {
      let success = false;
      if (typeof window.submitData === 'function') {
       await window.submitData(payload);
       success = true;
      } else {
       const response = await fetch('/api/submit', {
        method: 'POST',
        headers: { 
         'Content-Type': 'application/json',
         'X-Idempotency-Key': idempotencyKey
        },
        body: JSON.stringify(payload)
       });
       if (response.ok) { success = true; }
      }
      
      if (success) {
       msgBox.className = 'text-center text-sm font-medium min-h-[1.5rem] text-green-400';
       msgBox.textContent = 'Request submitted successfully. We will be in touch.';
       form.reset();
      } else {
       throw new Error('Failed to submit');
      }
     } catch (err) {
      msgBox.className = 'text-center text-sm font-medium min-h-[1.5rem] text-ch-coral';
      msgBox.textContent = 'An error occurred. Please try again.';
      console.error(err);
     } finally {
      submitBtn.disabled = false;
      btnSpan.textContent = 'Submit Request';
     }
    });
   }
  })();
 </script>
"""

if '<!-- INTAKE MODAL FOR CREATOR HOUSE -->' not in content:
    content = content.replace('</body>', modal_html + '\n</body>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed CTAs and appended modal logic.")
