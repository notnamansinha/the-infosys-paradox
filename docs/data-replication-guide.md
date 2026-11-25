# Data Replication & Query Specification Guide

This document records the institutional financial terminal functions and parameters used to
produce the source data for this research archive. Any researcher with terminal database access
can reproduce the data extracts.

## Terminal session details

- Date: 15 September 2026
- Securities: INFO IN Equity (Infosys), TCS IN Equity (TCS)
- Indices: NIFTY Index, NIFTYIT Index, NSE500 Index, NIFTY200 Index
- Currency: INR throughout (except USDINR Curncy for exchange rate)
- Period: FY2007 to FY2026 for annual data; April 2006 to March 2026 for prices

## Financial statement exports (FA)

| Export | Function | Security | Template | Period |
|---|---|---|---|---|
| 011 | FA `<GO>` | INFO IN | Standardized Adjusted Income Statement | FY2007-FY2026 |
| 016 | FA `<GO>` | INFO IN | Profitability Ratios | FY2007-FY2026 |
| 017 | FA `<GO>` | INFO IN | Revenue Growth | FY2006-FY2026 |
| 019 | FA `<GO>` | INFO IN | Cash Flow (Standardized) | FY2007-FY2026 |
| 021 | FA `<GO>` | INFO IN | Cash Flow (As Reported) | FY2007-FY2026 |
| 022 | FA `<GO>` | INFO IN | Balance Sheet (Standardized) | FY2007-FY2026 |
| 023 | FA `<GO>` | INFO IN | Balance Sheet (As Reported) | FY2007-FY2026 |
| 024 | FA `<GO>` | INFO IN | Balance Sheet (Common Size) | FY2007-FY2026 |
| 025 | FA `<GO>` | INFO IN | Balance Sheet (Fair Value) | FY2007-FY2026 |
| 026 | FA `<GO>` | INFO IN | Employee Data | FY2007-FY2026 |
| 028 | FA `<GO>` | INFO IN | Geographic Revenue (by Measure) | FY2007-FY2026 |
| 030 | FA `<GO>` | INFO IN | Business Revenue (by Measure) | FY2007-FY2026 |
| 046 | FA `<GO>` | TCS IN | Standardized Adjusted Income Statement | FY2007-FY2026 |
| 047 | FA `<GO>` | TCS IN | Profitability Ratios | FY2007-FY2026 |
| 048 | FA `<GO>` | TCS IN | Revenue Growth | FY2007-FY2026 |

All FA exports use the "Export to Excel" option. Row numbers referenced in
`build_analysis_data.py` correspond to the standard FA Excel layout.

## Historical price exports (HP)

| Export | Function | Security | Frequency | Period | Fields |
|---|---|---|---|---|---|
| 033 | HP `<GO>` | INFO IN | Monthly | Apr 2006-Mar 2026 | PX_LAST |
| 034 | HP `<GO>` | INFO IN | Monthly | Apr 2006-Mar 2026 | PX_LAST, % change |
| 035 | HP `<GO>` | INFO IN | Monthly | Apr 2006-Mar 2026 | OHLC, % change |
| 045 | HP `<GO>` | TCS IN | Monthly | Apr 2006-Mar 2026 | PX_LAST |

HP exports contain 239 monthly observations from 31 May 2006 to 30 March 2026.
The first observation date is one month after the requested start date.

## Comparative returns (COMP)

| Export | Function | Securities | Frequency | Period |
|---|---|---|---|---|
| 049 | COMP `<GO>` | NIFTY, INFO IN, TCS IN, NIFTYIT | Monthly | 31 Mar 2006-28 Feb 2026 |

Values were transcribed from the on-screen table. COMP provides total return
comparisons but dividend treatment may differ between indices and equities.

## Corporate actions and M&A

| Export | Function | Security | Type |
|---|---|---|---|
| 058 | CACS `<GO>` | INFO IN | Dividends, splits, M&A, IPO/ADDL, listings |
| 059 | MA `<GO>` | INFO IN | Mergers and acquisitions |

## Relative valuation (RV)

| Export | Function | Security | Peers | Snapshot |
|---|---|---|---|---|
| 054 | RV `<GO>` | INFO IN | Custom peer set | Sep 2026 |
| 055 | RV `<GO>` | INFO IN | Overview | Sep 2026 |

## Notes

- All exports used the default database field definitions unless otherwise noted.
- The FCF figure uses "Standardized" cash flow (export 019). The "As Reported"
  cash flow (export 021) differs by approximately INR 8.75 billion in FY2026 due
  to operating cash flow classification. See Appendix G of the report.
- HP price-adjustment flags are absent from the exported headers. The series may
  reflect unadjusted closing prices.
