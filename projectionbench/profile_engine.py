from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.models import JSONLD_CONTEXT


@dataclass(frozen=True)
class BenchmarkProfile:
    id: str
    name: str
    objective: str
    constraints: list[str]
    metric_weights: dict[str, float]
    trust_weight: float = 0.20
    benchmark_weight: float = 0.80
    certification_threshold: float = 0.90

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": self.id,
            "@type": ["schema:DefinedTerm", "pb:BenchmarkProfile"],
            "name": self.name,
            "objective": self.objective,
            "constraint": self.constraints,
            "metricWeights": self.metric_weights,
            "trustWeight": self.trust_weight,
            "benchmarkWeight": self.benchmark_weight,
            "certificationThreshold": self.certification_threshold,
        }


class ProfileEngine:
    """Resolves benchmark profiles into executable scoring configuration."""

    def __init__(self):
        self._profiles = {
            "projectionbench": BenchmarkProfile(
                id="pb:profile/projectionbench",
                name="ProjectionBench",
                objective="Generate and revise scientific hypotheses as evidence is progressively disclosed.",
                constraints=[
                    "Use only evidence disclosed at or before the current stage.",
                    "Preserve claim provenance.",
                    "Compare generated claims against reference conclusions.",
                ],
                metric_weights={
                    "claim_precision": 0.15,
                    "claim_recall": 0.15,
                    "claim_f1": 0.30,
                    "stage_improvement": 0.10,
                    "groundedness": 0.15,
                    "novelty": 0.10,
                    "consistency": 0.15,
                },
                trust_weight=0.20,
                benchmark_weight=0.80,
                certification_threshold=0.90,
            ),
            "generic-theory": BenchmarkProfile(
                id="pb:profile/generic-theory",
                name="Generic Theory Evaluation",
                objective="Evaluate whether a theory explains, predicts, revises, or guides action in context.",
                constraints=[
                    "State assumptions explicitly.",
                    "Ground claims in available evidence.",
                    "Identify contradictions and gaps.",
                ],
                metric_weights={
                    "claim_precision": 0.15,
                    "claim_recall": 0.15,
                    "claim_f1": 0.25,
                    "stage_improvement": 0.15,
                    "groundedness": 0.15,
                    "novelty": 0.10,
                    "consistency": 0.15,
                },
                trust_weight=0.20,
                benchmark_weight=0.80,
                certification_threshold=0.85,
            ),
        }

    def get(self, profile_name: str = "projectionbench") -> BenchmarkProfile:
        key = profile_name.strip().lower()
        if key not in self._profiles:
            raise ValueError(f"Unknown profile: {profile_name}")
        return self._profiles[key]

    def list_profiles(self) -> list[BenchmarkProfile]:
        return list(self._profiles.values())
