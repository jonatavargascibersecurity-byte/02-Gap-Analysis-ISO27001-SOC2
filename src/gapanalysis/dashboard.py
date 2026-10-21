"""Static HTML dashboard for gap analysis."""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path

from .loader import GapSet
from .scales import MATURITY_EN

CSS = """
:root{--bg:#f4f6f8;--card:#fff;--ink:#1b2430;--muted:#5c6b7a;--line:#dfe5ec}
*{box-sizing:border-box}body{margin:0;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink)}
header{background:linear-gradient(135deg,#0b1b3a,#0b5fff);color:#fff;padding:28px 32px}
header h1{margin:0 0 6px}header p{margin:0;opacity:.85}
main{padding:24px 32px 48px;max-width:1180px;margin:0 auto}
h2{margin:32px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.cards{display:flex;flex-wrap:wrap;gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;min-width:180px;flex:1}
.card .label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.card .value{font-size:28px;font-weight:700;margin-top:6px}
.card .sub{font-size:12px;color:var(--muted);margin-top:4px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:9px 12px;text-align:left;font-size:13px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#eef2f7;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.03em}
tr:last-child td{border-bottom:none}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;color:#fff}
.muted{color:var(--muted)}
footer{color:var(--muted);font-size:12px;margin-top:32px;border-top:1px solid var(--line);padding-top:12px}
"""


def _esc(x): return escape(str(x), quote=True)


def _pill(text, color="#5c6b7a"): return f"<span class='pill' style='background:{color}'>{_esc(text)}</span>"


SEV_COLOR = {"Informativo": "#607d8b", "Baixo": "#2e7d32", "Alto": "#ef6c00", "Crítico": "#c62828"}
MAT_COLOR = {0:"#9e9e9e",1:"#b71c1c",2:"#ef6c00",3:"#f9a825",4:"#2e7d32",5:"#1b5e20"}


def build_dashboard(g: GapSet, generated_at: datetime | None = None) -> str:
    now = generated_at or datetime.now(timezone.utc)
    crit = [f for f in g.findings if f.gap_severity == "Crítico"]
    high = [f for f in g.findings if f.gap_severity == "Alto"]
    html = []
    add = html.append
    add("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>")
    add("<title>ISO27001 & SOC2 Gap Dashboard - Meridian Pay</title>")
    add(f"<style>{CSS}</style></head><body>")
    add("<header><h1>ISO/IEC 27001:2017 & SOC 2 Readiness Dashboard - Meridian Pay</h1>")
    add(f"<p>Fictional Brazilian fintech &#183; generated {now.strftime('%Y-%m-%d %H:%M UTC')}</p></header>")
    add("<main>")
    add("<div class='cards'>")
    add(f"<div class='card'><div class='label'>Controls mapped</div><div class='value'>{len(g.controls)}</div><div class='sub'>Annex A + SOC 2 criteria</div></div>")
    add(f"<div class='card'><div class='label'>Findings</div><div class='value'>{len(g.findings)}</div><div class='sub'>{len(crit)} Critical / {len(high)} High</div></div>")
    add(f"<div class='card'><div class='label'>Tracker items</div><div class='value'>{len(g.tracker)}</div><div class='sub'>Action plans tracked</div></div>")
    add(f"<div class='card'><div class='label'>Avg gap (tracker)</div><div class='value'>{round(sum(t.gap for t in g.tracker)/len(g.tracker),1) if g.tracker else 0}</div><div class='sub'>Target - Current maturity</div></div>")
    add("</div>")
    add("<h2>Findings by Severity</h2><table><thead><tr><th>ID</th><th>Framework</th><th>Control</th><th>Severity</th><th>Responsible</th><th>Target</th><th>Status</th></tr></thead><tbody>")
    for f in sorted(g.findings, key=lambda x: x.severity_rank, reverse=True):
        add(f"<tr><td>{_esc(f.finding_id)}</td><td>{_esc(f.framework)}</td><td>{_esc(f.control_id)}</td><td>{_pill(f.gap_severity, SEV_COLOR[f.gap_severity])}</td><td>{_esc(f.responsible)}</td><td class='muted'>{_esc(f.target_date)}</td><td class='muted'>{_esc(f.status)}</td></tr>")
    add("</tbody></table>")
    add("<h2>Readiness Tracker - Maturity</h2><table><thead><tr><th>Control/Criteria</th><th>Framework</th><th>Current</th><th>Target</th><th>Gap</th><th>Owner</th><th>Status</th><th>Last Assessed</th><th>Due</th></tr></thead><tbody>")
    for t in sorted(g.tracker, key=lambda x: x.gap, reverse=True):
        add(f"<tr><td>{_esc(t.control_id)}</td><td>{_esc(t.framework)}</td><td>{_pill(str(t.current_maturity), MAT_COLOR[t.current_maturity])} {MATURITY_EN[t.current_maturity]}</td><td>{_pill(str(t.target_maturity), MAT_COLOR[t.target_maturity])} {MATURITY_EN[t.target_maturity]}</td><td>{t.gap}</td><td>{_esc(t.owner)}</td><td class='muted'>{_esc(t.status)}</td><td class='muted'>{_esc(t.last_assessed)}</td><td class='muted'>{_esc(t.due_for_review)}</td></tr>")
    add("</tbody></table>")
    add("<footer>Generated by <span class='mono'>python -m gapanalysis dashboard</span> &#183; portfolio project, fictional scenario.</footer>")
    add("</main></body></html>")
    return "\n".join(html)


def write_dashboard(g: GapSet, out: str | Path) -> Path:
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(build_dashboard(g), encoding="utf-8")
    return p
