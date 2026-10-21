"""Unit tests for gap analysis scales and data."""

from pathlib import Path

from gapanalysis.loader import load_gap_set
from gapanalysis.scales import gap_score, maturity_label, readiness_pct

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_maturity_label():
    assert maturity_label(0) == "Nao existente"
    assert maturity_label(3) == "Definido"
    assert maturity_label(5) == "Otimizado"


def test_gap_score():
    assert gap_score(2, 4) == 2
    assert gap_score(4, 4) == 0
    assert gap_score(5, 3) == 0


def test_readiness_pct():
    assert readiness_pct(4, 4) == 100.0
    assert readiness_pct(3, 4) == 75.0
    assert readiness_pct(0, 4) == 0.0


def test_data_loads_and_validates():
    g = load_gap_set(DATA_DIR)
    assert len(g.controls) >= 20
    assert len(g.findings) >= 10
    assert g.validate() == []


def test_findings_have_evidence():
    g = load_gap_set(DATA_DIR)
    for f in g.findings:
        assert f.recommended_action.strip()
        assert f.evidence_needed.strip()
        assert f.responsible.strip()
