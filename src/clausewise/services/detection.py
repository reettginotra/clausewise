from __future__ import annotations

import re
from dataclasses import dataclass

from clausewise.models import ClauseFinding, TextSegment


@dataclass(frozen=True, slots=True)
class ClauseRule:
    clause_type: str
    title: str
    severity: str
    pattern: str
    explanation: str


RULES: tuple[ClauseRule, ...] = (
    ClauseRule('auto_renewal', 'Automatic renewal', 'Medium', r'\b(auto[- ]?renew(?:al)?|renews? automatically|automatic renewal)\b', 'Automatic renewals can keep a customer locked in unless they cancel on time.'),
    ClauseRule('termination_notice', 'Strict notice period', 'Medium', r'\b(30|60|90)\s+days?\s+(prior\s+written\s+notice|notice required)\b', 'Long notice periods can make cancellation harder.'),
    ClauseRule('mandatory_arbitration', 'Mandatory arbitration or class-action waiver', 'High', r'\b(binding arbitration|mandatory arbitration|class action waiver|waive (your )?right to sue)\b', 'Arbitration or class-action waivers can limit legal options.'),
    ClauseRule('unilateral_changes', 'One-sided changes', 'High', r'\b(reserve the right to modify|we may change (these )?terms at any time|sole discretion)\b', 'One-sided change clauses let the company alter terms without balanced consent.'),
    ClauseRule('early_termination_fee', 'Early termination fee', 'High', r'\b(early termination fee|early cancellation fee|must pay the remaining balance|termination fee)\b', 'Exit penalties can create unexpected costs.'),
    ClauseRule('late_fee', 'Late fee or overdue penalty', 'Low', r'\b(late fee|overdue amount|interest on unpaid balances|penalty for late payment)\b', 'Late fees can increase the real cost of the contract.'),
    ClauseRule('data_sharing', 'Broad data sharing', 'Medium', r'\b(share (your )?data with third parties|sell your data|marketing partners|third-party advertisers)\b', 'Broad data-sharing language can weaken privacy protections.'),
)


def detect_clauses(segments: list[TextSegment]) -> list[ClauseFinding]:
    findings: list[ClauseFinding] = []
    for segment in segments:
        for rule in RULES:
            match = re.search(rule.pattern, segment.text, flags=re.IGNORECASE)
            if match:
                findings.append(
                    ClauseFinding(rule.clause_type, rule.title, rule.severity, _excerpt(segment.text, match.start(), match.end()), rule.explanation, segment.reference)
                )
    return findings


def _excerpt(text: str, start: int, end: int, window: int = 70) -> str:
    return text[max(0, start - window):min(len(text), end + window)].strip()

