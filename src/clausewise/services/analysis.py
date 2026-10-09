from __future__ import annotations

from clausewise.models import AnalysisResult, TextSegment
from clausewise.services.costs import estimate_costs
from clausewise.services.detection import detect_clauses
from clausewise.services.explanations import build_summary
from clausewise.services.llm import get_llm_status
from clausewise.services.risk import calculate_risk


def analyze_document(segments: list[TextSegment]) -> AnalysisResult:
    findings = detect_clauses(segments)
    risk_score, risk_label = calculate_risk(findings)
    cost_items, total_estimated_cost = estimate_costs(findings)
    llm_status = get_llm_status()
    summary = build_summary(findings, risk_score, risk_label, total_estimated_cost, llm_status)
    return AnalysisResult(findings, summary, llm_status, risk_score, risk_label, cost_items, total_estimated_cost)

