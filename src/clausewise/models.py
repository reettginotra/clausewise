from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TextSegment:
    source_type: str
    source_label: str
    text: str
    reference: str


@dataclass(slots=True)
class ClauseFinding:
    clause_type: str
    title: str
    severity: str
    matched_text: str
    explanation: str
    source_reference: str


@dataclass(slots=True)
class CostItem:
    label: str
    estimated_amount: float
    reason: str


@dataclass(slots=True)
class AnalysisResult:
    findings: list[ClauseFinding]
    summary: str
    llm_status: str
    risk_score: int
    risk_label: str
    cost_items: list[CostItem]
    total_estimated_cost: float

