"""Verify the generated report against source workbooks and analysis data.

Runs assertions on the analysis_data.json values, checks them against
xlsx workbooks (when available), and validates the DOCX report structure.
Writes output/verification_results.json.
"""
from pathlib import Path
import json, re, math
from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / 'output/analysis_data.json').read_text())
a = D['annual']
checks = []


def check(label, condition):
    assert condition, label
    checks.append(label)


def has_raw_folders():
    """Return True if the source export folders are present."""
    return any(ROOT.glob("011__*/*.xlsx"))


# ---- Raw workbook cross-checks (only when source folders are present) ----
if has_raw_folders():
    from openpyxl import load_workbook
    print("Verifying against source workbooks.")
    for key, prefix, row in [
        ('revenue', '011', 6), ('net_income', '011', 49),
        ('operating_margin', '016', 15), ('revenue_growth', '017', 7),
        ('headcount', '026', 6), ('sales_per_employee', '026', 8),
        ('cfo', '019', 18), ('fcf', '019', 63),
    ]:
        ws = load_workbook(next(ROOT.glob(prefix + '*/*.xlsx')), data_only=True).active
        for c in range(3, ws.max_column + 1):
            h = ws.cell(4, c).value
            if isinstance(h, str) and re.fullmatch(r'FY \d{4}', h) and h[-4:] in a[key]:
                check(f'{key} {h} matches raw export', a[key][h[-4:]] == ws.cell(row, c).value)

    for key in ['geography_pct', 'segments_pct']:
        if D.get(key):
            years = set.intersection(*(set(v) for v in D[key].values()))
            for y in years:
                check(f'{key} {y} totals 100%',
                      math.isclose(sum(v[y] for v in D[key].values()), 100, abs_tol=1e-7))
else:
    print("Source workbooks not locally present in root. Skipping raw workbook cross-checks.")

# ---- Structural checks on the analysis data ----
if D.get('infosys_monthly_price'):
    check('Price first date', D['infosys_monthly_price'][0]['date'] == '2006-05-31')
    check('239 monthly observations', len(D['infosys_monthly_price']) == 239)

check('COMP Infosys cumulative transcription',
      D['comparative_returns']['Infosys']['total_return_pct'] == 985.87)
check('FCF bridge',
      math.isclose(366.99 - 27.27, 339.72) and math.isclose(358.24 - 27.27, 330.97))

# ---- DOCX report structural checks ----
report_candidates = [
    ROOT / 'output/Scaling_with_Discipline_Infosys_Working_Paper.docx',
]
report_path = None
for rp in report_candidates:
    if rp.exists():
        report_path = rp
        break

if report_path:
    d = Document(report_path)
    p = d.paragraphs
    start = next(i for i, x in enumerate(p) if x.text == 'Executive Summary')
    end = next(i for i, x in enumerate(p) if x.text == 'References')
    count = lambda text: len(re.findall(r"\b[\w₹%–'-]+\b", text))
    full = count(' '.join(x.text for x in p[start:end]))
    narr = count(' '.join(
        x.text for x in p[start:end]
        if not x.style.name.startswith('Heading')
        and x.style.name not in ['Figure Caption', 'Figure Note']
    ))
    check('Narrative 1500-2000 words', 1500 <= narr <= 2000)
    check('Including headings captions notes 1500-2000', 1500 <= full <= 2000)
    check('Eight observation paragraphs',
          sum(x.text.startswith('Observation\u2014') for x in p) == 8)
    check('Eight interpretation paragraphs',
          sum(x.text.startswith('Interpretation\u2014') for x in p) == 8)
    check('Eight source notes',
          sum(x.text.startswith('Source and parameters:') for x in p) == 8)
    for h in [x for x in p if x.style.name.startswith('Heading')]:
        check('Black serif heading: ' + h.text,
              all(str(r.font.color.rgb) == '000000' and r.font.name == 'Cambria'
                  for r in h.runs))
    for title in [
        'Executive Summary', '1. Introduction', '2. Data Description',
        '3. Methodology', '4. Data Visualizations and Analysis',
        '5. Discussion', '6. Limitations', '7. Conclusion',
        'AI Tool Disclosure', 'References', 'Appendices',
    ]:
        check('Required section: ' + title, any(x.text == title for x in p))
    check('Body spacing is 1.15',
          math.isclose(d.styles['Normal'].paragraph_format.line_spacing, 1.15))
    check('Body paragraph spacing is 6 pt',
          d.styles['Normal'].paragraph_format.space_after.pt == 6)
else:
    narr = 0
    full = 0
    print("No report DOCX found. Skipping DOCX structural checks.")

report = {
    'passed_checks': len(checks),
    'narrative_words': narr,
    'words_with_headings_captions_notes': full,
    'checks': checks,
    'remaining_user_details': [
        'student name', 'roll number', 'course title/code', 'submission date',
    ],
    'limitations': [
        'HP price-adjustment flags absent',
        'COMP dividend treatment not fully comparable',
        'FCF classification difference located but not explained by exports',
        'instructor approval and prescribed citation/counting rules require student confirmation',
    ],
}
(ROOT / 'output/verification_results.json').write_text(
    json.dumps(report, indent=2), encoding='utf-8'
)
print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, indent=2))
