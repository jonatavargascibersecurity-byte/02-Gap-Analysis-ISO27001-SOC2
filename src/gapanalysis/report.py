"""Executive report generator for ISO/IEC 27001 & SOC 2 gap analysis."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from .loader import GapSet
from .scales import GAP_SEVERITY_EN, MATURITY_EN

COMPANY = "Meridian Pay"


def build_executive_report(g: GapSet) -> str:
    now = datetime.now(timezone.utc)
    crit = [f for f in g.findings if f.gap_severity == "Crítico"]
    high = [f for f in g.findings if f.gap_severity == "Alto"]
    lines = []
    add = lines.append
    add(f"# Gap Analysis Report - ISO/IEC 27001:2017 & SOC 2 Readiness - {COMPANY}")
    add("")
    add("> Fictional Brazilian fintech used as portfolio scenario.")
    add("")
    add(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')} | **Reference date:** {date.today().isoformat()}")
    add("")
    add("## 1) Scope")
    add("")
    for s in g.scope:
        add(f"### {s.framework}")
        add(f"- **Organization:** {s.org_name}")
        add(f"- **Scope:** {s.scope_description}")
        add(f"- **Applicability:** {s.applicability_date} | **Approved by:** {s.approved_by} | **Auditor:** {s.auditor}")
        add("")
    add("## 2) Executive Summary")
    add("")
    add(f"- **Annex A controls mapped:** {len(g.controls)}")
    add(f"- **Gap findings:** {len(g.findings)} ({len(crit)} Critical / {len(high)} High)")
    add(f"- **Readiness tracker items:** {len(g.tracker)}")
    add("")
    add("## 3) Top Findings (by severity)")
    add("")
    add("| Finding ID | Framework | Control | Severity | Responsible | Target | Status |")
    add("|---|---|---|---|---|---|---|")
    for f in sorted(g.findings, key=lambda x: x.severity_rank, reverse=True):
        add(f"| {f.finding_id} | {f.framework} | {f.control_id} | {f.gap_severity} | {f.responsible} | {f.target_date} | {f.status} |")
    add("")
    add("## 4) Readiness Tracker (Maturity)")
    add("")
    add("| Control/Criteria | Framework | Current | Target | Gap | Owner | Status | Last Assessed | Due Review |")
    add("|---|---|---|---|---|---|---|---|---|")
    for t in sorted(g.tracker, key=lambda x: x.gap, reverse=True):
        add(f"| {t.control_id} | {t.framework} | {t.current_maturity} ({MATURITY_EN[t.current_maturity]}) | {t.target_maturity} ({MATURITY_EN[t.target_maturity]}) | {t.gap} | {t.owner} | {t.status} | {t.last_assessed} | {t.due_for_review} |")
    add("")
    add("## 5) Recommended Actions")
    add("")
    for f in sorted(g.findings, key=lambda x: x.severity_rank, reverse=True)[:12]:
        add(f"### {f.finding_id} - {f.control_id} [{f.gap_severity}]")
        add(f"- **Requirement:** {f.requirement}")
        add(f"- **Observed:** {f.observed}")
        add(f"- **Recommended action:** {f.recommended_action}")
        add(f"- **Evidence needed:** {f.evidence_needed}")
        add(f"- **Responsible / Target:** {f.responsible} / {f.target_date}")
        add("")
    add("## 6) Approach")
    add("")
    add("- **ISO/IEC 27001:2017** - Annex A controls assessed against required evidence.")
    add("- **SOC 2 (Security/Availability/Confidentiality)** - mapped to Trust Service Criteria with readiness focus.")
    add("- **Evidence-driven** - each gap requires concrete evidence to be considered closed.")
    add("- **Risk-based prioritization** - Critical/High first, tracked to due dates.")
    add("")
    return "\n".join(lines)
