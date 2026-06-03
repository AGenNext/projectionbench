# JSON-LD Artifact Graph

ProjectionBench uses JSON-LD as the canonical representation for all artifacts.

The graph uses schema.org wherever possible and introduces a small `pb:` namespace only for benchmark-specific concepts that schema.org does not define precisely.

## Principle

Every artifact is a graph node.

Every artifact must have:

- stable `@id`
- `@type`
- name
- description
- provenance
- version
- license where applicable
- creator or publisher
- dateCreated or dateModified
- relationship to other artifacts

## Namespaces

```json
{
  "@context": {
    "schema": "https://schema.org/",
    "pb": "https://github.com/AGenNext/projectionbench/ns#"
  }
}
```

## Canonical Artifact Types

| ProjectionBench Artifact | schema.org Type | Extension Type |
|---|---|---|
| Theory | schema:CreativeWork | pb:Theory |
| Claim | schema:Claim | pb:Claim |
| Evidence | schema:CreativeWork / schema:Dataset / schema:ScholarlyArticle | pb:Evidence |
| Assumption | schema:CreativeWork | pb:Assumption |
| Prediction | schema:CreativeWork | pb:Prediction |
| Counter Claim | schema:Claim | pb:CounterClaim |
| Outcome | schema:Thing | pb:Outcome |
| Revision | schema:CreativeWork | pb:Revision |
| Score | schema:Rating | pb:Score |
| Benchmark Scenario | schema:Dataset | pb:BenchmarkScenario |
| Disclosure Stage | schema:CreativeWork | pb:DisclosureStage |
| Evaluation Run | schema:Action | pb:EvaluationRun |
| Evaluation Report | schema:Report | pb:EvaluationReport |
| Insight | schema:CreativeWork | pb:Insight |
| Profile | schema:DefinedTermSet | pb:BenchmarkProfile |
| Metric | schema:PropertyValue | pb:Metric |
| Rubric | schema:CreativeWork | pb:Rubric |

## Core Graph

```text
Theory
 ├─ hasPart → Claim
 ├─ citation → Evidence
 ├─ isBasedOn → Evidence
 ├─ mentions → Assumption
 ├─ predicts → Prediction
 ├─ reviewedBy → EvaluationRun
 ├─ subjectOf → EvaluationReport
 └─ aggregateRating → Score
```

## JSON-LD Example

```json
{
  "@context": {
    "schema": "https://schema.org/",
    "pb": "https://github.com/AGenNext/projectionbench/ns#",
    "hasClaim": "pb:hasClaim",
    "hasAssumption": "pb:hasAssumption",
    "hasPrediction": "pb:hasPrediction",
    "hasScore": "pb:hasScore"
  },
  "@id": "pb:theory/example-biomaterial-hypothesis",
  "@type": ["schema:CreativeWork", "pb:Theory"],
  "name": "Example Biomaterial Hypothesis",
  "description": "A theory generated under progressive disclosure for a biomaterial research question.",
  "creator": {
    "@type": "schema:Organization",
    "name": "AGenNext"
  },
  "license": "https://www.apache.org/licenses/LICENSE-2.0",
  "version": "0.1.0",
  "hasClaim": [
    {
      "@id": "pb:claim/example-claim-1",
      "@type": ["schema:Claim", "pb:Claim"],
      "claimReviewed": "The material improves mechanical resilience through hierarchical structure.",
      "appearance": "stage-1"
    }
  ],
  "hasAssumption": [
    {
      "@id": "pb:assumption/example-assumption-1",
      "@type": ["schema:CreativeWork", "pb:Assumption"],
      "text": "Hierarchical microstructure is present in the material."
    }
  ],
  "hasPrediction": [
    {
      "@id": "pb:prediction/example-prediction-1",
      "@type": ["schema:CreativeWork", "pb:Prediction"],
      "text": "Mechanical performance should improve under cyclic loading."
    }
  ],
  "hasScore": {
    "@id": "pb:score/example-score-1",
    "@type": ["schema:Rating", "pb:Score"],
    "ratingValue": 0.82,
    "bestRating": 1,
    "worstRating": 0
  }
}
```

## Artifact Graph Rules

1. Use schema.org type first.
2. Add `pb:` type only when benchmark semantics need precision.
3. Never store orphan artifacts.
4. Every claim must link to a theory.
5. Every score must link to an evaluation run.
6. Every evaluation run must link to scenario, profile, evaluator, input, output, and report.
7. Every report must be reproducible from source artifacts.
8. Every generated artifact must preserve provenance.

## Practical Use

This allows ProjectionBench to export every theory, hypothesis, claim, evaluation, and score as a portable knowledge graph.

The same graph can support:

- benchmark datasets
- audit reports
- leaderboards
- scientific reasoning evaluation
- enterprise theory evaluation
- agent evaluation
- governance evidence
- reproducible research
