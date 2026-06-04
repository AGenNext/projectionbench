from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.evaluator import Evaluator
from projectionbench.models import Claim, Hypothesis, JSONLD_CONTEXT


@dataclass(frozen=True)
class ReconciliationResult:
    matched_claims: int
    missed_claims: int
    unsupported_claims: int
    match_ratio: float
    gaps: list[str]
    insights: list[str]
    recommendations: list[str]

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": "pb:reconciliation/latest",
            "@type": ["schema:Action", "pb:Reconciliation"],
            "name": "Claim reconciliation",
            "matchedClaims": self.matched_claims,
            "missedClaims": self.missed_claims,
            "unsupportedClaims": self.unsupported_claims,
            "matchRatio": round(self.match_ratio, 6),
            "hasPart": [
                *[{"@type": ["schema:CreativeWork", "pb:Gap"], "text": gap} for gap in self.gaps],
                *[{"@type": ["schema:CreativeWork", "pb:Insight"], "text": insight} for insight in self.insights],
                *[{"@type": ["schema:Recommendation", "pb:Recommendation"], "text": rec} for rec in self.recommendations],
            ],
        }


class Reconciler:
    def __init__(self, evaluator: Evaluator | None = None):
        self.evaluator = evaluator or Evaluator()

    def reconcile(self, hypotheses: list[Hypothesis], reference_claims: list[Claim]) -> ReconciliationResult:
        generated = [claim for hypothesis in hypotheses for claim in hypothesis.claims]
        matched_reference = [
            ref for ref in reference_claims
            if self.evaluator.best_match(ref, generated) >= self.evaluator.config.match_threshold
        ]
        unsupported_generated = [
            claim for claim in generated
            if self.evaluator.best_match(claim, reference_claims) < self.evaluator.config.match_threshold
        ]
        missed = [ref for ref in reference_claims if ref not in matched_reference]
        match_ratio = len(matched_reference) / len(reference_claims) if reference_claims else 1.0

        gaps = [f"Missed reference claim: {claim.text}" for claim in missed]
        insights = []
        if matched_reference:
            insights.append(f"Matched {len(matched_reference)} reference claim(s) against generated hypotheses.")
        if unsupported_generated:
            insights.append(f"Detected {len(unsupported_generated)} generated claim(s) without sufficient reference alignment.")
        recommendations = []
        if missed:
            recommendations.append("Improve evidence use and claim coverage for missed reference conclusions.")
        if unsupported_generated:
            recommendations.append("Reduce unsupported claims or add stronger evidence links.")
        if not recommendations:
            recommendations.append("Maintain current claim generation strategy and add semantic scoring validation.")

        return ReconciliationResult(
            matched_claims=len(matched_reference),
            missed_claims=len(missed),
            unsupported_claims=len(unsupported_generated),
            match_ratio=match_ratio,
            gaps=gaps,
            insights=insights,
            recommendations=recommendations,
        )
