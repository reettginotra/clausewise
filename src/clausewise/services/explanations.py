from __future__ import annotations

from clausewise.models import ClauseFinding


def build_summary(findings: list[ClauseFinding], risk_score: int, risk_label: str, total_estimated_cost: float, llm_status: str) -> str:
    if not findings:
        return 'ClauseWise did not match any current rule patterns. That is not a legal approval. ' + llm_status
    top_titles = ', '.join(finding.title for finding in findings[:3])
    summary = f'ClauseWise flagged {len(findings)} clause(s), giving this contract a {risk_label.lower()} risk profile with a score of {risk_score}/100. The most visible issues include {top_titles}.'
    if total_estimated_cost > 0:
        summary += f' Illustrative estimated cost exposure is about ${total_estimated_cost:,.0f} based on simple heuristics.'
    return summary + ' ' + llm_status

