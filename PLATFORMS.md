# Plataformas, trilhas e como este repositório se conecta

Este repositório foi pensado para gerar **evidência prática** ao estudar em trilhas de GRC/Compliance. A regra é: *1 sala/trilha = 1 melhoria commitada, com menção ao que foi resolvido*.

## Mapeamento direto

| Plataforma / Trilha / Sala | Foco | Como este repo se relaciona | Como foi aplicado (evidência) |
|---|---|---|---|
| [TryHackMe - Governance & Regulation](https://tryhackme.com/room/cybergovernanceregulation) | Governança, leis/regulamentos, framework GRC | Mapeamento direto com ISO/IEC 27001:2022, SOC 2 e elementos de governança. | `soa` gera `build/SoA.md` com aplicabilidade, justificativa, status, maturidade e evidência dos 25 controles do Anexo A; SOC 2 aparece em seção separada. |
| [TryHackMe - Risk Management](https://tryhackme.com/room/seriskmanagement) | Avaliar/responder/monitorar riscos | Lacunas, severidade, plano de remediação e tracker de maturidade. | `remediation --as-of` ordena por `severity x gap` em Quick win/Estrutural/Monitorar e marca atrasos (8 vencidos em 2026-11-02). |
| [LetsDefend - Risk Management](https://app.letsdefend.io/training/lessons/risk-management) | Documentação, avaliação e priorização | Relatório executivo + artefatos auditáveis (SoA, plano de remediação). | `report`/`dashboard` e `remediation-plan.csv` trazem dono, prazo e evidência necessária por achado — formato de auditoria. |
| [HTB Academy - Security Audit and Testing](https://academy.hackthebox.com/course/preview/security-audit-and-testing) | Auditoria, evidência e testes | Estrutura próxima a auditoria de controles. | Cada achado tem `current_state`, `observed`, `recommended_action` e `evidence_needed`; o plano exporta esses campos sem perda. |
| [HTB Academy - Information Security Guidelines](https://academy.hackthebox.com/course/preview/information-security-guidelines) | DORA, NIST CSF 2.0, PCI-DSS, governança | Crosswalk no SoA (NIST/DORA/LGPD). | `crosswalk` exporta 25 controles em 12 categorias com referência NIST CSF 2.0, DORA e LGPD em Markdown + CSV. |

## Novos artefatos (Fase 1)

| Artefato | Comando | Descrição |
|---|---|---|
| `build/SoA.md` + `build/soa.csv` | `python -m gapanalysis soa` | *Statement of Applicability*: aplicabilidade, status, maturidade, evidências, crosswalk NIST/DORA/LGPD. |
| `build/remediation-plan.md` + `build/remediation-plan.csv` | `python -m gapanalysis remediation [--as-of YYYY-MM-DD]` | Plano sequenciado por `severity x gap` com buckets *Quick win/Estrutural/Monitorar* e carga por responsável. |
| `build/framework-crosswalk.md` + `build/framework-crosswalk.csv` | `python -m gapanalysis --out build crosswalk` | Crosswalk canônico ISO Anexo A → SOC 2 / NIST CSF 2.0 / DORA / LGPD, compartilhado com os repositórios 01 e 03. |

## Como usar para benefício duplo

1. Estude a sala/trilha
2. Identifique melhoria (nova evidência exigida, mapeamento, critério de priorização)
3. Atualize CSVs/código
4. Gere artefatos: `validate`, `soa`, `remediation`, `crosswalk`, `report`
5. **Commit com menção explícita**: `feat(gap): SoA+remediation from TryHackMe Governance&Regulation (room: https://tryhackme.com/room/cybergovernanceregulation) - resolve GF-XXX with evidence mapping`
6. Registre no `learning-log/` (Fase 5)

## Status

- [x] SoA + Remediation Plan (Fase 1)
- [x] Crosswalk compartilhado entre repos (Fase 4)
- [x] `learning-log/` com template de write-up (Fase 5)
- [x] SoA separa explicitamente ISO Anexo A (25 controles) de achados SOC 2 (6), sem misturar frameworks
- [x] Metadados do GitHub (description/topics) atualizados via API: *ISO/IEC 27001:2022 and SOC 2 gap analysis with generated Statement of Applicability, remediation plan and NIST CSF/DORA/LGPD crosswalk*; topics `compliance`, `audit`, `iso-27001`, `soc2`, `nist-csf`, `dora`, `lgpd`, `grc`, `tryhackme`, `hackthebox`, `python`, `portfolio`
