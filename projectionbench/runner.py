from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from projectionbench.baseline import BaselineTheoryAgent
from projectionbench.evaluator import Evaluator
from projectionbench.models import JSONLD_CONTEXT, Scenario


class BenchmarkRunner:
    def __init__(self, agent: BaselineTheoryAgent | None = None, evaluator: Evaluator | None = None):
        self.agent = agent or BaselineTheoryAgent()
        self.evaluator = evaluator or Evaluator()

    def run_file(self, scenario_path: str | Path) -> dict[str, Any]:
        path = Path(scenario_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return self.run_dict(data)

    def run_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        scenario = Scenario.from_dict(data)
        hypotheses = self.agent.generate(scenario)
        disclosed_text = "\n".join(stage.content for stage in scenario.disclosure_stages)
        score = self.evaluator.score(hypotheses, scenario.reference_claims, disclosed_text)

        return {
            "@context": JSONLD_CONTEXT,
            "@id": f"pb:evaluation-run/{scenario.id.split('/')[-1]}",
            "@type": ["schema:Action", "pb:EvaluationRun"],
            "name": f"Evaluation run for {scenario.name}",
            "object": scenario.to_jsonld(),
            "agent": {
                "@id": "pb:agent/baseline-theory-agent",
                "@type": ["schema:SoftwareApplication", "pb:EvaluatorAgent"],
                "name": "Baseline Theory Agent",
            },
            "result": {
                "hypotheses": [hypothesis.to_jsonld() for hypothesis in hypotheses],
                "score": score.to_jsonld(),
            },
            "hasScore": score.to_jsonld(),
        }
