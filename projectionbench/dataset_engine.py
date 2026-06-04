from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from projectionbench.models import JSONLD_CONTEXT, Scenario


@dataclass(frozen=True)
class DatasetSummary:
    id: str
    name: str
    version: str
    domain: str
    license: str
    scenario_count: int
    coverage: dict[str, float]

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@context": JSONLD_CONTEXT,
            "@id": self.id,
            "@type": ["schema:Dataset", "pb:BenchmarkDataset"],
            "name": self.name,
            "version": self.version,
            "domain": self.domain,
            "license": self.license,
            "scenarioCount": self.scenario_count,
            "coverage": self.coverage,
        }


class DatasetEngine:
    """Loads and summarizes benchmark datasets made of scenario JSON files."""

    def summarize_directory(
        self,
        directory: str | Path,
        *,
        dataset_id: str = "pb:dataset/local",
        name: str = "Local ProjectionBench Dataset",
        version: str = "0.1.0",
        license: str = "Apache-2.0",
    ) -> DatasetSummary:
        path = Path(directory)
        scenarios = []
        for file in sorted(path.glob("*.json")):
            data = json.loads(file.read_text(encoding="utf-8"))
            scenarios.append(Scenario.from_dict(data))

        domains = {scenario.domain for scenario in scenarios}
        total_reference_claims = sum(len(s.reference_claims) for s in scenarios)
        total_stages = sum(len(s.disclosure_stages) for s in scenarios)

        coverage = {
            "domain_coverage": min(1.0, len(domains) / 5) if scenarios else 0.0,
            "scenario_coverage": min(1.0, len(scenarios) / 50),
            "claim_coverage": min(1.0, total_reference_claims / 200),
            "disclosure_stage_coverage": min(1.0, total_stages / 200),
        }

        return DatasetSummary(
            id=dataset_id,
            name=name,
            version=version,
            domain=", ".join(sorted(domains)) if domains else "unknown",
            license=license,
            scenario_count=len(scenarios),
            coverage=coverage,
        )
