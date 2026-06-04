from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from projectionbench.baseline import BaselineTheoryAgent
from projectionbench.evaluator import Evaluator
from projectionbench.models import JSONLD_CONTEXT, Scenario
from projectionbench.reconciliation import Reconciler
from projectionbench.trust import ReportEngine, TrustEngine


class BenchmarkRunner:
    def __init__(self, agent: BaselineTheoryAgent | None = None, evaluator: Evaluator | None = None):
        self.agent = agent or BaselineTheoryAgent()
        self.evaluator = evaluator or Evaluator()
        self.reconciler = Reconciler(self.evaluator)
        self.trust_engine = TrustEngine()
        self.report_engine = ReportEngine()

    def run_file(self, scenario_path: str | Path) -> dict[str, Any]:
        path = Path(scenario_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return self.run_dict(data)

    def run_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        scenario = Scenario.from_dict(data)
        hypotheses = self.agent.generate(scenario)
        disclosed_text = "\n".join(stage.content for stage in scenario.disclosure_stages)
        score = self.evaluator.score(hypotheses, scenario.reference_claims, disclosed_text)
        reconciliation = self.reconciler.reconcile(hypotheses, scenario.reference_claims)
        trust = self.trust_engine.evaluate(
            has_source=bool(data.get("isBasedOn")),
            has_scenario=True,
            has_score=True,
            has_reconciliation=True,
            deterministic=True,
        )
        report = self.report_engine.build(score, reconciliation, trust)

        score_summary = {
            "overall": round(score.overall, 6),
            "metrics": {metric.name: round(metric.value, 6) for metric in score.metrics},
        }

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
            "scoreSummary": score_summary,
            "trustSummary": {
                "overall": round(trust.trust_score, 6),
                "provenance": trust.provenance,
                "reproducibility": trust.reproducibility,
                "explainability": trust.explainability,
                "verification": trust.verification,
                "confidence": trust.confidence,
            },
            "result": {
                "hypotheses": [hypothesis.to_jsonld() for hypothesis in hypotheses],
                "score": score.to_jsonld(),
                "reconciliation": reconciliation.to_jsonld(),
                "trust": trust.to_jsonld(),
                "report": report.to_jsonld(),
            },
            "hasScore": score.to_jsonld(),
            "hasReport": report.to_jsonld(),
        }
