from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JSONLD_CONTEXT = {
    "schema": "https://schema.org/",
    "pb": "https://github.com/AGenNext/projectionbench/ns#",
    "hasClaim": "pb:hasClaim",
    "hasScore": "pb:hasScore",
    "hasDisclosureStage": "pb:hasDisclosureStage",
}


@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    stage: str | None = None
    confidence: float = 1.0

    def tokens(self) -> set[str]:
        return tokenize(self.text)

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@id": self.id,
            "@type": ["schema:Claim", "pb:Claim"],
            "claimReviewed": self.text,
            "stage": self.stage,
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class DisclosureStage:
    id: str
    name: str
    content: str
    position: int

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@id": self.id,
            "@type": ["schema:CreativeWork", "pb:DisclosureStage"],
            "name": self.name,
            "text": self.content,
            "position": self.position,
        }


@dataclass(frozen=True)
class Scenario:
    id: str
    name: str
    domain: str
    theory_seed: str
    evaluation_goal: str
    disclosure_stages: list[DisclosureStage]
    reference_claims: list[Claim]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scenario":
        stages = [
            DisclosureStage(
                id=s.get("@id", s.get("id", f"pb:stage/{idx + 1}")),
                name=s["name"],
                content=s["content"],
                position=int(s.get("position", idx + 1)),
            )
            for idx, s in enumerate(data.get("disclosure_stages", data.get("hasDisclosureStage", [])))
        ]
        refs = [
            Claim(
                id=c.get("@id", c.get("id", f"pb:reference-claim/{idx + 1}")),
                text=c.get("text", c.get("claimReviewed", "")),
                stage=c.get("stage"),
                confidence=float(c.get("confidence", 1.0)),
            )
            for idx, c in enumerate(data.get("reference_claims", data.get("hasReferenceClaim", [])))
        ]
        return cls(
            id=data.get("@id", data.get("id", "pb:scenario/unknown")),
            name=data["name"],
            domain=data.get("domain", "generic"),
            theory_seed=data.get("theory_seed", data.get("theorySeed", "")),
            evaluation_goal=data.get("evaluation_goal", data.get("evaluationGoal", "")),
            disclosure_stages=stages,
            reference_claims=refs,
        )

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": self.id,
            "@type": ["schema:Dataset", "pb:BenchmarkScenario"],
            "name": self.name,
            "description": self.evaluation_goal,
            "domain": self.domain,
            "theorySeed": self.theory_seed,
            "hasDisclosureStage": [s.to_jsonld() for s in self.disclosure_stages],
            "hasReferenceClaim": [c.to_jsonld() for c in self.reference_claims],
        }


@dataclass(frozen=True)
class Hypothesis:
    id: str
    stage: str
    text: str
    claims: list[Claim] = field(default_factory=list)

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@id": self.id,
            "@type": ["schema:CreativeWork", "pb:Hypothesis"],
            "name": f"Hypothesis {self.stage}",
            "text": self.text,
            "stage": self.stage,
            "hasClaim": [c.to_jsonld() for c in self.claims],
        }


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    weight: float = 1.0
    description: str = ""

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@type": ["schema:PropertyValue", "pb:Metric"],
            "name": self.name,
            "value": round(self.value, 6),
            "weight": self.weight,
            "description": self.description,
            "unitText": "normalized-score",
        }


@dataclass(frozen=True)
class Score:
    id: str
    metrics: list[Metric]

    @property
    def overall(self) -> float:
        total_weight = sum(m.weight for m in self.metrics) or 1.0
        return sum(m.value * m.weight for m in self.metrics) / total_weight

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": self.id,
            "@type": ["schema:Rating", "pb:Score"],
            "ratingValue": round(self.overall, 6),
            "bestRating": 1,
            "worstRating": 0,
            "additionalProperty": [m.to_jsonld() for m in self.metrics],
        }


def tokenize(text: str) -> set[str]:
    stopwords = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "of", "on", "or", "that", "the", "to", "under", "with", "will", "should", "can"
    }
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {token for token in cleaned.split() if len(token) > 2 and token not in stopwords}
