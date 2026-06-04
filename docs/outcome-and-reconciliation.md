# Outcome and Reconciliation

ProjectionBench evaluates theories by comparing generated predictions or claims against observed, reference, or actual outcomes.

## Why Outcome Matters

A prediction cannot be evaluated without an outcome.

A theory cannot be trusted unless its claims can be compared with what later became known, observed, or accepted as reference truth.

## Outcome

Outcome answers:

```text
What happened?
What was observed?
What was the accepted reference result?
What changed after execution, testing, or disclosure?
```

## Outcome Artifact

```json
{
  "@id": "pb:outcome/example",
  "@type": ["schema:Thing", "pb:Outcome"],
  "name": "Reference outcome",
  "expected": "The hypothesis predicts improved fatigue resistance.",
  "actual": "The reference conclusion reports higher fatigue resistance than the non-hierarchical control.",
  "delta": "Prediction aligned with reference outcome.",
  "confidence": 0.9
}
```

## Outcome Fields

```text
Outcome
├── expected
├── actual
├── delta
├── impact
├── confidence
├── evidence
└── observedAt
```

## Reconciliation

Reconciliation answers:

```text
What matched?
What did not match?
What improved?
What degraded?
What should change next?
```

## Reconciliation Artifact

```json
{
  "@id": "pb:reconciliation/example",
  "@type": ["schema:Action", "pb:Reconciliation"],
  "name": "Claim reconciliation",
  "object": { "@id": "pb:prediction/example" },
  "result": { "@id": "pb:outcome/example" },
  "matchedClaims": 3,
  "missedClaims": 1,
  "unsupportedClaims": 0,
  "recommendation": "Improve disclosure-stage claim grounding."
}
```

## ProjectionBench Interpretation

For the ProjectionBench profile grounded in arXiv:2605.30284:

```text
Prediction = generated hypothesis claims
Outcome = reference paper conclusions
Reconciliation = semantic claim comparison
Score = claim alignment + stage improvement + groundedness + consistency
```

## Generic Theory Interpretation

For generic theory evaluation:

```text
Prediction = expected theory implication
Outcome = observed result or accepted reference
Reconciliation = gap analysis between theory and reality
Score = quality of explanation, prediction, adaptation, and practical usefulness
```

## Final Evaluation Loop

```text
Evidence
  -> Theory
  -> Prediction
  -> Outcome
  -> Reconciliation
  -> Score
  -> Insight
  -> Revision
```

## Rule

No benchmark score should be considered final unless it is linked to an outcome and reconciliation artifact.
