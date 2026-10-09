from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from clausewise.services.analysis import analyze_document
from clausewise.services.extraction import UnsupportedFileTypeError, extract_document_bytes
from clausewise.services.reports import build_pdf_report

st.set_page_config(page_title='ClauseWise', page_icon='CW', layout='wide')
st.title('ClauseWise')
st.caption('Explainable consumer contract analysis for a hackathon MVP.')

left, middle, right = st.columns(3)
left.metric('Engine', 'Rule-based')
middle.metric('Files', 'PDF / DOCX / TXT')
right.metric('Output', 'PDF report')

st.markdown('Upload a contract, extract its text, flag risky clauses, and keep every finding tied to a visible source reference.')

uploaded_file = st.file_uploader('Upload contract', type=['pdf', 'docx', 'txt'])

if uploaded_file and st.button('Analyze contract', type='primary'):
    try:
        segments = extract_document_bytes(uploaded_file.name, uploaded_file.getvalue())
        result = analyze_document(segments)
    except UnsupportedFileTypeError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error(f'ClauseWise could not parse this file yet: {exc}')
        st.stop()

    st.success('Analysis complete.')
    a, b, c = st.columns(3)
    a.metric('Risk score', f'{result.risk_score}/100', result.risk_label)
    b.metric('Flagged clauses', len(result.findings))
    c.metric('References', len(segments))

    st.info(result.llm_status)
    st.write(result.summary)

    if result.findings:
        st.dataframe(
            [
                {
                    'Clause': finding.title,
                    'Severity': finding.severity,
                    'Reference': finding.source_reference,
                    'Matched text': finding.matched_text,
                }
                for finding in result.findings
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.write('No current rules matched. That does not mean the contract is safe.')

    if result.cost_items:
        st.write(f'Illustrative estimated cost exposure: ${result.total_estimated_cost:,.0f}')

    for segment in segments[:8]:
        with st.expander(segment.reference):
            st.write(segment.text)

    st.download_button(
        'Download PDF report',
        data=build_pdf_report(result, uploaded_file.name),
        file_name=f'clausewise-report-{Path(uploaded_file.name).stem}.pdf',
        mime='application/pdf',
        type='primary',
    )

