with open('C:/Users/abdul/.gemini/antigravity-ide/brain/034e8756-ed45-4f83-b685-e282d5a25a8c/task.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('[ ]', '[x]')

with open('C:/Users/abdul/.gemini/antigravity-ide/brain/034e8756-ed45-4f83-b685-e282d5a25a8c/task.md', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated tasks')
