# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-26

### Added
- **Public Statutory Dataset** (`data/infosys_annual_fy2007_fy2026.csv`): Public domain statutory financial series (revenue, net income, margins, employee count, cash flows, dividends, buybacks) derived from Infosys Limited Annual Reports and SEC Form 20-F filings.
- **Primary Report** (`Group-25-NamanKrSinha_KabirCharterjee_AU2540195_AU23L10004.pdf`):
  - 22-page Group 25 report edition containing Figures 1-8, Executive Summary, Section 5 Discussion, Limitations, References, and Appendices A-G (including terminal evidence and reconciliation).
- **Terminal Replication Guide** (`docs/data-replication-guide.md`): Complete runbook detailing exact terminal functions (`FA`, `HP`, `COMP`, `RV`, `CACS`, `DVD`), tickers, and parameters to replicate all raw series.
- **Sanitized Research Provenance** (`docs/thread-index.md`, `docs/thread-messages.md`): Research thread index and notes with all personal identifiable information (PII) and local machine paths scrubbed.
- **Dual-Mode Data Pipeline** (`scripts/build_analysis_data.py`): Automatically loads source workbooks if present locally; otherwise falls back gracefully to `data/infosys_annual_fy2007_fy2026.csv`.
- **Automated Verification Pipeline** (`scripts/verify_report.py`): Automated mathematical, statistical, and structural assertions ensuring zero-drift replication and report integrity.
- **Issue Templates** (`.github/ISSUE_TEMPLATE/`): Standardized templates for bug reports and replication inquiries.
- **Licensing**: Split license model—MIT for code (`LICENSE-CODE`) and Creative Commons Attribution 4.0 International (`LICENSE-DOCS`) for text and figures.
- **Contribution Guidelines** (`CONTRIBUTING.md`).

### Changed
- Moved all executable Python scripts into `scripts/` with relative path resolution.
- Refactored `scripts/make_charts.py` and `scripts/verified_charts.py` for cross-platform font resolution (Windows Cambria / Linux DejaVu Serif fallback).
- Replaced Appendix F screenshot images with a structured text-based Terminal Query Parameter and Provenance Audit table (Table F1).
- Overhauled `README.md` with executive findings, visual gallery, replication instructions, and citation format.

### Removed
- Purged all raw proprietary Excel workbooks (`.xlsx`), CSV exports, terminal UI screenshots, and rasterized preview directories from repository history to comply with intellectual property policies and terms of service.
- Removed student institutional email addresses, internal email headers (`.eml`), and absolute local path manifests.
