from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.models import JSONLD_CONTEXT, Score
from projectionbench.trust import TrustResult


RATING_BANDS = [
    (0.95, "A+", "certified_excellent"),
    (0.90, "A", "certified"),
    (0.80, "B", "verified"),
    (0.70, "C", "provisional"),
    (0.60, "D", "needs_improvement"),
    (0.00, "F", "not_certified"),
]


@dataclass(frozen=True)
class FinalScore:
    overall_score: float
    benchmark_score: float
    trust_score: float
    rating: str
    certification_status: str
    metrics: dict[str, float]

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": "pb:final-score/latest",
            "@type": ["schema:Rating", "pb:FinalScore"],
            "name": "Final ProjectionBench score",
            "ratingValue": round(self.overall_score, 6),
            "bestRating": 1,
            "worstRating": 0,
            "ratingExplanation": self.rating,
            "certificationStatus": self.certification_status,
            "additionalProperty": [
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": name, "value": value}
                for name, value in self.metrics.items()
            ] + [
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": "benchmark_score", "value": round(self.benchmark_score, 6)},
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": "trust_score", "value": round(self.trust_score, 6)},
            ],
        }


class ScoreEngine:
    """Combines benchmark metrics and trust into a final score.

    The evaluator computes raw metric values. The score engine applies profile
    weights, trust weighting, rating bands, and certification status.
    """

    def __init__(self, benchmark_weight: float = 0.80, trust_weight: float = 0.20, metric_weights: dict[str, float] | None = None):
        self.benchmark_weight = benchmark_weight
        self.trust_weight = trust_weight
        self.metric_weights = metric_weights

    def finalize(self, score: Score, trust: TrustResult) -> FinalScore:
        benchmark_score = self._weighted_benchmark_score(score)
        trust_score = trust.trust_score
        total_weight = self.benchmark_weight + self.trust_weight or 1.0
        overall = ((benchmark_score * self.benchmark_weight) + (trust_score * self.trust_weight)) / total_weight
        rating, status = self._band(overall)
        metrics = {metric.name: round(metric.value, 6) for metric in score.metrics}
        return FinalScore(
            overall_score=overall,
            benchmark_score=benchmark_score,
            trust_score=trust_score,
            rating=rating,
            certification_status=status,
            metrics=metrics,
        )

    def _weighted_benchmark_score(self, score: Score) -> float:
        if not self.metric_weights:
            return score.overall
        metric_values = {metric.name: metric.value for metric in score.metrics}
        total = 0.0
        used_weight = 0.0
        for name, weight in self.metric_weights.items():
            if name in metric_values:
                total += metric_values[name] * weight
                used_weight += weight
        return total / used_weight if used_weight else score.overall

    def _band(self, value: float) -> tuple[str, str]:
        for threshold, rating, status in RATING_BANDS:
            if value >= threshold:
                return rating, status
        return "F", "not_certified"
