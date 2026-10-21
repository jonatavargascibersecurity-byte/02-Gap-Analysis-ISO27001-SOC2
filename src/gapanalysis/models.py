"""Data models for ISO/IEC 27001 and SOC 2 gap analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

from .scales import FINDING_STATUS, GAP_SEVERITY, SEVERITY_ORDER


def _strip(raw: str) -> str:
    return str(raw).strip()


def _to_int(raw: str, name: str, row_id: str) -> int:
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{row_id}: {name} must be integer") from exc


@dataclass(frozen=True)
class ControlISO27001:
    control_id: str
    clause: str
    control_name: str
    objective: str
    category: str
    owner: str
    iso_ref: str
    soc2_mapping: str
    required: str
    maturity_target: int
    evidence_expected: str
    status_planned: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "ControlISO27001":
        return cls(
            control_id=_strip(row["control_id"]),
            clause=_strip(row["clause"]),
            control_name=_strip(row["control_name"]),
            objective=_strip(row["objective"]),
            category=_strip(row["category"]),
            owner=_strip(row["owner"]),
            iso_ref=_strip(row["iso_ref"]),
            soc2_mapping=_strip(row.get("soc2_mapping", "")),
            required=_strip(row["required"]),
            maturity_target=_to_int(row["maturity_target"], "maturity_target", row["control_id"]),
            evidence_expected=_strip(row["evidence_expected"]),
            status_planned=_strip(row["status_planned"]),
        )


@dataclass(frozen=True)
class GapFinding:
    finding_id: str
    framework: str
    control_id: str
    requirement: str
    observed: str
    current_state: str
    gap_severity: str
    recommended_action: str
    evidence_needed: str
    responsible: str
    target_date: str
    status: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "GapFinding":
        return cls(
            finding_id=_strip(row["finding_id"]),
            framework=_strip(row["framework"]),
            control_id=_strip(row["control_id"]),
            requirement=_strip(row["requirement"]),
            observed=_strip(row["observed"]),
            current_state=_strip(row["current_state"]),
            gap_severity=_strip(row["gap_severity"]),
            recommended_action=_strip(row["recommended_action"]),
            evidence_needed=_strip(row["evidence_needed"]),
            responsible=_strip(row["responsible"]),
            target_date=_strip(row["target_date"]),
            status=_strip(row["status"]),
        )

    @property
    def severity_rank(self) -> int:
        return SEVERITY_ORDER.get(self.gap_severity, 0)


@dataclass(frozen=True)
class ReadinessItem:
    control_id: str
    framework: str
    target_maturity: int
    current_maturity: int
    owner: str
    status: str
    last_assessed: str
    due_for_review: str
    action_plan_id: str
    notes: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "ReadinessItem":
        cid = _strip(row["control_id"])
        return cls(
            control_id=cid,
            framework=_strip(row["framework"]),
            target_maturity=_to_int(row["target_maturity"], "target_maturity", cid),
            current_maturity=_to_int(row["current_maturity"], "current_maturity", cid),
            owner=_strip(row["owner"]),
            status=_strip(row["status"]),
            last_assessed=_strip(row["last_assessed"]),
            due_for_review=_strip(row["due_for_review"]),
            action_plan_id=_strip(row["action_plan_id"]),
            notes=_strip(row["notes"]),
        )

    @property
    def gap(self) -> int:
        return max(0, self.target_maturity - self.current_maturity)


@dataclass(frozen=True)
class Scope:
    framework: str
    org_name: str
    scope_description: str
    applicability_date: str
    approved_by: str
    auditor: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Scope":
        return cls(
            framework=_strip(row["framework"]),
            org_name=_strip(row["org_name"]),
            scope_description=_strip(row["scope_description"]),
            applicability_date=_strip(row["applicability_date"]),
            approved_by=_strip(row["approved_by"]),
            auditor=_strip(row["auditor"]),
        )
