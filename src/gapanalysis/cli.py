"""Command line interface for ISO/IEC 27001 & SOC 2 gap analysis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .loader import DataError, load_gap_set
from .report import build_executive_report
from .dashboard import write_dashboard

DEFAULT_DATA_DIR = "data"
DEFAULT_OUT_DIR = "build"


def cmd_validate(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    issues = g.validate()
    if not issues:
        print("OK - gap analysis data quality checks passed.")
        return 0
    print(f"{len(issues)} finding(s):")
    for i, issue in enumerate(issues, 1):
        print(f"  {i:>2}. {issue}")
    return 1


def cmd_summary(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    crit = [f for f in g.findings if f.gap_severity == "Crítico"]
    high = [f for f in g.findings if f.gap_severity == "Alto"]
    print("=" * 68)
    print("ISO/IEC 27001 & SOC 2 GAP ANALYSIS - MERIDIAN PAY (READINESS)")
    print("=" * 68)
    print(f"Controls (Annex A / mapped): {len(g.controls)}")
    print(f"Gap findings               : {len(g.findings)}")
    print(f"  - Critical               : {len(crit)}")
    print(f"  - High                   : {len(high)}")
    print(f"Readiness tracker items    : {len(g.tracker)}")
    print("=" * 68)
    return 0


def cmd_findings(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    items = sorted(g.findings, key=lambda x: x.severity_rank, reverse=True)
    print("ID        FW        CTRL   SEV      RESPONSIBLE           TARGET      STATUS")
    print("-" * 95)
    for f in items:
        print(f"{f.finding_id:<10}{f.framework:<10}{f.control_id:<7}{f.gap_severity:<9}{f.responsible:<22}{f.target_date:<12}{f.status}")
    return 0


def cmd_tracker(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    print("CTRL/CRITERIA   FW              CUR  TGT  GAP  OWNER                        STATUS")
    print("-" * 92)
    for t in sorted(g.tracker, key=lambda x: x.gap, reverse=True):
        print(f"{t.control_id:<16}{t.framework:<16}{t.current_maturity:<5}{t.target_maturity:<5}{t.gap:<5}{t.owner:<29}{t.status}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    out = Path(args.out) / "iso27001-soc2-gap-report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_executive_report(g), encoding="utf-8")
    print(f"report written: {out}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    out = Path(args.out) / "gap-dashboard.html"
    p = write_dashboard(g, out)
    print(f"dashboard written: {p}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gapanalysis", description="ISO/IEC 27001 & SOC 2 Gap Analysis Tool")
    p.add_argument("--data", default=DEFAULT_DATA_DIR)
    p.add_argument("--out", default=DEFAULT_OUT_DIR)
    sp = p.add_subparsers(dest="command", required=True)
    sp.add_parser("validate").set_defaults(func=cmd_validate)
    sp.add_parser("summary").set_defaults(func=cmd_summary)
    sp.add_parser("findings").set_defaults(func=cmd_findings)
    sp.add_parser("tracker").set_defaults(func=cmd_tracker)
    sp.add_parser("report").set_defaults(func=cmd_report)
    sp.add_parser("dashboard").set_defaults(func=cmd_dashboard)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except DataError as e:
        print(f"data error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
