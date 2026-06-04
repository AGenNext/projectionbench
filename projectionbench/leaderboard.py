from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from projectionbench.models import JSONLD_CONTEXT
from projectionbench.score_engine import FinalScore


@dataclass(frozen=True)
class LeaderboardEntry:
    subject: str
    capability: str
    profile: str
    dataset: str
    final_score: float
    trust_score: float
    coverage_score: float
    rank_score: float
    rank: int | None = None

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": f"pb:leaderboard-entry/{self.profile}/{self.subject}".replace(" ", "-").lower(),
            "@type": ["schema:Rating", "pb:LeaderboardEntry"],
            "name": f"Leaderboard entry for {self.subject}",
            "subject": self.subject,
            "capability": self.capability,
            "profile": self.profile,
            "dataset": self.dataset,
            "ratingValue": round(self.rank_score, 6),
            "bestRating": 1,
            "worstRating": 0,
            "rank": self.rank,
            "additionalProperty": [
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": "final_score", "value": round(self.final_score, 6)},
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": "trust_score", "value": round(self.trust_score, 6)},
                {"@type": ["schema:PropertyValue", "pb:Metric"], "name": "coverage_score", "value": round(self.coverage_score, 6)},
            ],
        }


class LeaderboardEngine:
    """Ranks benchmark runs using score, trust, and coverage.

    Ranking is intentionally not score-only. A high score on a weak or narrow
    dataset should not outrank a slightly lower score on a stronger dataset.
    """

    def __init__(self, score_weight: float = 0.60, trust_weight: float = 0.30, coverage_weight: float = 0.10):
        self.score_weight = score_weight
        self.trust_weight = trust_weight
        self.coverage_weight = coverage_weight

    def create_entry(
        self,
        final_score: FinalScore,
        *,
        subject: str = "Baseline Theory Agent",
        capability: str = "Progressive Hypothesis Generation",
        profile: str = "ProjectionBench",
        dataset: str = "Local Dataset",
        coverage_score: float = 0.0,
    ) -> LeaderboardEntry:
        rank_score = (
            final_score.overall_score * self.score_weight
            + final_score.trust_score * self.trust_weight
            + coverage_score * self.coverage_weight
        )
        return LeaderboardEntry(
            subject=subject,
            capability=capability,
            profile=profile,
            dataset=dataset,
            final_score=final_score.overall_score,
            trust_score=final_score.trust_score,
            coverage_score=coverage_score,
            rank_score=rank_score,
        )

    def rank(self, entries: list[LeaderboardEntry]) -> list[LeaderboardEntry]:
        ordered = sorted(entries, key=lambda item: item.rank_score, reverse=True)
        return [
            LeaderboardEntry(
                subject=item.subject,
                capability=item.capability,
                profile=item.profile,
                dataset=item.dataset,
                final_score=item.final_score,
                trust_score=item.trust_score,
                coverage_score=item.coverage_score,
                rank_score=item.rank_score,
                rank=index + 1,
            )
            for index, item in enumerate(ordered)
        ]
