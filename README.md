# ISO/IEC 27001:2017 & SOC 2 Gap Analysis (Meridian Pay)

Evidence-driven gap analysis for a fictional Brazilian fintech (**Meridian Pay**), mapping **ISO/IEC 27001:2017 Annex A** controls to **SOC 2 Trust Service Criteria (Security/Availability/Confidentiality)**.

## Features

- **Annex A mapping**: 25 controls with owners, evidence expected and maturity targets
- **SOC 2 readiness**: TSC mapping (CC6/CC7/CC9/A1) with focus on common audit findings
- **Gap findings**: Critical/High prioritized with responsible, target dates and evidence needed
- **Readiness tracker**: maturity 0-5 with gap calculation and review cadence
- **CLI**: `validate`, `summary`, `findings`, `tracker`, `report`, `dashboard`
- **Reports**: Markdown executive report + self-contained HTML dashboard
- **Zero runtime deps**: pure Python stdlib, CSV as single source of truth

## Quick start

```bash
cd 02-Gap-Analysis-ISO27001-SOC2
pip install -e ".[dev]"
python -m gapanalysis validate
python -m gapanalysis summary
python -m gapanalysis report --out build
python -m gapanalysis dashboard --out build
```

## Data model

- `data/scope.csv` - ISMS scope and SOC 2 scope
- `data/controls_iso27001.csv` - Annex A controls with SOC 2 mapping
- `data/gap_findings.csv` - findings with severity, actions and evidence
- `data/readiness_tracker.csv` - maturity tracking

## License

MIT
