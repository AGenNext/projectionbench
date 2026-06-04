# ProjectionBench Core Primitives

ProjectionBench is built on five primitives.

```text
Artifact
Time
State
Context
Relation
```

Everything else is derived from these primitives.

## 1. Artifact

An artifact is any object that can be authored, versioned, evaluated, governed, trusted, or reused.

Examples:

- theory
- claim
- evidence
- scenario
- metric
- score
- report
- profile
- evaluation run
- leaderboard entry

## 2. Time

Every artifact is temporal.

Time fields include:

- `validFrom`
- `validUntil`
- `observedAt`
- `evaluatedAt`
- `publishedAt`
- `archivedAt`

Time prevents overwriting truth. New evidence creates new versions, revisions, and evaluations.

## 3. State

Every artifact has lifecycle state.

Canonical states:

```text
Draft
Review
Approved
Published
Evaluated
Verified
Certified
Deprecated
Archived
Rejected
```

State makes governance executable.

## 4. Context

Evaluation is meaningless without context.

Context includes:

- domain
- industry
- geography
- jurisdiction
- audience
- environment
- constraints
- assumptions
- disclosure level
- evaluation profile

The same theory can score differently in different contexts.

## 5. Relation

Artifacts become meaningful through relations.

Canonical relations:

```text
CREATED_BY
OWNED_BY
VERSION_OF
DEPENDS_ON
REFERENCES
IS_BASED_ON
CONTRADICTS
SUPPORTS
PREDICTS
EVALUATED_BY
SCORED_BY
VERIFIED_BY
APPROVED_BY
CERTIFIED_BY
REPLACED_BY
```

## Meta Graph

```text
Artifact
  -> hasState
  -> hasTime
  -> hasContext
  -> hasRelation
  -> evaluatedBy
  -> scoredBy
```

## Why This Matters

A score without context is not trustworthy.
A claim without evidence is not grounded.
An evaluation without time is not reproducible.
A benchmark without state is not governable.
A theory without relations is not a graph.

ProjectionBench therefore treats every evaluation as a temporal, contextual, governed graph.
