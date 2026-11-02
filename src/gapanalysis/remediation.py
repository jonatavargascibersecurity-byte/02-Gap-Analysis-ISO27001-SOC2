"""Remediation plan generator for gap findings.

Findings arrive from audits in severity order, but remediation is scheduled by
*impact x effort x dependency*. This module turns the gap findings plus the
maturity tracker into a sequenced plan with three buckets:

* ``Quick win``      - high severity, small maturity gap (<= 1): schedule first.
* ``Estrutural``     - high severity, maturity gap >= 2: needs a project.
* ``Monitorar``      - low/informational severity: batch into the next cycle.

Scoring is deterministic and date-aware only for overdue detection, so the same
inputs always produce the same plan.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .loader import GapSet
from .models import GapFinding, ReadinessItem
from .scales import SEVERITY_ORDER

BUCKET_ORDER = {"Quick win": 0, "Estrutural": 1, "Monitorar": 2}


@dataclass(frozen=True)
class RemediationItem:
    finding_id: str
    control_id: str
    framework: str
    severity: str
    priority_score: int
    bucket: str
    control_gap: int
    responsible: str
    target_date: str
    status: str
    overdue: str
    action: str
    evidence_needed: str

    def to_row(self) -> dict[str, str]:
        return {
            "priority_rank": "",  # filled by the writer
            "finding_id": self.finding_id,
            "control_id": self.control_id,
            "framework": self.framework,
            "severity": self.severity,
            "priority_score": str(self.priority_score),
            "bucket": self.bucket,
            "control_gap": str(self.control_gap),
            "responsible": self.responsible,
            "target_date": self.target_date,
            "status": self.status,
            "overdue": self.overdue,
            "action": self.action,
            "evidence_needed": self.evidence_needed,
        }


def _tracker_index(tracker: list[ReadinessItem]) -> dict[str, ReadinessItem]:
    return {item.control_id: item for item in tracker}


def _bucket(severity: str, gap: int) -> str:
    if severity in ("Alto", "Crítico"):
        return "Quick win" if gap <= 1 else "Estrutural"
    return "Monitorar"


def _score(finding: GapFinding, gap: int, overdue: bool) -> int:
    value = SEVERITY_ORDER.get(finding.gap_severity, 1) * 10
    value += max(0, gap) * 2
    if finding.status == "Aberto":
        value += 3
    if overdue:
        value += 2
    return value


def _is_overdue(target: str, as_of: date) -> bool:
    try:
        return date.fromisoformat(target.strip()) < as_of
    except ValueError:
        return False


def build_plan(gap_set: GapSet, as_of: date | None = None) -> list[RemediationItem]:
    reference = as_of or date.today()
    tracker = _tracker_index(gap_set.tracker)
    open_findings = [f for f in gap_set.findings if f.status != "Fechado"]

    items: list[RemediationItem] = []
    for finding in open_findings:
        item = tracker.get(finding.control_id)
        gap = item.gap if item else 0
        overdue = _is_overdue(finding.target_date, reference)
        items.append(
            RemediationItem(
                finding_id=finding.finding_id,
                control_id=finding.control_id,
                framework=finding.framework,
                severity=finding.gap_severity,
                priority_score=_score(finding, gap, overdue),
                bucket=_bucket(finding.gap_severity, gap),
                control_gap=gap,
                responsible=finding.responsible,
                target_date=finding.target_date,
                status=finding.status,
                overdue="Sim" if overdue else "Nao",
                action=finding.recommended_action,
                evidence_needed=finding.evidence_needed,
            )
        )
    return sorted(
        items,
        key=lambda i: (-i.priority_score, BUCKET_ORDER[i.bucket], i.target_date, i.finding_id),
    )


def workload(plan: list[RemediationItem]) -> list[tuple[str, int, int]]:
    """Return ``(responsible, items, total_score)`` sorted by total score."""

    totals: dict[str, list[int]] = {}
    for item in plan:
        entry = totals.setdefault(item.responsible, [0, 0])
        entry[0] += 1
        entry[1] += item.priority_score
    return sorted(
        ((owner, count, score) for owner, (count, score) in totals.items()),
        key=lambda row: (-row[2], row[0]),
    )


def plan_summary(plan: list[RemediationItem]) -> dict[str, int]:
    summary = {bucket: 0 for bucket in BUCKET_ORDER}
    for item in plan:
        summary[item.bucket] += 1
    summary["total"] = len(plan)
    summary["overdue"] = sum(1 for item in plan if item.overdue == "Sim")
    summary["critical_high"] = sum(
        1 for item in plan if item.severity in ("Crítico", "Alto")
    )
    return summary


def build_plan_markdown(plan: list[RemediationItem], company: str, as_of: date) -> str:
    summary = plan_summary(plan)
    lines: list[str] = []
    add = lines.append
    add(f"# Plano de Remediacao - {company}")
    add("")
    add(f"**Data de referencia:** {as_of.isoformat()}  ")
    add("**Fonte:** `data/gap_findings.csv` + `data/readiness_tracker.csv`")
    add("")
    add("## 1) Resumo")
    add("")
    add(f"- Achados em aberto: **{summary['total']}**")
    add(f"- Criticos/Altos: **{summary['critical_high']}** | Vencidos: **{summary['overdue']}**")
    add(f"- Quick wins: **{summary['Quick win']}** | Estruturais: **{summary['Estrutural']}** | Monitorar: **{summary['Monitorar']}**")
    add("")
    add("## 2) Sequencia de execucao")
    add("")
    add("| # | Achado | Controle | Severidade | Score | Bucket | Gap | Dono | Prazo | Vencido | Acao |")
    add("|---|---|---|---|---|---|---|---|---|---|---|")
    for index, item in enumerate(plan, start=1):
        add(
            f"| {index} | {item.finding_id} | {item.control_id} | {item.severity} | "
            f"{item.priority_score} | {item.bucket} | {item.control_gap} | "
            f"{item.responsible} | {item.target_date} | {item.overdue} | {item.action} |"
        )
    add("")
    add("## 3) Carga por responsavel")
    add("")
    add("| Responsavel | Achados | Score acumulado |")
    add("|---|---|---|")
    for owner, count, score in workload(plan):
        add(f"| {owner} | {count} | {score} |")
    add("")
    add("## 4) Regra de priorizacao")
    add("")
    add("`score = severidade x 10 + gap_de_maturidade x 2 + status_aberto(3) + vencido(2)`")
    add("")
    add("- **Quick win**: severidade Alta/Critica e gap de maturidade <= 1.")
    add("- **Estrutural**: severidade Alta/Critica e gap >= 2 (requer projeto e orcamento).")
    add("- **Monitorar**: severidade Baixa/Informativo; agrupar no proximo ciclo.")
    add("")
    return "\n".join(lines)


def write_plan_csv(plan: list[RemediationItem], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "priority_rank",
        "finding_id",
        "control_id",
        "framework",
        "severity",
        "priority_score",
        "bucket",
        "control_gap",
        "responsible",
        "target_date",
        "status",
        "overdue",
        "action",
        "evidence_needed",
    ]
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank, item in enumerate(plan, start=1):
            row = item.to_row()
            row["priority_rank"] = str(rank)
            writer.writerow(row)
    return out
