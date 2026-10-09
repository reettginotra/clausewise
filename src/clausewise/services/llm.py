from __future__ import annotations

import os


def get_llm_status() -> str:
    if os.getenv('OPENAI_API_KEY'):
        return 'API key detected, but LLM enrichment is not wired into this MVP yet. Results shown here are rule-based only.'
    return 'LLM unavailable. ClauseWise is currently using explainable rule-based detection only.'

