# Gap Analysis Report - ISO/IEC 27001:2017 & SOC 2 Readiness - Meridian Pay

> Fictional Brazilian fintech used as portfolio scenario.

**Generated:** 2026-10-21 18:42 UTC | **Reference date:** 2026-10-21

## 1) Scope

### ISO/IEC 27001:2017
- **Organization:** Meridian Pay
- **Scope:** ISMS covering onboarding digital; API PIX; processamento de pagamentos; dados de clientes; infraestrutura em nuvem e governanca
- **Applicability:** 2026-01-01 | **Approved by:** CISO | **Auditor:** Internal Audit

### SOC 2 - Trust Service Criteria 2017
- **Organization:** Meridian Pay
- **Scope:** SOC 2 Type 1/2 readiness for Security; Availability; Confidentiality (focus on Processing Integrity optional)
- **Applicability:** 2026-03-01 | **Approved by:** CFO/Internal Audit | **Auditor:** External Auditor (readiness)

## 2) Executive Summary

- **Annex A controls mapped:** 25
- **Gap findings:** 18 (3 Critical / 14 High)
- **Readiness tracker items:** 18

## 3) Top Findings (by severity)

| Finding ID | Framework | Control | Severity | Responsible | Target | Status |
|---|---|---|---|---|---|---|
| GF-003 | ISO/IEC 27001 | A.5.18 | Crítico | Head de Engenharia de Plataforma | 2026-10-15 | Em andamento |
| GF-007 | ISO/IEC 27001 | A.8.8 | Crítico | Head de Engenharia de Plataforma | 2026-10-20 | Em andamento |
| GF-009 | ISO/IEC 27001 | A.8.13 | Crítico | Head de Infraestrutura | 2026-10-25 | Em andamento |
| GF-001 | ISO/IEC 27001 | A.5.1 | Alto | Head de Conformidade | 2026-10-31 | Em andamento |
| GF-002 | ISO/IEC 27001 | A.5.15 | Alto | Head de Engenharia de Plataforma | 2026-11-15 | Em andamento |
| GF-004 | ISO/IEC 27001 | A.5.19 | Alto | Head de Third-Party Risk | 2026-11-30 | Em andamento |
| GF-005 | ISO/IEC 27001 | A.5.24 | Alto | Head de Conformidade | 2026-10-31 | Em andamento |
| GF-006 | ISO/IEC 27001 | A.8.2 | Alto | Head de Engenharia de Plataforma | 2026-11-15 | Em andamento |
| GF-008 | ISO/IEC 27001 | A.8.12 | Alto | Head de Engenharia de Plataforma | 2026-11-10 | Em andamento |
| GF-010 | ISO/IEC 27001 | A.8.16 | Alto | Head de SRE | 2026-11-01 | Em andamento |
| GF-011 | SOC 2 | CC6.1 | Alto | Head de Engenharia de Plataforma | 2026-11-20 | Em andamento |
| GF-012 | SOC 2 | CC6.2 | Alto | Head de RH/TI | 2026-11-15 | Em andamento |
| GF-013 | SOC 2 | CC7.2 | Alto | Head de SRE | 2026-11-10 | Em andamento |
| GF-014 | SOC 2 | CC7.3 | Alto | Head de Conformidade | 2026-10-31 | Em andamento |
| GF-016 | ISO/IEC 27001 | A.8.32 | Alto | Head de Engenharia de Plataforma | 2026-11-05 | Em andamento |
| GF-017 | ISO/IEC 27001 | A.8.25 | Alto | Head de Engenharia de Plataforma | 2026-11-12 | Em andamento |
| GF-018 | SOC 2 | CC9.1 | Alto | Head de Third-Party Risk | 2026-11-25 | Em andamento |
| GF-015 | SOC 2 | CC7.3 | A1 - Availability gap | A1 checklist; relatorio de teste; aprovacao | Head de Infraestrutura | 2026-10-28 |

## 4) Readiness Tracker (Maturity)

| Control/Criteria | Framework | Current | Target | Gap | Owner | Status | Last Assessed | Due Review |
|---|---|---|---|---|---|---|---|---|
| A.5.18 | ISO/IEC 27001 | 2 (Managed) | 4 (Quantitatively managed) | 2 | Head de Engenharia de Plataforma | Em andamento | 2026-09-05 | 2026-12-05 |
| CC6.2 | SOC 2 | 2 (Managed) | 4 (Quantitatively managed) | 2 | Head de RH/TI | Em andamento | 2026-09-18 | 2026-12-18 |
| A.5.1 | ISO/IEC 27001 | 2 (Managed) | 3 (Defined) | 1 | Head de Conformidade | Em andamento | 2026-09-01 | 2026-12-01 |
| A.5.15 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-05 | 2026-12-05 |
| A.5.19 | ISO/IEC 27001 | 2 (Managed) | 3 (Defined) | 1 | Head de Third-Party Risk | Em andamento | 2026-09-08 | 2026-12-08 |
| A.5.24 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Conformidade | Em andamento | 2026-09-08 | 2026-12-08 |
| A.8.2 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-10 | 2026-12-10 |
| A.8.8 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-10 | 2026-12-10 |
| A.8.12 | ISO/IEC 27001 | 2 (Managed) | 3 (Defined) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-12 | 2026-12-12 |
| A.8.13 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Infraestrutura | Em andamento | 2026-09-12 | 2026-12-12 |
| A.8.16 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de SRE | Em andamento | 2026-09-15 | 2026-12-15 |
| CC6.1 | SOC 2 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-18 | 2026-12-18 |
| CC7.2 | SOC 2 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de SRE | Em andamento | 2026-09-20 | 2026-12-20 |
| CC7.3 | SOC 2 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Conformidade | Em andamento | 2026-09-20 | 2026-12-20 |
| A1.3 | SOC 2 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Infraestrutura | Em andamento | 2026-09-22 | 2026-12-22 |
| CC9.1 | SOC 2 | 2 (Managed) | 3 (Defined) | 1 | Head de Third-Party Risk | Em andamento | 2026-09-22 | 2026-12-22 |
| A.8.32 | ISO/IEC 27001 | 3 (Defined) | 4 (Quantitatively managed) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-25 | 2026-12-25 |
| A.8.25 | ISO/IEC 27001 | 2 (Managed) | 3 (Defined) | 1 | Head de Engenharia de Plataforma | Em andamento | 2026-09-25 | 2026-12-25 |

## 5) Recommended Actions

### GF-003 - A.5.18 [Crítico]
- **Requirement:** Provisionamento com aprovacao do dono
- **Observed:** Existe fluxo mas aprovacao nao e obrigatoria para alguns perfis privilegiados
- **Recommended action:** Criar regra obrigatoria de aprovacao do owner e bloqueio se sem aprovacao
- **Evidence needed:** Workflow configurado; logs; teste aprovado
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-10-15

### GF-007 - A.8.8 [Crítico]
- **Requirement:** Vulnerabilidades com SLA por severidade
- **Observed:** SLA existe mas nao e monitorado em dashboard e ha criticos vencidos
- **Recommended action:** Monitorar SLA em dashboard com alerta e plano para criticos vencidos
- **Evidence needed:** Relatorio SLA; dashboard; plano de acao
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-10-20

### GF-009 - A.8.13 [Crítico]
- **Requirement:** Backup imutavel e teste de restauração
- **Observed:** Backup existe mas imutabilidade nao verificada e teste de restauração incompleto
- **Recommended action:** Ativar imutabilidade; testar restauração por servico critico; registrar evidencia
- **Evidence needed:** Config backup; verificação de imutabilidade; relatorio de restauracao
- **Responsible / Target:** Head de Infraestrutura / 2026-10-25

### GF-001 - A.5.1 [Alto]
- **Requirement:** Politica aprovada e revisada anualmente
- **Observed:** Politica existe mas ultima revisao foi ha 18 meses e nao tem ata assinada
- **Recommended action:** Revisar politica; aprovar em comite; registrar ata
- **Evidence needed:** Politica revisada; ata com aprovacao; registro
- **Responsible / Target:** Head de Conformidade / 2026-10-31

### GF-002 - A.5.15 [Alto]
- **Requirement:** Controle de acesso baseado em necessidade de conhecimento
- **Observed:** Matriz RBAC existe mas ha 12 contas com acesso generico sem justificativa
- **Recommended action:** Remover acesso generico; justificar ou re-provisionar com menor privilégio
- **Evidence needed:** Relatorio de acesso; justificativas; aprovacao
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-11-15

### GF-004 - A.5.19 [Alto]
- **Requirement:** Processo formal TPRM
- **Observed:** Due diligence ad-hoc por email sem scorecard padronizado
- **Recommended action:** Implantar scorecard; registro de fornecedores; criterios de aprovacao
- **Evidence needed:** Politica TPRM; scorecard preenchido; lista aprovada
- **Responsible / Target:** Head de Third-Party Risk / 2026-11-30

### GF-005 - A.5.24 [Alto]
- **Requirement:** Plano de resposta a incidente testado
- **Observed:** Runbook existe mas teste de mesa realizado ha >12 meses
- **Recommended action:** Realizar teste de mesa com cenario PIX/ransomware e registrar lições
- **Evidence needed:** Convite; lista presenca; relatorio com acoes; evidencias
- **Responsible / Target:** Head de Conformidade / 2026-10-31

### GF-006 - A.8.2 [Alto]
- **Requirement:** Acesso privilegiado com MFA e just-in-time
- **Observed:** Contas privilegiadas com MFA mas sem JIT e sem justificativa por sessao
- **Recommended action:** Implantar PIM/JIT; aprovacao por tempo e monitoramento
- **Evidence needed:** Configuracao PIM; logs; politica JIT
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-11-15

### GF-008 - A.8.12 [Alto]
- **Requirement:** Prevenção contra vazamento de dados
- **Observed:** Politica DLP existe mas regras em modo teste sem bloqueio
- **Recommended action:** Passar regras criticas para modo bloqueio com excecoes aprovadas
- **Evidence needed:** DLP policy; modo bloqueio; lista de excecoes aprovadas
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-11-10

### GF-010 - A.8.16 [Alto]
- **Requirement:** Monitoramento e alertas para eventos de seguranca
- **Observed:** SIEM com regras basicas mas sem cobertura para contas privilegiadas e PIX
- **Recommended action:** Ampliar regras para acesso privilegiado; API PIX; exfiltracao
- **Evidence needed:** Regras SIEM; teste de alerta; cobertura
- **Responsible / Target:** Head de SRE / 2026-11-01

### GF-011 - CC6.1 [Alto]
- **Requirement:** Autenticacao forte e controle de acesso
- **Observed:** MFA aplicado mas sem revisão formal de acesso privilegiado por trimestre
- **Recommended action:** Estabelecer revisão trimestral de acessos privilegiados com evidencia
- **Evidence needed:** SOC 2 checklist; relatorio revisao; aprovacao
- **Responsible / Target:** Head de Engenharia de Plataforma / 2026-11-20

### GF-012 - CC6.2 [Alto]
- **Requirement:** Registro de provisionamento e desprovisionamento
- **Observed:** Falta evidencia de tempo entre término e revogacao em 5% das amostras
- **Recommended action:** Automatizar desprovisionamento e medir tempo medio de revogacao
- **Evidence needed:** Evidencias de onboarding/offboarding; metricas; SLA
- **Responsible / Target:** Head de RH/TI / 2026-11-15

## 6) Approach

- **ISO/IEC 27001:2017** - Annex A controls assessed against required evidence.
- **SOC 2 (Security/Availability/Confidentiality)** - mapped to Trust Service Criteria with readiness focus.
- **Evidence-driven** - each gap requires concrete evidence to be considered closed.
- **Risk-based prioritization** - Critical/High first, tracked to due dates.
