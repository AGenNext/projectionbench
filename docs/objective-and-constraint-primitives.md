# Objective and Constraint Primitives

ProjectionBench evaluates capability in context. Capability is not meaningful unless the objective and constraints are explicit.

The core primitive set is:

```text
Artifact
Time
State
Context
Relation
Identity
Capability
Objective
Constraint
```

## Objective

Objective answers:

```text
Why is this artifact, theory, agent, model, or system being evaluated?
What outcome is desired?
What does success mean?
What does failure mean?
```

Examples:

- generate scientific hypotheses that converge toward reference conclusions
- evaluate whether a business thesis can explain market behavior
- assess whether a governance framework reduces risk without blocking execution
- compare whether an architecture theory improves reliability and maintainability
- determine whether an agent can revise claims as evidence is progressively disclosed

## Objective Artifact

```json
{
  "@id": "pb:objective/generate-progressive-hypothesis",
  "@type": ["schema:DefinedTerm", "pb:Objective"],
  "name": "generate_progressive_hypothesis",
  "description": "Generate and revise hypotheses as evidence is progressively disclosed.",
  "successCriterion": "Final claims converge toward reference claims while remaining grounded in disclosed evidence."
}
```

## Objective Relations

```text
EvaluationRun
├── hasObjective → Objective
├── measuresCapability → Capability
├── constrainedBy → Constraint
└── produces → Score
```

## Constraint

Constraint answers:

```text
What boundaries must the evaluated identity respect while pursuing the objective?
```

Constraints prevent optimization from becoming unsafe, misleading, non-compliant, or meaningless.

## Constraint Types

| Constraint | Meaning |
|---|---|
| Time Constraint | Deadline, sequence, freshness, disclosure order |
| Evidence Constraint | Only use disclosed evidence, cite sources, preserve provenance |
| Policy Constraint | Follow benchmark policy, governance, or enterprise rule |
| Risk Constraint | Avoid unsafe, unsupported, or overconfident claims |
| Domain Constraint | Stay within the evaluated domain |
| Method Constraint | Use allowed tools, prompts, models, or scoring methods |
| Context Constraint | Respect geography, audience, industry, environment |
| License Constraint | Respect artifact license and source usage limits |
| Privacy Constraint | Avoid exposing restricted or sensitive information |

## Constraint Artifact

```json
{
  "@id": "pb:constraint/disclosed-evidence-only",
  "@type": ["schema:DefinedTerm", "pb:Constraint"],
  "name": "disclosed_evidence_only",
  "description": "The evaluated system must only use evidence disclosed at or before the current stage.",
  "constraintType": "Evidence Constraint"
}
```

## Evaluation Formula

A trustworthy evaluation must include:

```text
Identity
+ Capability
+ Objective
+ Constraint
+ Context
+ Time
+ Evidence
+ Metric
= Score + Insight + Trust
```

## ProjectionBench Profile

For the ProjectionBench profile grounded in arXiv:2605.30284:

```text
Objective:
Generate scientific hypotheses that improve as information is progressively disclosed.

Constraint:
Use only the information available at the current disclosure stage.

Capability:
Progressive scientific hypothesis generation and revision.

Score:
Claim alignment, stage improvement, groundedness, novelty, and consistency.
```

## Generic Theory Profile

For generic theory evaluation:

```text
Objective:
Evaluate whether a theory explains, predicts, or guides action in a defined context.

Constraint:
Respect domain, evidence, assumptions, and policy boundaries.

Capability:
Theory generation, revision, contradiction detection, and practical insight.
```

## Why This Matters

A score without an objective is ambiguous.
A high-performing model without constraints may be unsafe.
A theory without boundaries cannot be fairly evaluated.

ProjectionBench therefore evaluates not just outputs, but purpose-bound, constraint-aware capability.
