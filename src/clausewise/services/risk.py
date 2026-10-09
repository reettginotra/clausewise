from __future__ import annotations

from clausewise.models import ClauseFinding

SEVERITY_WEIGHTS = {'High': 35, 'Medium': 20, 'Low': 10}


def calculate_risk(findings: list[ClauseFinding]) -> tuple[int, str]:
    score = min(100, sum(SEVERITY_WEIGHTS.get(finding.severity, 0) for finding in findings))
    if score >= 70:
        return score, 'High'
    if score >= 40:
        return score, 'Moderate'
    if score > 0:
        return score, 'Low'
    return score, 'Minimal'

