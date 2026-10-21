"""Scales for gap analysis."""

from __future__ import annotations

MATURITY = {0: "Nao existente", 1: "Inicial", 2: "Gerenciado", 3: "Definido", 4: "Gerenciado quantitativamente", 5: "Otimizado"}
MATURITY_EN = {0: "Non-existent", 1: "Initial", 2: "Managed", 3: "Defined", 4: "Quantitatively managed", 5: "Optimizing"}

GAP_SEVERITY = ("Informativo", "Baixo", "Alto", "Crítico")
GAP_SEVERITY_EN = {"Informativo": "Informational", "Baixo": "Low", "Alto": "High", "Crítico": "Critical"}

FINDING_STATUS = ("Aberto", "Em andamento", "Aguardando evidencia", "Fechado", "Aceito com risco")

SEVERITY_ORDER = {"Informativo": 1, "Baixo": 2, "Alto": 3, "Crítico": 4}


def maturity_label(level: int) -> str:
    if level not in MATURITY:
        raise ValueError(f"maturity level must be 0-5 (got {level})")
    return MATURITY[level]


def gap_score(current: int, target: int) -> int:
    if not 0 <= current <= 5 or not 0 <= target <= 5:
        raise ValueError("maturity levels must be 0-5")
    return max(0, target - current)


def readiness_pct(current: int, target: int) -> float:
    if target <= 0:
        return 100.0
    if current >= target:
        return 100.0
    return round(current / target * 100, 1)
