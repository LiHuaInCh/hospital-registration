#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Targeted fix: replace 2020->2026 and other placeholders across multi-run text"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from docx import Document

OUT = r'C:\Users\26370\Desktop\医院挂号导诊平台-课设文档'

def fix_paragraph_2020(para):
    """Fix '2020' split across runs (e.g., run1='20', run2='20')"""
    runs = para.runs
    if len(runs) < 2:
        # Check single run
        for run in runs:
            if '2020' in run.text:
                run.text = run.text.replace('2020', '2026')
                return True
        return False

    changed = False
    # Check adjacent pairs of runs for "20" + "20" pattern
    for i in range(len(runs) - 1):
        r1, r2 = runs[i], runs[i + 1]
        if r1.text.endswith('20') and r2.text.startswith('20'):
            # Change "20...20" to "20...26"
            r1.text = r1.text[:-2] + '20'  # keep "20"
            r2.text = '26' + r2.text[2:]     # "20" -> "26"
            changed = True
            return changed  # Only fix first occurrence per paragraph

    # Also check for single-run "2020"
    for run in runs:
        if '2020' in run.text:
            run.text = run.text.replace('2020', '2026')
            changed = True
    return changed

def fix_doc(path):
    doc = Document(path)
    changed = False

    # Fix paragraphs
    for para in doc.paragraphs:
        full = para.text

        # Fix 2020 dates
        if '2020' in full:
            if fix_paragraph_2020(para):
                changed = True

        # Fix system name placeholders
        for run in para.runs:
            if '****系统' in run.text:
                run.text = run.text.replace('****系统', '医院门诊挂号与导诊服务平台')
                changed = True
            elif '**系统' in run.text:
                run.text = run.text.replace('**系统', '医院门诊挂号与导诊服务平台')
                changed = True
            # Fix trailing * after project name (leftover from ** replacement)
            if '医院门诊挂号与导诊服务平台*' in run.text:
                run.text = run.text.replace('医院门诊挂号与导诊服务平台*', '医院门诊挂号与导诊服务平台')
                changed = True
            # Fix *** placeholder for names
            if '***' in run.text:
                run.text = run.text.replace('***', '成员A')
                changed = True
            # Fix class name
            if '软件171' in run.text:
                run.text = run.text.replace('软件171', '软件211')
                changed = True
            # Fix member list
            if '***，***，***，***，***，***，***' in run.text:
                run.text = run.text.replace('***，***，***，***，***，***，***',
                                           '成员A，成员B，成员C，成员D，成员E，成员F，成员G')
                changed = True
            # Fix ** in other contexts (group number, etc.)
            if '**' in run.text and ('组长' in para.text or '组别' in para.text or '学号' in para.text or '成绩' in para.text):
                run.text = run.text.replace('**', '成员A')
                changed = True

    # Fix tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if '2020' in para.text:
                        fix_paragraph_2020(para)
                        changed = True
                    for run in para.runs:
                        if '2020' in run.text:
                            run.text = run.text.replace('2020', '2026')
                            changed = True
                        if '****系统' in run.text:
                            run.text = run.text.replace('****系统', '医院门诊挂号与导诊服务平台')
                            changed = True
                        if '**系统' in run.text:
                            run.text = run.text.replace('**系统', '医院门诊挂号与导诊服务平台')
                            changed = True
                        if '***' in run.text:
                            run.text = run.text.replace('***', '成员A')
                            changed = True
                        if '软件171' in run.text:
                            run.text = run.text.replace('软件171', '软件211')
                            changed = True

    if changed:
        doc.save(path)
    return changed

# Process all 8 documents
for fname in sorted(os.listdir(OUT)):
    if fname.endswith('.docx') and fname[0].isdigit():
        path = os.path.join(OUT, fname)
        result = fix_doc(path)
        print(f'{"FIXED" if result else "OK"}: {fname}')

# Verify
print('\n--- Verification ---')
for fname in sorted(os.listdir(OUT)):
    if fname.endswith('.docx') and fname[0].isdigit():
        path = os.path.join(OUT, fname)
        doc = Document(path)
        has_2020 = any('2020' in p.text for p in doc.paragraphs)
        has_2026 = any('2026' in p.text for p in doc.paragraphs)
        has_proj = any('医院门诊挂号' in p.text for p in doc.paragraphs)
        status = 'OK' if (not has_2020 and has_2026 and has_proj) else 'ISSUES'
        print(f'{status}: {fname} (2020={has_2020}, 2026={has_2026}, proj={has_proj})')
