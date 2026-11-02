"""Statement of Applicability (SoA) generator for ISO/IEC 27001:2022.

The SoA is the document an auditor asks for first: for every Annex A control it
must state whether the control is applicable, why, how it is implemented and
where the evidence lives. Generating it from the same CSV that feeds the gap
analysis keeps the SoA, the findings and the tracker consistent by construction.

The framework crosswalk below is *category level* and indicative. It maps the
scenario controls to NIST CSF 2.0 functions, DORA articles and LGPD articles so
the SoA can be read by a risk committee, not only by an ISO auditor.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .loader import GapSet
from .models import ControlISO27001, GapFinding, ReadinessItem

COMPANY = "Meridian Pay"
ISO_VERSION = "ISO/IEC 27001:2022"

# category -> (NIST CSF 2.0, DORA, LGPD)
CROSSWALK: dict[str, tuple[str, str, str]] = {
    "Governanca": ("GV.OC / GV.RM", "Art. 5-6", "Art. 50"),
    "Acesso": ("PR.AA", "Art. 9", "Art. 46"),
    "Terceiros": ("GV.SC", "Art. 28-30", "Art. 46 / 49"),
    "Continuidade": ("RC.RP", "Art. 11-12", "Art. 46"),
    "Endpoint": ("PR.PS", "Art. 9", "Art. 46"),
    "Vulnerabilidades": ("ID.RA", "Art. 15", "Art. 46"),
    "Dados": ("PR.DS", "Art. 9-10", "Art. 46"),
    "Monitoramento": ("DE.CM", "Art. 10", "Art. 46 / 48"),
    "Redes": ("PR.IR", "Art. 9", "Art. 46"),
    "Aplicacao": ("PR.PS / PR.DS", "Art. 9 / 15", "Art. 49"),
    "Ambiente": ("PR.IR", "Art. 9", "Art. 46"),
    "Mudancas": ("PR.PS", "Art. 9", "Art. 46"),
}

STATUS_ORDER = {
    "Nao implementado": 0,
    "Parcialmente implementado": 1,
    "Implementado": 2,
    "Otimizado": 3,
}


@dataclass(frozen=True)
class SoAEntry:
    control_id: str
    clause: str
    control_name: str
    category: str
    applicable: str
    justification: str
    implementation_status: str
    maturity_current: int
    maturity_target: int
    owner: str
    soc2_mapping: str
    nist_csf: str
    dora: str
    lgpd: str
    evidence: str
    open_findings: int
    finding_ids: str
    status_planned: str

    def to_row(self) -> dict[str, str]:
        return {
            "control_id": self.control_id,
            "clause": self.clause,
            "control_name": self.control_name,
            "category": self.category,
            "applicable": self.applicable,
            "justification": self.justification,
            "implementation_status": self.implementation_status,
            "maturity_current": str(self.maturity_current),
            "maturity_target": str(self.maturity_target),
            "owner": self.owner,
            "soc2_mapping": self.soc2_mapping,
            "nist_csf": self.nist_csf,
            "dora": self.dora,
            "lgpd": self.lgpd,
            "evidence": self.evidence,
            "open_findings": str(self.open_findings),
            "finding_ids": self.finding_ids,
            "status_planned": self.status_planned,
        }


def _status_for(maturity: int, open_findings: int) -> str:
    """Derive the implementation status from maturity and open findings.

    An open finding is a contradiction with a "fully implemented" claim, so it
    caps the status at ``Parcialmente implementado``.
    """

    if maturity >= 5:
        status = "Otimizado"
    elif maturity >= 3:
        status = "Implementado"
    elif maturity >= 1:
        status = "Parcialmente implementado"
    else:
        status = "Nao implementado"
    if open_findings and STATUS_ORDER[status] > STATUS_ORDER["Parcialmente implementado"]:
        return "Parcialmente implementado"
    return status


def _index_tracker(tracker: list[ReadinessItem]) -> dict[str, ReadinessItem]:
    return {item.control_id: item for item in tracker}


def _index_findings(findings: list[GapFinding]) -> dict[str, list[GapFinding]]:
    out: dict[str, list[GapFinding]] = {}
    for finding in findings:
        out.setdefault(finding.control_id, []).append(finding)
    return out


def _justification(control: ControlISO27001, open_findings: int) -> str:
    if control.required.strip().lower() in ("nao", "não", "no"):
        return (
            "Nao aplicavel ao escopo atual: o ativo/processo nao esta coberto pelo SGSI "
            "ou o risco foi aceito formalmente pelo comite. Reavaliar na proxima revisao."
        )
    text = f"Aplicavel ao escopo ({control.category}): {control.objective}."
    if open_findings:
        text += f" {open_findings} achado(s) de lacuna em aberto impedem declarar implementacao plena."
    return text


def build_soa(gap_set: GapSet) -> list[SoAEntry]:
    """Build one SoA entry per mapped Annex A control."""

    tracker = _index_tracker(gap_set.tracker)
    findings = _index_findings(gap_set.findings)
    scope = gap_set.scope[0].scope_description if gap_set.scope else "escopo do SGSI"

    entries: list[SoAEntry] = []
    for control in gap_set.controls:
        item = tracker.get(control.control_id)
        current = item.current_maturity if item else 0
        target = item.target_maturity if item else control.maturity_target
        control_findings = findings.get(control.control_id, [])
        open_findings = [f for f in control_findings if f.status != "Fechado"]
        nist, dora, lgpd = CROSSWALK.get(control.category, ("-", "-", "-"))
        evidence = control.evidence_expected
        if open_findings:
            extra = "; ".join(
                dict.fromkeys(
                    f.evidence_needed for f in open_findings if f.evidence_needed
                )
            )
            if extra:
                evidence = f"{evidence}; {extra}"
        entries.append(
            SoAEntry(
                control_id=control.control_id,
                clause=control.clause,
                control_name=control.control_name,
                category=control.category,
                applicable="Sim"
                if control.required.strip().lower() in ("sim", "yes")
                else "Nao",
                justification=_justification(control, len(open_findings)),
                implementation_status=_status_for(current, len(open_findings)),
                maturity_current=current,
                maturity_target=target,
                owner=control.owner,
                soc2_mapping=control.soc2_mapping or "-",
                nist_csf=nist,
                dora=dora,
                lgpd=lgpd,
                evidence=evidence,
                open_findings=len(open_findings),
                finding_ids=";".join(sorted(f.finding_id for f in open_findings)),
                status_planned=control.status_planned,
            )
        )
    return entries


def soa_summary(entries: list[SoAEntry]) -> dict[str, int]:
    summary = {status: 0 for status in STATUS_ORDER}
    for entry in entries:
        summary[entry.implementation_status] += 1
    summary["applicable"] = sum(1 for e in entries if e.applicable == "Sim")
    summary["not_applicable"] = sum(1 for e in entries if e.applicable == "Nao")
    summary["with_open_findings"] = sum(1 for e in entries if e.open_findings)
    return summary


def build_soa_markdown(
    entries: list[SoAEntry], scope_line: str, soc2_findings: int = 0
) -> str:
    summary = soa_summary(entries)
    lines: list[str] = []
    add = lines.append
    add(f"# Statement of Applicability (SoA) - {COMPANY}")
    add("")
    add(f"> Referencia: **{ISO_VERSION}**, Anexo A. Documento gerado a partir de "
        "`data/controls_iso27001.csv`, `readiness_tracker.csv` e `gap_findings.csv`.")
    add("")
    add(f"**Escopo:** {scope_line}")
    add("")
    add("## 1) Resumo")
    add("")
    add(f"- Controles avaliados: **{len(entries)}**")
    add(f"- Aplicaveis: **{summary['applicable']}** | Nao aplicaveis: **{summary['not_applicable']}**")
    add(f"- Implementados ou otimizados: **{summary['Implementado'] + summary['Otimizado']}**")
    add(f"- Parcialmente implementados: **{summary['Parcialmente implementado']}**")
    add(f"- Nao implementados: **{summary['Nao implementado']}**")
    add(f"- Com achado de lacuna em aberto: **{summary['with_open_findings']}**")
    add("")
    add("> Este SoA cobre apenas o Anexo A da ISO/IEC 27001. "
        f"**{soc2_findings} achado(s) SOC 2** (Trust Service Criteria) sao acompanhados "
        "no `readiness_tracker.csv` e no `remediation-plan.md`, fora desta declaracao.")
    add("")
    add("## 2) Declaracao de aplicabilidade")
    add("")
    add("| Controle | Nome | Aplicavel | Justificativa | Status | Mad. atual/alvo | Dono |")
    add("|---|---|---|---|---|---|---|")
    for entry in entries:
        add(
            f"| {entry.control_id} | {entry.control_name} | {entry.applicable} | "
            f"{entry.justification} | {entry.implementation_status} | "
            f"{entry.maturity_current}/{entry.maturity_target} | {entry.owner} |"
        )
    add("")
    add("## 3) Evidencias e mapeamento cruzado")
    add("")
    add("| Controle | Evidencia esperada | SOC 2 | NIST CSF 2.0 | DORA | LGPD | Achados |")
    add("|---|---|---|---|---|---|---|")
    for entry in entries:
        add(
            f"| {entry.control_id} | {entry.evidence} | {entry.soc2_mapping} | "
            f"{entry.nist_csf} | {entry.dora} | {entry.lgpd} | "
            f"{entry.finding_ids or '-'} |"
        )
    add("")
    add("## 4) Metodologia")
    add("")
    add("- **Aplicabilidade**: derivada do campo `required` do catalogo de controles.")
    add("- **Status**: derivado da maturidade atual (`readiness_tracker.csv`); achado aberto limita o status a *Parcialmente implementado*.")
    add("- **Evidencia**: `evidence_expected` do controle, acrescida da evidencia exigida pelos achados abertos.")
    add("- **Crosswalk**: mapeamento indicativo por categoria (NIST CSF 2.0 / DORA / LGPD). Nao substitui parecer juridico.")
    add("")
    return "\n".join(lines)


def write_soa_csv(entries: list[SoAEntry], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(entries[0].to_row().keys()) if entries else []
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(entry.to_row() for entry in entries)
    return out


# --- Shared crosswalk export ------------------------------------------------
# This is the canonical cross-repository mapping. The risk register (01) and the
# TPRM toolkit (03) reference the same framework vocabulary so a reader can move
# from a risk/vendor to the matching ISO control without translating taxonomies.

CROSSWALK_FIELDS = [
    "control_id",
    "control_name",
    "category",
    "applicable",
    "implementation_status",
    "soc2_mapping",
    "nist_csf_2_0",
    "dora",
    "lgpd",
    "evidence",
    "open_findings",
]


def crosswalk_rows(entries: list[SoAEntry]) -> list[dict[str, str]]:
    """Flatten the SoA into one crosswalk row per control."""

    return [
        {
            "control_id": entry.control_id,
            "control_name": entry.control_name,
            "category": entry.category,
            "applicable": entry.applicable,
            "implementation_status": entry.implementation_status,
            "soc2_mapping": entry.soc2_mapping,
            "nist_csf_2_0": entry.nist_csf,
            "dora": entry.dora,
            "lgpd": entry.lgpd,
            "evidence": entry.evidence,
            "open_findings": str(entry.open_findings),
        }
        for entry in entries
    ]


def write_crosswalk_csv(rows: list[dict[str, str]], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CROSSWALK_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return out


def build_crosswalk_markdown(rows: list[dict[str, str]]) -> str:
    categories = sorted({row["category"] for row in rows})
    mapped = sum(1 for row in rows if row["nist_csf_2_0"] not in ("", "-"))
    lines: list[str] = []
    add = lines.append
    add(f"# Framework Crosswalk - {COMPANY}")
    add("")
    add(f"> Canonical mapping shared by repos 01 (risk register), 02 (gap analysis) "
        f"and 03 (TPRM). Reference: **{ISO_VERSION}** Annex A, **NIST CSF 2.0**, "
        "**DORA** and **LGPD**.")
    add("")
    add("## 1) Coverage")
    add("")
    add(f"- Controls mapped: **{len(rows)}**")
    add(f"- Categories: **{len(categories)}** ({', '.join(categories)})")
    add(f"- With NIST CSF 2.0 reference: **{mapped}**")
    add("")
    add("## 2) Control level mapping")
    add("")
    add("| Control | Name | Category | SOC 2 | NIST CSF 2.0 | DORA | LGPD | Status |")
    add("|---|---|---|---|---|---|---|---|")
    for row in rows:
        add(
            f"| {row['control_id']} | {row['control_name']} | {row['category']} | "
            f"{row['soc2_mapping']} | {row['nist_csf_2_0']} | {row['dora']} | "
            f"{row['lgpd']} | {row['implementation_status']} |"
        )
    add("")
    add("## 3) How the other repositories use this vocabulary")
    add("")
    add("- **01 - Risk register**: each risk carries a control reference and the KRI "
        "thresholds are the leading indicators of the same controls mapped here.")
    add("- **03 - TPRM**: vendor categories reuse the `Terceiros` row (DORA Art. 28-30, "
        "LGPD Art. 46/49) and exit plans cite the same articles.")
    add("- **02 - Gap analysis**: the SoA, remediation plan and this export are generated "
        "from the same CSV, so status and evidence never diverge.")
    add("")
    add("## 4) Disclaimer")
    add("")
    add("Mapping is indicative and category level. It supports a risk committee "
        "conversation; it does not replace legal advice or a formal audit.")
    add("")
    return "\n".join(lines)
