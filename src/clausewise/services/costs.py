from __future__ import annotations

from clausewise.models import ClauseFinding, CostItem

ESTIMATED_COSTS = {
    'auto_renewal': (120.0, 'Estimated extra charge if the plan renews unexpectedly.'),
    'early_termination_fee': (150.0, 'Representative cancellation penalty for a basic consumer service contract.'),
    'late_fee': (35.0, 'Representative fee exposure from a missed payment.'),
}


def estimate_costs(findings: list[ClauseFinding]) -> tuple[list[CostItem], float]:
    cost_items: list[CostItem] = []
    seen_clause_types: set[str] = set()
    for finding in findings:
        if finding.clause_type in seen_clause_types or finding.clause_type not in ESTIMATED_COSTS:
            continue
        amount, reason = ESTIMATED_COSTS[finding.clause_type]
        cost_items.append(CostItem(finding.title, amount, reason))
        seen_clause_types.add(finding.clause_type)
    return cost_items, sum(item.estimated_amount for item in cost_items)

