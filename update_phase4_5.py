with open('assets/styles/components.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css = '''
/* Phase 4: Gold Divider Animation */
.v-accent-bar {
    display: inline-block;
    position: relative;
}
.v-accent-bar::before {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 1px;
    background: var(--gold);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform var(--motion-reveal) var(--ease-premium);
}
.js .is-visible .v-accent-bar::before, .v-accent-bar.is-visible::before {
    transform: scaleX(1);
}

/* Phase 5: Portfolio Cards */
@media (hover: hover) and (pointer: fine) {
    .portfolio-card {
        transition: transform var(--motion-medium) var(--ease-premium), box-shadow var(--motion-medium) var(--ease-premium), border-color var(--motion-medium) var(--ease-premium);
    }
    .portfolio-card:hover {
        transform: translateY(-4px);
        border-color: var(--gold);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .portfolio-card img {
        transition: transform var(--motion-image) var(--ease-premium);
    }
    .portfolio-card:hover img {
        transform: scale(1.02);
    }
    .portfolio-card .description {
        transition: color var(--motion-medium) var(--ease-premium);
    }
    .portfolio-card:hover .description {
        color: var(--white);
    }
    .portfolio-card:hover .card-cta svg {
        transform: translateX(4px);
    }
}
'''

if 'Phase 4: Gold Divider' not in css:
    css += '\n' + new_css
    with open('assets/styles/components.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added divider and portfolio CSS')
