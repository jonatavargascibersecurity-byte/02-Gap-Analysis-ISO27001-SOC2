"""Loading/saving gap analysis data."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
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
        rows = list(reader)
        for line, row in enumerate(rows, start=2):
            if None in row:
                raise DataError(
                    f"{path}:{line}: extra column(s) - row has more values than the header"
                )
        return rows


@dataclass(frozen=True)
class GapSet:
    scope: list[Scope]
    controls: list[ControlISO27001]
    findings: list[GapFinding]
    tracker: list[ReadinessItem]

    def validate(self) -> list[str]:
        issues: list[str] = []
        control_ids = {c.control_id for c in self.controls}
        frameworks = {"ISO/IEC 27001", "SOC 2"}

        seen_controls: set[str] = set()
        for control in self.controls:
            if control.control_id in seen_controls:
                issues.append(f"{control.control_id}: duplicated control_id")
            seen_controls.add(control.control_id)
            if not 0 <= control.maturity_target <= 5:
                issues.append(
                    f"{control.control_id}: maturity_target must be between 0 and 5"
                )

        def soc2_control(control_id: str) -> bool:
            # SOC 2 Trust Service Criteria are tracked outside the ISO Annex A
            # catalogue: CC6/CC7/CC9 and A1 (Availability).
            return control_id.startswith(("CC", "A1."))

        seen_findings: set[str] = set()
        for f in self.findings:
            if f.finding_id in seen_findings:
                issues.append(f"{f.finding_id}: duplicated finding_id")
            seen_findings.add(f.finding_id)
            if f.framework not in frameworks:
                issues.append(f"{f.finding_id}: unknown framework '{f.framework}'")
            if f.control_id not in control_ids and not soc2_control(f.control_id):
                issues.append(f"{f.finding_id}: unknown control_id '{f.control_id}'")
            if f.gap_severity not in GAP_SEVERITY:
                issues.append(f"{f.finding_id}: unknown gap_severity '{f.gap_severity}'")
            if f.status not in FINDING_STATUS:
                issues.append(f"{f.finding_id}: unknown status '{f.status}'")
            try:
                date.fromisoformat(f.target_date)
            except ValueError:
                issues.append(f"{f.finding_id}: target_date must be YYYY-MM-DD")

        seen_tracker: set[tuple[str, str]] = set()
        for t in self.tracker:
            key = (t.control_id, t.framework)
            if key in seen_tracker:
                issues.append(f"{t.control_id}/{t.framework}: duplicated tracker row")
            seen_tracker.add(key)
            if t.framework not in frameworks:
                issues.append(f"{t.control_id}: unknown framework '{t.framework}'")
            if t.control_id not in control_ids and not soc2_control(t.control_id):
                issues.append(f"{t.control_id}: unknown control_id '{t.control_id}'")
            if not 0 <= t.current_maturity <= 5 or not 0 <= t.target_maturity <= 5:
                issues.append(f"{t.control_id}/{t.framework}: maturity must be 0-5")
            if t.current_maturity > t.target_maturity:
                issues.append(f"{t.control_id}/{t.framework}: current_maturity > target_maturity")
            for field_name in ("last_assessed", "due_for_review"):
                try:
                    date.fromisoformat(getattr(t, field_name))
                except ValueError:
                    issues.append(
                        f"{t.control_id}/{t.framework}: {field_name} must be YYYY-MM-DD"
                    )
        return issues


def load_gap_set(data_dir: str | Path) -> GapSet:
    base = Path(data_dir)
    return GapSet(
        scope=[Scope.from_row(r) for r in _read_rows(base / "scope.csv")],
        controls=[ControlISO27001.from_row(r) for r in _read_rows(base / "controls_iso27001.csv")],
        findings=[GapFinding.from_row(r) for r in _read_rows(base / "gap_findings.csv")],
        tracker=[ReadinessItem.from_row(r) for r in _read_rows(base / "readiness_tracker.csv")],
    )
