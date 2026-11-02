"""Tests for the Statement of Applicability and remediation plan."""

from dataclasses import replace
from datetime import date
from pathlib import Path

from gapanalysis.dashboard import build_dashboard
from gapanalysis.loader import load_gap_set
from gapanalysis.remediation import (
    build_plan,
    build_plan_markdown,
    plan_summary,
    write_plan_csv,
)
from gapanalysis.soa import (
    build_crosswalk_markdown,
    build_soa,
    build_soa_markdown,
    crosswalk_rows,
    soa_summary,
    write_crosswalk_csv,
    write_soa_csv,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_soa_covers_every_control():
    g = load_gap_set(DATA_DIR)
    entries = build_soa(g)
    assert len(entries) == len(g.controls)
    assert all(e.applicable == "Sim" for e in entries)
    assert all(e.nist_csf and e.dora and e.lgpd for e in entries)


def test_soa_open_finding_caps_status():
    g = load_gap_set(DATA_DIR)
    entries = {e.control_id: e for e in build_soa(g)}
    # A.5.18 has an open Critical finding and a maturity gap.
    assert entries["A.5.18"].open_findings == 1
    assert entries["A.5.18"].implementation_status == "Parcialmente implementado"
    assert "GF-003" in entries["A.5.18"].finding_ids


def test_soa_markdown_and_csv(tmp_path):
    g = load_gap_set(DATA_DIR)
    entries = build_soa(g)
    md = build_soa_markdown(entries, g.scope[0].scope_description)
    assert "Statement of Applicability" in md
    assert "ISO/IEC 27001:2022" in md
    csv_path = write_soa_csv(entries, tmp_path / "soa.csv")
    assert csv_path.exists()
    assert len(csv_path.read_text(encoding="utf-8").splitlines()) == len(entries) + 1
    assert soa_summary(entries)["applicable"] == len(entries)


def test_remediation_is_deterministic_and_scores_desc():
    g = load_gap_set(DATA_DIR)
    reference = date(2026, 11, 2)
    first = build_plan(g, reference)
    second = build_plan(g, reference)
    assert [i.finding_id for i in first] == [i.finding_id for i in second]
    assert all(first[i].priority_score >= first[i + 1].priority_score for i in range(len(first) - 1))
    summary = plan_summary(first)
    assert summary["total"] == len(first)
    assert summary["overdue"] >= 1
    assert summary["critical_high"] == len(first)


def test_remediation_outputs(tmp_path):
    g = load_gap_set(DATA_DIR)
    plan = build_plan(g, date(2026, 11, 2))
    md = build_plan_markdown(plan, "Meridian Pay", date(2026, 11, 2))
    assert "Plano de Remediacao" in md
    assert "Quick win" in md
    path = write_plan_csv(plan, tmp_path / "plan.csv")
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[1].startswith("1,")


def test_crosswalk_export(tmp_path):
    g = load_gap_set(DATA_DIR)
    rows = crosswalk_rows(build_soa(g))
    assert len(rows) == len(g.controls)
    assert all(row["nist_csf_2_0"] for row in rows)
    md = build_crosswalk_markdown(rows)
    assert "Framework Crosswalk" in md
    assert "DORA" in md
    path = write_crosswalk_csv(rows, tmp_path / "crosswalk.csv")
    assert path.exists()
    assert len(path.read_text(encoding="utf-8").splitlines()) == len(rows) + 1


def test_soa_declares_soc2_findings_separately():
    g = load_gap_set(DATA_DIR)
    soc2 = sum(1 for finding in g.findings if finding.framework == "SOC 2")
    md = build_soa_markdown(build_soa(g), g.scope[0].scope_description, soc2)
    assert "apenas o Anexo A da ISO/IEC 27001" in md
    assert f"{soc2} achado(s) SOC 2" in md
    assert "ISO/IEC 27001:2022" in md
    assert "ISO/IEC 27001:2017" not in md


def test_dashboard_uses_2022_and_separates_frameworks():
    g = load_gap_set(DATA_DIR)
    html = build_dashboard(g)
    assert "ISO/IEC 27001:2022" in html
    assert "ISO/IEC 27001:2017" not in html
    assert "Annex A controls" in html
    assert "SOC 2 findings" in html


def test_validation_catches_broken_framework_and_duplicates():
    g = load_gap_set(DATA_DIR)
    broken_finding = replace(g.findings[0], framework="ISO 27001")
    broken_tracker = replace(g.tracker[0], current_maturity=9)
    broken = replace(
        g,
        findings=g.findings + [broken_finding],
        tracker=g.tracker + [broken_tracker],
    )
    issues = broken.validate()
    assert any("unknown framework" in issue for issue in issues)
    assert any("duplicated finding_id" in issue for issue in issues)
    assert any("maturity must be 0-5" in issue for issue in issues)
