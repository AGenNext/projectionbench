# SurrealDB In-Memory Agent with GPT-5.5

This document defines a ProjectionBench-compatible in-memory agent pattern using SurrealDB as the transient graph store and GPT-5.5 as the reasoning model identity.

## Purpose

The goal is to run benchmark evaluations without requiring persistent infrastructure.

```text
Scenario
  -> SurrealDB in-memory graph
  -> GPT-5.5 theory agent
  -> Claims
  -> Evaluation
  -> Score
  -> Trust
  -> Report
```

This pattern is useful for:

- local benchmark runs
- CI smoke tests
- fixture generation
- temporary evaluation sessions
- agent memory experiments
- graph-native reasoning traces

## Design Principle

SurrealDB stores the evaluation graph.

GPT-5.5 generates or revises theory artifacts.

ProjectionBench evaluates the artifacts.

```text
SurrealDB = memory and graph state
GPT-5.5   = reasoning identity
Evaluator = scoring and trust system
```

## Agent Identity

```json
{
  "@id": "pb:agent/gpt-5-5-theory-agent",
  "@type": ["schema:SoftwareApplication", "pb:TheoryAgent"],
  "name": "GPT-5.5 Theory Agent",
  "model": "GPT-5.5",
  "memory": "SurrealDB in-memory",
  "mode": "progressive-disclosure-evaluation"
}
```

## In-Memory Runtime

SurrealDB can be used as a temporary datastore for each benchmark run.

Conceptual launch:

```bash
surreal start --log info memory
```

The runtime should be treated as ephemeral unless explicitly exported.

## Graph Tables

```sql
DEFINE TABLE artifact SCHEMAFULL;
DEFINE TABLE scenario SCHEMAFULL;
DEFINE TABLE disclosure_stage SCHEMAFULL;
DEFINE TABLE theory SCHEMAFULL;
DEFINE TABLE hypothesis SCHEMAFULL;
DEFINE TABLE claim SCHEMAFULL;
DEFINE TABLE evidence SCHEMAFULL;
DEFINE TABLE evaluation_run SCHEMAFULL;
DEFINE TABLE score SCHEMAFULL;
DEFINE TABLE trust_score SCHEMAFULL;
DEFINE TABLE report SCHEMAFULL;
DEFINE TABLE certificate SCHEMAFULL;
```

## Graph Relations

```sql
DEFINE TABLE has_claim TYPE RELATION IN theory OUT claim;
DEFINE TABLE based_on TYPE RELATION IN claim OUT evidence;
DEFINE TABLE generated_by TYPE RELATION IN artifact OUT artifact;
DEFINE TABLE evaluated_by TYPE RELATION IN theory OUT evaluation_run;
DEFINE TABLE scored_by TYPE RELATION IN evaluation_run OUT score;
DEFINE TABLE trusted_by TYPE RELATION IN evaluation_run OUT trust_score;
DEFINE TABLE certified_by TYPE RELATION IN evaluation_run OUT certificate;
```

## Minimal Flow

```text
1. Load scenario into SurrealDB memory.
2. Load disclosure stages as graph nodes.
3. Ask GPT-5.5 to generate a hypothesis for each stage.
4. Extract generated claims.
5. Store hypotheses and claims as JSON-LD graph artifacts.
6. Run ProjectionBench evaluator.
7. Store score, trust, reconciliation, report, and certificate.
8. Export result as JSON-LD.
```

## Prompt Contract

The GPT-5.5 agent must follow the evaluation contract.

```text
You are a theory agent.
Use only evidence disclosed at the current stage.
Generate concise scientific or theory claims.
State assumptions separately.
Do not use undisclosed future evidence.
Return JSON with hypothesis, claims, assumptions, predictions, and confidence.
```

## Output Contract

```json
{
  "hypothesis": "...",
  "claims": [
    {
      "text": "...",
      "confidence": 0.8,
      "evidence_refs": ["pb:stage/example/1"]
    }
  ],
  "assumptions": [],
  "predictions": []
}
```

## Memory Rules

The in-memory graph must preserve:

- scenario
- disclosure stage order
- generated hypothesis per stage
- claim provenance
- evidence references
- evaluation metrics
- score calculation
- insights
- trust state
- signature state

## Safety and Benchmark Integrity Rules

The GPT-5.5 agent must not:

- use future disclosure stages early
- overwrite previous stage outputs
- hide assumptions
- fabricate evidence references
- mark unsigned results as verified
- claim benchmark validity from a fixture run

## Result Status

A SurrealDB in-memory run should default to:

```json
{
  "result_type": "generated_ephemeral_run",
  "signature": {
    "status": "unsigned",
    "verification": "not_verified"
  }
}
```

Only signed and reproducible CI artifacts may be promoted to verified benchmark results.

## Why SurrealDB Fits

SurrealDB is useful here because ProjectionBench treats every evaluation object as a graph artifact:

```text
Scenario -> Stage -> Hypothesis -> Claim -> Score -> Trust -> Report -> Certificate
```

An in-memory SurrealDB agent gives the benchmark a temporary graph-native working memory without forcing persistent deployment.

## Future Implementation

Recommended files:

```text
projectionbench/memory/surreal.py
projectionbench/agents/gpt55.py
projectionbench/agents/base.py
examples/surrealdb-in-memory-agent.py
```

The first implementation should remain optional and dependency-light so the core benchmark can still run without SurrealDB or model access.
