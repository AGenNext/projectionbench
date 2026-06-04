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

    The evaluator computes benchmark quality. The score engine applies final
    aggregation, rating bands, and certification status.
    """

    def __init__(self, benchmark_weight: float = 0.80, trust_weight: float = 0.20):
        self.benchmark_weight = benchmark_weight
        self.trust_weight = trust_weight

    def finalize(self, score: Score, trust: TrustResult) -> FinalScore:
        benchmark_score = score.overall
        trust_score = trust.trust_score
        overall = (benchmark_score * self.benchmark_weight) + (trust_score * self.trust_weight)
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

    def _band(self, value: float) -> tuple[str, str]:
        for threshold, rating, status in RATING_BANDS:
            if value >= threshold:
                return rating, status
        return "F", "not_certified"
