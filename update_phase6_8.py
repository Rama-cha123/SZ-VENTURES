with open('assets/styles/components.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Update card img scale from 1.03 to 1.02 and use motion-image var
css = css.replace('transform: scale(1.03);', 'transform: scale(1.02);')
css = css.replace('transition: transform var(--dur-img) var(--ease), filter var(--dur-img) var(--ease);', 
                  'transition: transform var(--motion-image) var(--ease-premium), filter var(--motion-image) var(--ease-premium);')

# Update creator house animation to run once or be more controlled
css = css.replace('animation: creatorSweep 2s infinite linear;', 'animation: creatorSweep 1.5s 1 forwards ease-out;')

# Add Image mask reveal
reveal_css = '''
/* Image Mask Reveal */
img[data-reveal], .reveal-image {
    clip-path: inset(100% 0 0 0);
    transition: clip-path var(--motion-image) var(--ease-premium), opacity var(--motion-reveal) var(--ease-premium);
}
.js img[data-reveal].is-visible, .js .is-visible img[data-reveal], .reveal-image.is-visible {
    clip-path: inset(0 0 0 0);
}
'''
if 'Image Mask Reveal' not in css:
    css += '\n' + reveal_css

with open('assets/styles/components.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated phase 6 and 8 CSS')
