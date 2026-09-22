css_content = """

/* ==========================================================================
   FOUNDER SECTION (ABOUT PAGE)
   Premium editorial pattern with restrained animations.
   ========================================================================== */

.founder {
    padding: clamp(6rem, 10vw, 10rem) 0;
    background-color: var(--bg-dark);
    color: var(--text-light);
    overflow: hidden;
}

.founder__grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 4rem;
    align-items: center;
}

@media (min-width: 992px) {
    .founder__grid {
        grid-template-columns: 5fr 7fr;
        gap: 6rem;
    }
}

.founder__visual {
    width: 100%;
}

.founder__portrait-frame {
    aspect-ratio: 4/5;
    width: 100%;
    overflow: hidden;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    transition: border-color 0.6s ease;
}

.founder__portrait {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: 50% 30%;
    transition: transform 0.8s cubic-bezier(0.25, 1, 0.5, 1), filter 0.8s ease;
}

/* Hover effect restricted to fine pointer */
@media (hover: hover) and (pointer: fine) {
    .founder__portrait-frame:hover {
        border-color: rgba(212, 175, 55, 0.3); /* Soft gold edge */
    }
    
    .founder__portrait-frame:hover .founder__portrait {
        transform: scale(1.02);
        filter: brightness(1.05);
    }
    
    .founder__link:hover {
        transform: translateY(-2px);
        color: var(--gold-bright);
    }
    
    .founder__link:hover .founder__link-arrow {
        transform: translateX(4px);
    }
}

@media (prefers-reduced-motion: reduce) {
    .founder__portrait,
    .founder__portrait-frame,
    .founder__link,
    .founder__link-arrow {
        transition: none !important;
        transform: none !important;
    }
}

.founder__content {
    display: flex;
    flex-direction: column;
}

.founder__header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.founder__eyebrow {
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: var(--gold);
    text-transform: uppercase;
}

.founder__line {
    flex-grow: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(212, 175, 55, 0.4) 0%, transparent 100%);
    max-width: 120px;
}

.founder__heading {
    font-size: clamp(2rem, 4vw, 3.5rem);
    line-height: 1.1;
    margin-bottom: 3rem;
    color: var(--text-light);
}

.founder__identity {
    margin-bottom: 2.5rem;
}

.founder__name {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 400;
    color: var(--gold);
    margin-bottom: 0.25rem;
}

.founder__role {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 300;
}

.founder__bio {
    font-size: 1.125rem;
    line-height: 1.7;
    color: var(--text-muted);
    margin-bottom: 3rem;
}

.founder__bio p {
    margin-bottom: 1.5rem;
}

.founder__bio p:last-child {
    margin-bottom: 0;
}

.founder__cta-wrap {
    margin-top: 1rem;
}

.founder__link {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--gold);
    text-decoration: none;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
    transition: transform 0.4s ease, color 0.4s ease;
}

.founder__link:focus-visible {
    outline: 2px solid var(--gold);
    outline-offset: 4px;
    border-radius: 2px;
}

.founder__link:active {
    transform: translateY(0);
}

.founder__link-arrow {
    display: inline-block;
    transition: transform 0.4s ease;
}
"""

with open('assets/styles/components.css', 'a', encoding='utf-8') as f:
    f.write(css_content)

print('Updated assets/styles/components.css')
