import docx, os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out = r'C:\Users\26370\Desktop\医院挂号导诊平台-课设文档'

# Verify doc 8 specifically
doc = docx.Document(os.path.join(out, '8个人总结.docx'))

print('=== Doc 8: Paragraphs with text ===')
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t:
        print(f'P{i}: {t[:180]}')
print()

print('=== Doc 8: Table 0 (document list) ===')
t0 = doc.tables[0]
for ri, row in enumerate(t0.rows):
    cells = [c.text[:80] for c in row.cells]
    print(f'  Row{ri}: {" | ".join(cells)}')
print()

# Also quick check all docs are clean
for fname in ['5详细设计说明书.docx','6软件测试计划.docx','7测试分析报告.docx']:
    fp = os.path.join(out, fname)
    doc = docx.Document(fp)
    full_text = ' '.join([p.text for p in doc.paragraphs])
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                full_text += ' ' + c.text
    remaining = [p for p in ['****', '**系统', '2020年', '软件171', '***'] if p in full_text]
    status = 'CLEAN' if not remaining else f'HAS: {remaining}'
    print(f'{fname}: {status}')
