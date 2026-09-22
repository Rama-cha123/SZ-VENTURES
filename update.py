import sys

html_content = """  <!-- FOUNDER SECTION -->
  <section class="section founder" id="founder">
    <div class="container">
      <div class="founder__grid">
        
        <!-- Visual Column -->
        <div class="founder__visual" data-aos="fade-up" data-aos-duration="900" data-aos-easing="ease-out-cubic">
          <div class="founder__portrait-frame">
            <picture>
              <source srcset="../assets/images/founder/sridhar-chakkravarthy.webp" type="image/webp">
              <img src="../assets/images/founder/sridhar-chakkravarthy.png" alt="Sridhar Chakkravarthy, Founder of SZ Ventures" class="founder__portrait">
            </picture>
          </div>
        </div>

        <!-- Content Column -->
        <div class="founder__content">
          <div class="founder__header" data-aos="fade-up" data-aos-delay="100" data-aos-duration=\"800\">
            <div class="founder__eyebrow">FOUNDER</div>
            <div class="founder__line"></div>
          </div>
          
          <h2 class="founder__heading heading-display" data-aos="fade-up" data-aos-delay="200" data-aos-duration="800">
            THE FOUNDER BEHIND SZ VENTURES.
          </h2>

          <div class="founder__identity" data-aos="fade-up" data-aos-delay="300" data-aos-duration="800">
            <h3 class="founder__name">Sridhar Chakkravarthy</h3>
            <p class="founder__role">Founder — SZ Ventures Private Limited</p>
          </div>

          <div class="founder__bio" data-aos="fade-up" data-aos-delay="400" data-aos-duration="800">
            <p>Sridhar Chakkravarthy is the Founder of SZ Ventures Private Limited, a venture-building company developing businesses across industrial technology and the new economy.</p>
            <p>His experience spans business leadership, operations, quality management and venture development. Before founding SZ Ventures, he held leadership and operational roles across companies including IppoPay, UPS, InterGlobe Technologies and IBM.</p>
            <p>He holds an MBA from Warwick Business School and is a certified Six Sigma Master Black Belt.</p>
            <p>At SZ Ventures, he focuses on identifying practical market opportunities and building the operational, technological and commercial capabilities required to develop sustainable businesses.</p>
          </div>

          <div class="founder__cta-wrap" data-aos="fade-up" data-aos-delay="500" data-aos-duration="800">
            <a href="https://www.linkedin.com/in/sridharchakkravarthy/" target="_blank" rel="noopener noreferrer" class="founder__link">
              CONNECT ON LINKEDIN
              <span class="founder__link-arrow">↗</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

with open('about/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if '<!-- DRAFT PENDING FOUNDER APPROVAL' in line:
        skip = True
        new_lines.append(html_content)
    elif skip and '</main>' in line:
        skip = False
        new_lines.append(line)
    elif not skip:
        new_lines.append(line)

with open('about/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Updated about/index.html')
