# Análise de Lacunas ISO/IEC 27001:2022 & SOC 2 (Meridian Pay)

Análise de lacunas orientada a evidências para uma fintech brasileira fictícia (**Meridian Pay**), mapeando controles do **Anexo A da ISO/IEC 27001:2022** aos **Critérios de Serviço de Confiança SOC 2 (Segurança/Disponibilidade/Confidencialidade)**.

## Funcionalidades

- **Mapeamento Anexo A**: 25 controles com responsáveis, evidências esperadas e metas de maturidade
- **Prontidão SOC 2**: mapeamento para TSC com foco em achados comuns de auditoria
- **Achados de lacuna**: priorização Crítico/Alto com responsável, prazo e evidências necessárias
- **Tracker de prontidão**: maturidade 0-5 com cálculo de lacuna e cadência de revisão
- **Statement of Applicability (SoA)**: aplicabilidade, justificativa, status, maturidade e evidência dos 25 controles do Anexo A
- **Plano de remediação**: sequência por `severity x gap` em Quick win/Estrutural/Monitorar, com atraso e carga por dono
- **Crosswalk**: ISO Anexo A → SOC 2 / NIST CSF 2.0 / DORA / LGPD, exportado em Markdown + CSV
- **CLI**: `validate`, `summary`, `findings`, `tracker`, `report`, `dashboard`, `soa`, `remediation`, `crosswalk`
- **Relatórios**: relatório executivo em Markdown + dashboard HTML autocontido
- **Frameworks separados**: o SoA cobre **apenas ISO Anexo A**; os 6 achados SOC 2 são acompanhados no tracker e no plano de remediação, fora da declaração ISO
- **Sem dependências em tempo de execução**: Python puro (stdlib), CSV como fonte única da verdade

## Início rápido

```bash
cd 02-Gap-Analysis-ISO27001-SOC2
pip install -e ".[dev]"
python -m gapanalysis validate
python -m gapanalysis summary
python -m gapanalysis --out build report
python -m gapanalysis --out build dashboard
python -m gapanalysis --out build soa
python -m gapanalysis --out build remediation --as-of 2026-11-02
python -m gapanalysis --out build crosswalk
```

## Alinhamento com plataformas de estudo

Este repositório é um laboratório de prática para trilhas de GRC e auditoria. Cada sala/trilha vira uma melhoria rastreável; o mapeamento completo (plataforma, link, artefato e o que foi resolvido) está em [`PLATFORMS.md`](PLATFORMS.md).

| Plataforma / conteúdo real | Link | Como o repositório aplica |
|---|---|---|
| **TryHackMe — Governance & Regulation** (sala) | [sala](https://tryhackme.com/room/cybergovernanceregulation) | SoA declara aplicabilidade, justificativa, status e evidência de cada controle do Anexo A. |
| **TryHackMe — Risk Management** (sala) | [sala](https://tryhackme.com/room/seriskmanagement) | Plano de remediação prioriza severidade x gap de maturidade (`Quick win` / `Estrutural` / `Monitorar`). |
| **LetsDefend — Risk Management** (curso) | [curso](https://app.letsdefend.io/training/lessons/risk-management) | Evidência, responsável e prazo no formato que uma auditoria pede. |
| **HTB Academy — Security Audit and Testing** (módulo) | [módulo](https://academy.hackthebox.com/course/preview/security-audit-and-testing) | Relatório com evidência necessária e ação recomendada por achado. |
| **HTB Academy — Information Security Guidelines** (módulo) | [módulo](https://academy.hackthebox.com/course/preview/information-security-guidelines) | Crosswalk NIST CSF 2.0 / DORA / LGPD exportado em CSV e Markdown. |

### Artefatos de auditoria

| Comando | Saída | Para que serve |
|---|---|---|
| `python -m gapanalysis --out build soa` | `build/SoA.md` + `build/soa.csv` | *Statement of Applicability*: o primeiro documento pedido em auditoria ISO. |
| `python -m gapanalysis --out build remediation --as-of YYYY-MM-DD` | `build/remediation-plan.md` + `.csv` | Sequência de execução com bucket, score, dono, prazo e atraso. |
| `python -m gapanalysis --out build crosswalk` | `build/framework-crosswalk.md` + `.csv` | Vocabulário compartilhado com os repositórios 01 (riscos) e 03 (TPRM). |

O crosswalk é gerado do mesmo CSV do SoA, então status, evidência e referência de framework nunca divergem. O template de write-up está em [`learning-log/000-template.md`](learning-log/000-template.md).

## Estrutura de dados

- `data/scope.csv` - escopo do SGSI e escopo SOC 2
- `data/controls_iso27001.csv` - controles do Anexo A com mapeamento SOC 2
- `data/gap_findings.csv` - achados com severidade, ações e evidências
- `data/readiness_tracker.csv` - acompanhamento de maturidade

## Licença

MIT
