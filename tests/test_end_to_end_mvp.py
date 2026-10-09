from __future__ import annotations

from pathlib import Path

import fitz
from streamlit.testing.v1 import AppTest

from clausewise.services.analysis import analyze_document
from clausewise.services.extraction import extract_document_bytes
from clausewise.services.reports import build_pdf_report

FICTIONAL_CONTRACT_TEXT = (
    'This membership renews automatically at the end of each billing term.\n'
    'To cancel, you must provide 30 days prior written notice before the renewal date.\n'
    'Any dispute will be resolved by binding arbitration and include a class action waiver.\n'
    'If you cancel early, an early termination fee applies.\n'
    'A late fee may be charged on overdue balances.\n'
)

FICTIONAL_CONTRACT_BYTES = FICTIONAL_CONTRACT_TEXT.encode('utf-8')

EXPECTED_FINDINGS = [
    {
        'Clause': 'Automatic renewal',
        'Severity': 'Medium',
        'Reference': 'Line 1',
        'Matched text': 'This membership renews automatically at the end of each billing term.',
    },
    {
        'Clause': 'Strict notice period',
        'Severity': 'Medium',
        'Reference': 'Line 2',
        'Matched text': 'To cancel, you must provide 30 days prior written notice before the renewal date.',
    },
    {
        'Clause': 'Mandatory arbitration or class-action waiver',
        'Severity': 'High',
        'Reference': 'Line 3',
        'Matched text': 'Any dispute will be resolved by binding arbitration and include a class action waiver.',
    },
    {
        'Clause': 'Early termination fee',
        'Severity': 'High',
        'Reference': 'Line 4',
        'Matched text': 'If you cancel early, an early termination fee applies.',
    },
    {
        'Clause': 'Late fee or overdue penalty',
        'Severity': 'Low',
        'Reference': 'Line 5',
        'Matched text': 'A late fee may be charged on overdue balances.',
    },
]

EXPECTED_LLM_DISCLOSURE = 'LLM unavailable. ClauseWise is currently using explainable rule-based detection only.'
APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'


def test_fictional_contract_extracts_and_detects_known_rules() -> None:
    segments = extract_document_bytes('fictional-consumer-contract.txt', FICTIONAL_CONTRACT_BYTES)

    assert [segment.reference for segment in segments] == ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5']
    assert [segment.text for segment in segments] == FICTIONAL_CONTRACT_TEXT.strip().splitlines()

    result = analyze_document(segments)
    findings_table = [
        {
            'Clause': finding.title,
            'Severity': finding.severity,
            'Reference': finding.source_reference,
            'Matched text': finding.matched_text,
        }
        for finding in result.findings
    ]

    assert findings_table == EXPECTED_FINDINGS
    assert result.risk_score == 100
    assert result.risk_label == 'High'
    assert result.llm_status == EXPECTED_LLM_DISCLOSURE
    assert result.total_estimated_cost == 305.0


def test_pdf_report_contains_same_findings_as_analysis() -> None:
    segments = extract_document_bytes('fictional-consumer-contract.txt', FICTIONAL_CONTRACT_BYTES)
    result = analyze_document(segments)

    pdf_bytes = build_pdf_report(result, 'fictional-consumer-contract.txt')
    document = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        report_text = ''.join(page.get_text('text') for page in document)
    finally:
        document.close()

    normalized_report_text = ' '.join(report_text.split())

    assert 'ClauseWise Contract Analysis Report' in report_text
    assert 'Risk score: 100/100 (High)' in report_text
    assert EXPECTED_LLM_DISCLOSURE in report_text

    for finding in EXPECTED_FINDINGS:
        assert finding['Clause'] in report_text
        assert finding['Reference'] in report_text
        assert ' '.join(finding['Matched text'].split()) in normalized_report_text


def test_streamlit_app_renders_end_to_end_results_for_known_contract() -> None:
    app = AppTest.from_file(APP_PATH)

    app.run(timeout=10)
    app.file_uploader[0].upload('fictional-consumer-contract.txt', FICTIONAL_CONTRACT_BYTES, 'text/plain')
    app.run(timeout=10)
    app.button[0].click()
    app.run(timeout=15)

    metrics = {metric.proto.label: (metric.proto.body, metric.proto.delta) for metric in app.metric}
    assert metrics['Risk score'] == ('100/100', 'High')
    assert metrics['Flagged clauses'] == ('5', '')
    assert metrics['References'] == ('5', '')

    assert [info.proto.body for info in app.info] == [EXPECTED_LLM_DISCLOSURE]
    assert [success.proto.body for success in app.success] == ['Analysis complete.']
    assert [expander.proto.label for expander in app.expander] == ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5']
    assert len(app.download_button) == 1

    findings_table = app.dataframe[0].value.to_dict(orient='records')
    assert findings_table == EXPECTED_FINDINGS

