from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from projectionbench.models import Claim, Hypothesis, Metric, Score, tokenize


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass(frozen=True)
class EvaluationConfig:
    match_threshold: float = 0.35


class Evaluator:
    """Deterministic claim-level evaluator.

    This intentionally starts simple and reproducible. Later versions can swap the
    token overlap matcher with embedding or LLM-based semantic claim matching.
    """

    def __init__(self, config: EvaluationConfig | None = None):
        self.config = config or EvaluationConfig()

    def score(self, hypotheses: list[Hypothesis], reference_claims: list[Claim], disclosed_text: str = "") -> Score:
        generated_claims = [claim for hypothesis in hypotheses for claim in hypothesis.claims]
        precision = self.claim_precision(generated_claims, reference_claims)
        recall = self.claim_recall(generated_claims, reference_claims)
        f1 = harmonic_mean(precision, recall)
        stage_improvement = self.stage_improvement(hypotheses, reference_claims)
        groundedness = self.groundedness(generated_claims, disclosed_text)
        novelty = self.novelty(generated_claims)
        consistency = self.consistency(generated_claims)

        metrics = [
            Metric("claim_precision", precision, 0.15, "Generated claims aligned to reference claims."),
            Metric("claim_recall", recall, 0.15, "Reference claims covered by generated claims."),
            Metric("claim_f1", f1, 0.30, "Claim-level F1 alignment."),
            Metric("stage_improvement", stage_improvement, 0.10, "Improvement from first to final disclosure stage."),
            Metric("groundedness", groundedness, 0.15, "Claims grounded in disclosed evidence."),
            Metric("novelty", novelty, 0.10, "Non-generic claim quality."),
            Metric("consistency", consistency, 0.15, "Internal contradiction avoidance."),
        ]
        return Score("pb:score/latest", metrics)

    def claim_precision(self, generated: list[Claim], reference: list[Claim]) -> float:
        if not generated:
            return 0.0
        matches = sum(1 for claim in generated if self.best_match(claim, reference) >= self.config.match_threshold)
        return matches / len(generated)

    def claim_recall(self, generated: list[Claim], reference: list[Claim]) -> float:
        if not reference:
            return 1.0
        matches = sum(1 for ref in reference if self.best_match(ref, generated) >= self.config.match_threshold)
        return matches / len(reference)

    def stage_improvement(self, hypotheses: list[Hypothesis], reference: list[Claim]) -> float:
        if len(hypotheses) < 2:
            return 0.0
        first = hypotheses[0].claims
        final = hypotheses[-1].claims
        first_f1 = harmonic_mean(self.claim_precision(first, reference), self.claim_recall(first, reference))
        final_f1 = harmonic_mean(self.claim_precision(final, reference), self.claim_recall(final, reference))
        return clamp((final_f1 - first_f1 + 1) / 2)

    def groundedness(self, generated: list[Claim], disclosed_text: str) -> float:
        if not generated:
            return 0.0
        evidence_tokens = tokenize(disclosed_text)
        if not evidence_tokens:
            return 0.0
        grounded = sum(1 for claim in generated if jaccard(claim.tokens(), evidence_tokens) >= 0.10)
        return grounded / len(generated)

    def novelty(self, generated: list[Claim]) -> float:
        if not generated:
            return 0.0
        generic_terms = {"improve", "increase", "decrease", "better", "effective", "important", "significant"}
        non_generic = 0
        for claim in generated:
            tokens = claim.tokens()
            if len(tokens - generic_terms) >= 4:
                non_generic += 1
        return non_generic / len(generated)

    def consistency(self, generated: list[Claim]) -> float:
        if len(generated) < 2:
            return 1.0
        contradictions = 0
        pairs = 0
        for i, left in enumerate(generated):
            for right in generated[i + 1:]:
                pairs += 1
                if simple_contradiction(left.text, right.text):
                    contradictions += 1
        return 1.0 if pairs == 0 else 1 - contradictions / pairs

    def best_match(self, claim: Claim, candidates: Iterable[Claim]) -> float:
        scores = [jaccard(claim.tokens(), candidate.tokens()) for candidate in candidates]
        return max(scores, default=0.0)


def harmonic_mean(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def simple_contradiction(a: str, b: str) -> bool:
    left = a.lower()
    right = b.lower()
    negations = [("increase", "decrease"), ("improves", "reduces"), ("supports", "contradicts"), ("enhances", "impairs")]
    shared = tokenize(a) & tokenize(b)
    if len(shared) < 2:
        return False
    return any((x in left and y in right) or (y in left and x in right) for x, y in negations)
