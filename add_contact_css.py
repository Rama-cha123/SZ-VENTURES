with open('assets/styles/layout.css', 'r', encoding='utf-8') as f:
    css = f.read()

contact_css = '''
/* =========================== CONTACT SECTION =========================== */
.interest-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.interest-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}
.contact-detail {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--line);
}
.cd-label {
  font-family: var(--font-display);
  font-size: var(--fs-300);
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  margin-bottom: 0.5rem;
}
.contact-info a {
  color: var(--ink);
  font-size: var(--fs-500);
  text-decoration: none;
  transition: color 0.3s ease;
}
.contact-info a:hover {
  color: var(--gold-light);
}
@media (max-width: 880px) {
  .interest-grid { grid-template-columns: 1fr; }
  .contact-grid { grid-template-columns: 1fr; gap: 2.5rem; }
}
'''

if '.interest-grid' not in css:
    css += '\n' + contact_css
    with open('assets/styles/layout.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added contact CSS to layout.css')
else:
    print('contact CSS already exists')
