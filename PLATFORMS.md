# Plataformas, trilhas e como este repositório se conecta

Este repositório foi pensado para gerar **evidência prática** ao estudar em trilhas de GRC/Compliance. A regra é: *1 sala/trilha = 1 melhoria commitada, com menção ao que foi resolvido*.

## Mapeamento direto

| Plataforma / Trilha / Sala | Foco | Como este repo se relaciona | Como foi/será aplicado |
|---|---|---|---|
| [TryHackMe - Governance & Regulation](https://tryhackme.com/room/cybergovernanceregulation) | Governança, leis/regulamentos, framework GRC | Mapeamento direto com ISO/IEC 27001:2022, SOC 2 e elementos de governança. | Usar achados e SoA para demonstrar "Governança → Risco → Conformidade". |
| [TryHackMe - Threats & Risks (Risk Management)](https://tryhackme.com/module/threats-and-risks) | Avaliar/responder/monitorar riscos | Lacunas, severidade, plano de remediação e tracker de maturidade. | Aplicar priorização por severidade + gap de maturidade ao invés de apenas severidade. |
| [LetsDefend - SOC Manager Path](https://app.letsdefend.io/training) | Documentação, escalonamento, avaliação | Relatório executivo + artefatos auditáveis (SoA, plano de remediação). | Gerar evidências no formato pedido em auditorias/avaliações. |
| [HTB Academy - SOC Analyst Path](https://academy.hackthebox.com/path/preview/soc-analyst) | Reporting e incident handling | Estrutura próxima a incident reporting. | Adaptar plano de remediação com responsáveis, prazos e evidências. |
| [HTB - Governance & Compliance](https://www.hackthebox.com/cybersecurity-resources/governance_compliance) | DORA, NIST CSF 2.0, PCI-DSS | Crosswalk no SoA (NIST/DORA/LGPD). | Expandir mapeamento com base no que for estudado em DORA/NIST CSF 2.0. |

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
4. Gere artefatos: `validate`, `soa`, `remediation`, `report`
5. **Commit com menção explícita**: `feat(gap): SoA+remediation from TryHackMe Governance&Regulation (room: https://tryhackme.com/room/cybergovernanceregulation) - resolve GF-XXX with evidence mapping`
6. Registre no `learning-log/` (Fase 5)

## Status

- [x] SoA + Remediation Plan (Fase 1)
- [x] Crosswalk compartilhado entre repos (Fase 4)
- [x] `learning-log/` com template de write-up (Fase 5)
- [ ] Metadados do GitHub (description/topics) atualizados via `gh repo edit`
