# ClauseWise

ClauseWise is a hackathon-friendly consumer contract analysis app built with Streamlit and Python. It starts with explainable, rule-based clause detection so you can demo an end-to-end MVP before layering on optional LLM features.

## What this MVP does

- Uploads `PDF`, `DOCX`, or `TXT` contracts
- Extracts text with source references where available
- Detects potentially risky consumer clauses with regex rules
- Scores risk in a transparent, explainable way
- Estimates possible cost exposure for selected clause types
- Generates a downloadable PDF summary report
- Clearly labels LLM support as unavailable unless it is actually wired in later

## Project structure

```text
.
├── app.py
├── requirements.txt
├── src/
│   └── clausewise/
│       ├── __init__.py
│       ├── models.py
│       └── services/
│           ├── analysis.py
│           ├── costs.py
│           ├── detection.py
│           ├── explanations.py
│           ├── extraction.py
│           ├── llm.py
│           ├── reports.py
│           └── risk.py
└── tests/
    ├── conftest.py
    ├── test_analysis.py
    ├── test_detection.py
    └── test_extraction.py
```

## Why the architecture looks like this

- `app.py`: presentation layer only
- `extraction.py`: file parsing and source references
- `detection.py`: regex-based clause detection rules
- `risk.py`: scoring logic that judges can understand easily
- `costs.py`: simple consumer cost exposure estimates
- `explanations.py`: plain-English summaries
- `reports.py`: downloadable PDF output
- `llm.py`: reserved integration point for future AI enrichment

This separation makes the demo easier to defend: the UI collects a file, the services analyze it, and the report module exports the result.

## Setup

Activate the project virtual environment from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
streamlit run app.py
```

Expected local URL:

- `http://localhost:8501`

## Current limitations

- Detection is rule-based only in this milestone
- `DOCX` extraction preserves paragraph references, not real page numbers
- Cost estimates are rough educational signals, not legal or financial advice
- LLM enrichment is intentionally not simulated or faked

## Security notes

- Do not commit API keys
- Do not store confidential contracts in the repository
- Keep `.env` local only

