# ProjectionBench

**ProjectionBench** is an executable benchmark framework for evaluating scientific hypothesis generation in language models under progressive information disclosure.

This repository is grounded in the arXiv paper **ProjectionBench: Evaluating Scientific Hypothesis Generation in LLMs Under Progressive Information Disclosure** by A. J. Lew, Y. Cao, and M. J. Buehler, submitted on 28 May 2026 as arXiv:2605.30284.

Source: https://arxiv.org/abs/2605.30284

## Core Hypothesis

A language model should not only be evaluated on whether it can recall or summarize known scientific conclusions. It should also be evaluated on whether it can generate plausible, innovative, and progressively grounded hypotheses as information is gradually disclosed.

ProjectionBench evaluates that capability.

## Benchmark Pattern

```text
Topic + research question
  -> initial hypothesis
  -> disclose background
  -> revised hypothesis
  -> disclose methods
  -> revised hypothesis
  -> disclose results
  -> final hypothesis
  -> compare with reference conclusion
```

## What This Repo Builds

- Scenario schema for progressive disclosure scientific reasoning tasks.
- Baseline hypothesis agent.
- Claim-level evaluator.
- Stage-wise scoring model.
- CLI runner.
- Example benchmark scenario.
- Tests and CI.

## Quick Start

```bash
pip install -e .
projectionbench run scenarios/example-biomaterial.json
```

Or:

```bash
python -m projectionbench.cli run scenarios/example-biomaterial.json
```

## Scoring Outputs

The evaluator reports:

- `claim_precision`
- `claim_recall`
- `claim_f1`
- `stage_improvement`
- `groundedness`
- `novelty`
- `consistency`
- `overall`

## Status

This is an executable foundation. It is not a full reproduction of the paper dataset or semantic evaluation pipeline yet. It provides the repo scaffold required to add model adapters, real paper tasks, semantic similarity models, and leaderboard workflows.

## License

Apache-2.0.
