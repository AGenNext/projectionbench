from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.models import JSONLD_CONTEXT, Score
from projectionbench.reconciliation import ReconciliationResult


@dataclass(frozen=True)
class TrustResult:
    provenance: float
    reproducibility: float
    explainability: float
    verification: float
    confidence: float

    @property
    def trust_score(self) -> float:
        return (self.provenance + self.reproducibility + self.explainability + self.verification + self.confidence) / 5

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": "pb:trust/latest",
            "@type": ["schema:Rating", "pb:TrustScore"],
            "name": "Evaluation trust score",
            "ratingValue": round(self.trust_score, 6),
            "bestRating": 1,
            "worstRating": 0,
            "additionalProperty": [
                {"@type": ["schema:PropertyValue", "pb:TrustMetric"], "name": "provenance", "value": self.provenance},
                {"@type": ["schema:PropertyValue", "pb:TrustMetric"], "name": "reproducibility", "value": self.reproducibility},
                {"@type": ["schema:PropertyValue", "pb:TrustMetric"], "name": "explainability", "value": self.explainability},
                {"@type": ["schema:PropertyValue", "pb:TrustMetric"], "name": "verification", "value": self.verification},
                {"@type": ["schema:PropertyValue", "pb:TrustMetric"], "name": "confidence", "value": self.confidence},
            ],
        }


class TrustEngine:
    """Computes a conservative trust score for a benchmark run."""

    def evaluate(self, *, has_source: bool, has_scenario: bool, has_score: bool, has_reconciliation: bool, deterministic: bool = True) -> TrustResult:
        provenance = 1.0 if has_source and has_scenario else 0.5 if has_scenario else 0.0
        reproducibility = 1.0 if deterministic and has_scenario else 0.5
        explainability = 1.0 if has_score and has_reconciliation else 0.5 if has_score else 0.0
        verification = 0.5  # self-verifiable foundation; external verification not implemented yet
        confidence = (provenance + reproducibility + explainability + verification) / 4
        return TrustResult(provenance, reproducibility, explainability, verification, confidence)


@dataclass(frozen=True)
class EvaluationReport:
    overall: float
    trust: float
    strengths: list[str]
    weaknesses: list[str]
    gaps: list[str]
    recommendations: list[str]

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": "pb:report/latest",
            "@type": ["schema:Report", "pb:EvaluationReport"],
            "name": "ProjectionBench Evaluation Report",
            "ratingValue": round(self.overall, 6),
            "trustScore": round(self.trust, 6),
            "hasPart": [
                *[{"@type": ["schema:CreativeWork", "pb:Strength"], "text": item} for item in self.strengths],
                *[{"@type": ["schema:CreativeWork", "pb:Weakness"], "text": item} for item in self.weaknesses],
                *[{"@type": ["schema:CreativeWork", "pb:Gap"], "text": item} for item in self.gaps],
                *[{"@type": ["schema:Recommendation", "pb:Recommendation"], "text": item} for item in self.recommendations],
            ],
        }


class ReportEngine:
    def build(self, score: Score, reconciliation: ReconciliationResult, trust: TrustResult) -> EvaluationReport:
        metrics = {metric.name: metric.value for metric in score.metrics}
        strengths: list[str] = []
        weaknesses: list[str] = []

        if metrics.get("claim_f1", 0) >= 0.7:
            strengths.append("Generated claims align strongly with reference claims.")
        else:
            weaknesses.append("Generated claims need stronger alignment with reference claims.")

        if metrics.get("groundedness", 0) >= 0.7:
            strengths.append("Generated claims are grounded in disclosed evidence.")
        else:
            weaknesses.append("Grounding should be improved by linking claims to disclosed evidence.")

        if metrics.get("consistency", 0) >= 0.9:
            strengths.append("Generated claims are internally consistent.")
        else:
            weaknesses.append("Generated claims contain possible contradictions or instability.")

        return EvaluationReport(
            overall=score.overall,
            trust=trust.trust_score,
            strengths=strengths,
            weaknesses=weaknesses,
            gaps=reconciliation.gaps,
            recommendations=reconciliation.recommendations,
        )
