from clausewise.models import TextSegment
from clausewise.services.detection import detect_clauses


def test_detects_multiple_known_clause_types() -> None:
    segments = [
        TextSegment('txt', 'sample.txt', 'This agreement renews automatically unless you give 30 days prior written notice.', 'Line 1'),
        TextSegment('txt', 'sample.txt', 'All disputes must be resolved by binding arbitration and include a class action waiver.', 'Line 2'),
    ]
    findings = detect_clauses(segments)
    clause_types = {finding.clause_type for finding in findings}
    assert 'auto_renewal' in clause_types
    assert 'termination_notice' in clause_types
    assert 'mandatory_arbitration' in clause_types

