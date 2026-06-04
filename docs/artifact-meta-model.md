# ProjectionBench Artifact Meta-Model

ProjectionBench treats every benchmark object as a governed graph artifact.

## Core Principle

```text
Everything is an Artifact.
Every Artifact is a JSON-LD node.
Every Artifact maps to schema.org first.
Every benchmark-specific semantic gap uses the pb: namespace.
```

## Artifact Classes

```text
Artifact
├── Knowledge Artifact
│   ├── Theory
│   ├── Hypothesis
│   ├── Claim
│   ├── Evidence
│   ├── Assumption
│   ├── Prediction
│   └── Outcome
│
├── Evaluation Artifact
│   ├── Scenario
│   ├── DisclosureStage
│   ├── Profile
│   ├── Metric
│   ├── EvaluationRun
│   ├── Score
│   └── Report
│
├── Governance Artifact
│   ├── ArtifactCard
│   ├── Policy
│   ├── Approval
│   ├── Verification
│   ├── Certification
│   └── TrustScore
│
└── Registry Artifact
    ├── DatasetRegistry
    ├── ScenarioRegistry
    ├── ProfileRegistry
    ├── MetricRegistry
    ├── RunRegistry
    └── LeaderboardRegistry
```

## Artifact Lifecycle

```text
Draft
  -> Review
  -> Approved
  -> Published
  -> Evaluated
  -> Verified
  -> Certified
  -> Deprecated
  -> Archived
```

## Canonical Relations

```text
Artifact
├── CREATED_BY
├── OWNED_BY
├── VERSION_OF
├── DEPENDS_ON
├── REFERENCES
├── IS_BASED_ON
├── EVALUATED_BY
├── SCORED_BY
├── VERIFIED_BY
├── APPROVED_BY
├── CERTIFIED_BY
└── REPLACED_BY
```

## Trust Requirement

A benchmark result is trustworthy only when it has:

- source artifact
- scenario artifact
- profile artifact
- metric artifact
- evaluator artifact
- evaluation run artifact
- score artifact
- report artifact
- artifact card
- version and provenance

## ProjectionBench Profile

ProjectionBench is the first profile on top of the generic theory evaluation model.

It evaluates scientific hypothesis generation under progressive information disclosure, grounded in arXiv:2605.30284.

## Generic Theory Extension

The same artifact model supports evaluating:

- scientific theories
- business theses
- governance frameworks
- product strategies
- architecture principles
- economic models
- policy arguments
- education frameworks
- agent behavior theories

## Target State

ProjectionBench should evolve into an artifact-native theory evaluation platform where every scenario, metric, score, report, and leaderboard entry is reproducible, governed, and graph-native.
