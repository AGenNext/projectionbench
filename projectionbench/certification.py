from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.models import JSONLD_CONTEXT
from projectionbench.score_engine import FinalScore


@dataclass(frozen=True)
class CapabilityCertificate:
    subject: str
    capability: str
    profile: str
    overall_score: float
    trust_score: float
    rating: str
    status: str

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": f"pb:certificate/{self.profile}/{self.subject}".replace(" ", "-").lower(),
            "@type": ["schema:CreativeWork", "pb:CapabilityCertificate"],
            "name": f"{self.capability} certificate for {self.subject}",
            "subject": self.subject,
            "capability": self.capability,
            "profile": self.profile,
            "rating": self.rating,
            "certificationStatus": self.status,
            "overallScore": round(self.overall_score, 6),
            "trustScore": round(self.trust_score, 6),
        }


class CertificationEngine:
    """Turns final scores into capability certification artifacts."""

    def certify(
        self,
        final_score: FinalScore,
        *,
        subject: str = "Baseline Theory Agent",
        capability: str = "Progressive Hypothesis Generation",
        profile: str = "ProjectionBench",
    ) -> CapabilityCertificate:
        return CapabilityCertificate(
            subject=subject,
            capability=capability,
            profile=profile,
            overall_score=final_score.overall_score,
            trust_score=final_score.trust_score,
            rating=final_score.rating,
            status=final_score.certification_status,
        )
