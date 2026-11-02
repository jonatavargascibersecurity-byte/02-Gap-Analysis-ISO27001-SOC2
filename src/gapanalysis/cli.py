"""Command line interface for ISO/IEC 27001 & SOC 2 gap analysis."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from .loader import DataError, load_gap_set
from .remediation import build_plan, build_plan_markdown, plan_summary, write_plan_csv
from .report import build_executive_report
from .dashboard import write_dashboard
from .soa import (
    build_crosswalk_markdown,
    build_soa,
    build_soa_markdown,
    crosswalk_rows,
    soa_summary,
    write_crosswalk_csv,
    write_soa_csv,
)

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


def cmd_soa(args: argparse.Namespace) -> int:
    from .soa import COMPANY

    g = load_gap_set(args.data)
    entries = build_soa(g)
    scope = g.scope[0].scope_description if g.scope else "escopo do SGSI"
    out_dir = Path(args.out)
    md = out_dir / "SoA.md"
    csv_path = out_dir / "soa.csv"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(build_soa_markdown(entries, scope), encoding="utf-8")
    write_soa_csv(entries, csv_path)
    summary = soa_summary(entries)
    print(f"soa written: {md}")
    print(f"soa data   : {csv_path}")
    print(
        "controls: {total} | applicable: {applicable} | implemented/optimised: {done} | "
        "partial: {partial} | not implemented: {missing} | open findings: {findings}".format(
            total=len(entries),
            applicable=summary["applicable"],
            done=summary["Implementado"] + summary["Otimizado"],
            partial=summary["Parcialmente implementado"],
            missing=summary["Nao implementado"],
            findings=summary["with_open_findings"],
        )
    )
    print(f"organization: {COMPANY}")
    return 0


def cmd_crosswalk(args: argparse.Namespace) -> int:
    g = load_gap_set(args.data)
    rows = crosswalk_rows(build_soa(g))
    out_dir = Path(args.out)
    md = out_dir / "framework-crosswalk.md"
    csv_path = out_dir / "framework-crosswalk.csv"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(build_crosswalk_markdown(rows), encoding="utf-8")
    write_crosswalk_csv(rows, csv_path)
    categories = sorted({row["category"] for row in rows})
    print(f"crosswalk written: {md}")
    print(f"crosswalk data   : {csv_path}")
    print(f"controls: {len(rows)} | categories: {len(categories)}")
    return 0


def cmd_remediation(args: argparse.Namespace) -> int:
    from .soa import COMPANY

    g = load_gap_set(args.data)
    try:
        as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    except ValueError:
        print(f"invalid --as-of date: {args.as_of!r} (expected YYYY-MM-DD)", file=sys.stderr)
        return 3
    plan = build_plan(g, as_of)
    out_dir = Path(args.out)
    md = out_dir / "remediation-plan.md"
    csv_path = out_dir / "remediation-plan.csv"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(build_plan_markdown(plan, COMPANY, as_of), encoding="utf-8")
    write_plan_csv(plan, csv_path)
    summary = plan_summary(plan)
    print(f"remediation plan written: {md}")
    print(f"remediation data        : {csv_path}")
    print(
        "open findings: {total} | critical/high: {ch} | overdue: {overdue} | "
        "quick wins: {qw} | structural: {st} | monitor: {mon}".format(
            total=summary["total"],
            ch=summary["critical_high"],
            overdue=summary["overdue"],
            qw=summary["Quick win"],
            st=summary["Estrutural"],
            mon=summary["Monitorar"],
        )
    )
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
    sp.add_parser("soa", help="generate the Statement of Applicability").set_defaults(func=cmd_soa)
    sp.add_parser(
        "crosswalk", help="export the shared NIST CSF/DORA/LGPD crosswalk"
    ).set_defaults(func=cmd_crosswalk)
    rem = sp.add_parser("remediation", help="generate the sequenced remediation plan")
    rem.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    rem.set_defaults(func=cmd_remediation)
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
