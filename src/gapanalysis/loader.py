"""Loading/saving gap analysis data."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .models import ControlISO27001, GapFinding, ReadinessItem, Scope
from .scales import FINDING_STATUS, GAP_SEVERITY

SCOPE_FIELDS = ["framework", "org_name", "scope_description", "applicability_date", "approved_by", "auditor"]
ISO_FIELDS = ["control_id", "clause", "control_name", "objective", "category", "owner", "iso_ref", "soc2_mapping", "required", "maturity_target", "evidence_expected", "status_planned"]
FINDINGS_FIELDS = ["finding_id", "framework", "control_id", "requirement", "observed", "current_state", "gap_severity", "recommended_action", "evidence_needed", "responsible", "target_date", "status"]
TRACKER_FIELDS = ["control_id", "framework", "target_maturity", "current_maturity", "owner", "status", "last_assessed", "due_for_review", "action_plan_id", "notes"]


class DataError(RuntimeError):
    pass


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise DataError(f"data file not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise DataError(f"empty data file: {path}")
        return [dict(row) for row in reader]


@dataclass(frozen=True)
class GapSet:
    scope: list[Scope]
    controls: list[ControlISO27001]
    findings: list[GapFinding]
    tracker: list[ReadinessItem]

    def validate(self) -> list[str]:
        issues: list[str] = []
        control_ids = {c.control_id for c in self.controls}
        for f in self.findings:
            if f.control_id not in control_ids and not f.control_id.startswith("CC"):
                issues.append(f"{f.finding_id}: unknown control_id '{f.control_id}'")
            if f.gap_severity not in GAP_SEVERITY:
                issues.append(f"{f.finding_id}: unknown gap_severity '{f.gap_severity}'")
            if f.status not in FINDING_STATUS:
                issues.append(f"{f.finding_id}: unknown status '{f.status}'")
        seen = set()
        for t in self.tracker:
            if t.control_id in seen and t.framework in ("ISO/IEC 27001", "SOC 2"):
                # allow same control_id only if different framework? not required
                pass
            seen.add((t.control_id, t.framework))
            if t.current_maturity > t.target_maturity:
                issues.append(f"{t.control_id}/{t.framework}: current_maturity > target_maturity")
        return issues


def load_gap_set(data_dir: str | Path) -> GapSet:
    base = Path(data_dir)
    return GapSet(
        scope=[Scope.from_row(r) for r in _read_rows(base / "scope.csv")],
        controls=[ControlISO27001.from_row(r) for r in _read_rows(base / "controls_iso27001.csv")],
        findings=[GapFinding.from_row(r) for r in _read_rows(base / "gap_findings.csv")],
        tracker=[ReadinessItem.from_row(r) for r in _read_rows(base / "readiness_tracker.csv")],
    )
