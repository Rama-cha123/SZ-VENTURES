import os
import re

path = r'c:\Data\Projects\Downloads\sz-ventures\about\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the founder bio section
pattern = r'(<div class="founder__bio"[^>]*>)(.*?)(</div>)'

new_bio = """
              <p>Sridhar Chakkravarthy is the Founder of SZ Ventures Private Limited, a venture studio developing businesses across industrial technology and the new economy.</p>
              <p>His professional foundation was built over years of driving operational excellence and enterprise capability across global logistics, aviation, and technology. With a career spanning leadership and operational roles at UPS, InterGlobe Technologies (IndiGo Airlines), and IBM, he developed a rigorous approach to process, quality, and scale.</p>
              <!-- PENDING VERIFIED GLOBAL TRAVEL DATA: Do not add countries until provided by CEO -->
              <p>Transitioning from corporate enterprise to venture building, Sridhar now applies this discipline to the startup ecosystem. At SZ Ventures, he focuses on identifying practical market opportunities and engineering the core technological and commercial infrastructure required to build sustainable businesses.</p>
              <p>He holds an MBA from Warwick Business School and is a certified Six Sigma Master Black Belt.</p>
            """

new_content = re.sub(pattern, r'\1' + new_bio + r'\3', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated about/index.html")
