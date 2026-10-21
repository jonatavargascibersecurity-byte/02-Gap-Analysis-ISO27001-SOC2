# Análise de Lacunas ISO/IEC 27001:2017 & SOC 2 (Meridian Pay)

Análise de lacunas orientada a evidências para uma fintech brasileira fictícia (**Meridian Pay**), mapeando controles do **Anexo A da ISO/IEC 27001:2017** aos **Critérios de Serviço de Confiança SOC 2 (Segurança/Disponibilidade/Confidencialidade)**.

## Funcionalidades

- **Mapeamento Anexo A**: 25 controles com responsáveis, evidências esperadas e metas de maturidade
- **Prontidão SOC 2**: mapeamento para TSC com foco em achados comuns de auditoria
- **Achados de lacuna**: priorização Crítico/Alto com responsável, prazo e evidências necessárias
- **Tracker de prontidão**: maturidade 0-5 com cálculo de lacuna e cadência de revisão
- **CLI**: `validate`, `summary`, `findings`, `tracker`, `report`, `dashboard`
- **Relatórios**: relatório executivo em Markdown + dashboard HTML autocontido
- **Sem dependências em tempo de execução**: Python puro (stdlib), CSV como fonte única da verdade

## Início rápido

```bash
cd 02-Gap-Analysis-ISO27001-SOC2
pip install -e ".[dev]"
python -m gapanalysis validate
python -m gapanalysis summary
python -m gapanalysis report --out build
python -m gapanalysis dashboard --out build
```

## Estrutura de dados

- `data/scope.csv` - escopo do SGSI e escopo SOC 2
- `data/controls_iso27001.csv` - controles do Anexo A com mapeamento SOC 2
- `data/gap_findings.csv` - achados com severidade, ações e evidências
- `data/readiness_tracker.csv` - acompanhamento de maturidade

## Licença

MIT
