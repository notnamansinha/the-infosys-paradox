def append_reconciliation(doc, add_table, add_body):
    doc.add_page_break()
    doc.add_heading('Appendix G. Reconciliation and reproducibility', level=2)
    add_table(['FY2026, INR billion', 'Standardized', 'As reported'], [
        ['Operating cash flow', '366.99', '358.24'],
        ['Capital expenditure', '27.27', '27.27'],
        ['Free cash flow', '339.72', '330.97'],
        ['FCF difference', '8.75', '—'],
    ], font_size=9)
    notes = [
        'Source: Audited statutory cash flow filings and standardized institutional financial series (exports 019, 021); Infosys Limited (2026), business highlights. Standardized FCF = 366.99 − 27.27; as-reported FCF = 358.24 − 27.27. The exports locate the difference in operating cash flow but do not establish its accounting classification. The report consistently uses standardized FCF. The published 112.3% conversion also uses the company’s own profit basis; 115.4% here uses standardized NET_INCOME.',
        'Operating margin uses standardized operating margin series. FY2026 operating income/revenue from the adjusted income statement implies approximately 20.94%, versus 20.2933% in the standardized profitability field. These presentation bases must not be mixed. The company-adjusted 21.0% margin excludes labour-code provisions (Infosys Limited, 2026).',
        'Source: Institutional comparative return series (screen 049). Comparative return transcription: NIFTY 50 880.35% total return / 12.14% annualized; Infosys 985.87% / 12.71%; TCS 1563.25% / 15.15%; NIFTY IT 874.49% / 12.10%. Annualized values are transcribed directly. NIFTY IT also displays 874.49% price change; consistent dividend treatment is not established, so index outperformance is not claimed.',
        'Source: Institutional historical price series (exports 033–035). Historical price requested 30 April 2006–31 March 2026, monthly, INR. Infosys records contain 239 observations from 31 May 2006 to 30 March 2026. First price: INR181.87; final price: INR1,250.60. The series is rebased to the actual first observation. Adjustment settings are absent from exported headers.',
        'Source: Institutional segment disclosures (exports 028 and 030). Legend mapping: Energy & Utilities abbreviates Energy, Utilities, Resources & Services (SEG0000004619). Other industry labels follow the source. Geographic and industry shares sum to 100% before display rounding. Figure 7 plots annual FCF throughout; payout bars show selected years at actual calendar spacing.',
    ]
    for text in notes: add_body(text, style='Small Note', track=False)
    add_table(['Figure 8 marker', 'Date', 'Evidence'], [
        ['Financial crisis', '15 Sep 2008', 'IMF (2009): Lehman chronology'],
        ['CEO appointment', '12 Jun 2014', 'Infosys Limited (2014, p. 2): Sikka appointment announced; effective 1 Aug'],
        ['CEO resignation', '18 Aug 2017', 'Infosys Limited (2017): transition call'],
        ['Pandemic declaration', '11 Mar 2020', 'World Health Organization (2020): pandemic characterization'],
        ['Topaz launch', '23 May 2023', 'Infosys Limited (2023): launch release'],
        ['in-tech announcement', '18 Apr 2024', 'Infosys Limited (2024): acquisition disclosure'],
    ], font_size=8)
    add_body('Markers use exact dates against monthly observations; they do not estimate event returns. Source inventory: 011 income; 016 profitability; 017 growth; 019 standardized cash flow; 021 as-reported cash flow; 026 employees; 028 geography; 030 segments; 033–035 Infosys HP; 045 TCS HP; 047 TCS profitability; 049 COMP; 054–055 RV; 058 corporate actions; 059 M&A; 060 USD/INR screenshot. Source files remain in their archived inventory folders; earlier duplicate exports are not pooled.', style='Small Note', track=False)
