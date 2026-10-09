from clausewise.models import TextSegment
from clausewise.services.analysis import analyze_document


def test_analysis_returns_risk_and_cost_summary() -> None:
    segments = [
        TextSegment('txt', 'contract.txt', 'We reserve the right to modify these terms at any time in our sole discretion.', 'Line 4'),
        TextSegment('txt', 'contract.txt', 'An early termination fee applies and you must pay the remaining balance.', 'Line 7'),
    ]
    result = analyze_document(segments)
    assert result.risk_score >= 70
    assert result.risk_label == 'High'
    assert result.total_estimated_cost >= 150
    assert 'rule-based' in result.llm_status.lower()

