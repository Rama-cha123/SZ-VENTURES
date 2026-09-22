with open('task.md', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('- [ ] **Phase 1: Motion Tokens**', '- [x] **Phase 1: Motion Tokens**')
with open('task.md', 'w', encoding='utf-8') as f:
    f.write(text)
