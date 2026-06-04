# JSON-LD Node Model

ProjectionBench represents every benchmark object as a JSON-LD graph node.

## Source Grounding

This model is grounded in:

- JSON-LD: https://www.w3.org/TR/json-ld11/
- JSON-LD API: https://www.w3.org/TR/json-ld11-api/
- schema.org: https://schema.org/
- schema.org Claim: https://schema.org/Claim
- schema.org Dataset: https://schema.org/Dataset
- schema.org ScholarlyArticle: https://schema.org/ScholarlyArticle
- schema.org Rating: https://schema.org/Rating
- schema.org Action: https://schema.org/Action
- schema.org Report: https://schema.org/Report

## Definition

A ProjectionBench node is a uniquely identified JSON-LD graph artifact that represents a source, scenario, agent, theory, hypothesis, claim, metric, score, trust record, insight, recommendation, certificate, registry entry, or other evaluation object.

A node must be:

```text
Identified by @id
Typed by @type
Interpreted through @context
Connected through named properties
```

## Minimum Node Contract

```json
{
  "@context": {
    "schema": "https://schema.org/",
    "pb": "https://github.com/AGenNext/projectionbench/ns#"
  },
  "@id": "pb:claim/example-biomaterial/1",
  "@type": ["schema:Claim", "pb:Claim"],
  "name": "Example claim",
  "description": "A claim generated or referenced during evaluation."
}
```

## Required Fields

| Field | Requirement | Meaning |
|---|---|---|
| `@context` | Required at document or node graph level | Defines vocabulary mapping. |
| `@id` | Required | Stable node identity. |
| `@type` | Required | Semantic type using schema.org first and pb extension where needed. |
| `name` | Recommended | Human-readable label. |
| `description` | Recommended | Human-readable meaning. |
| `version` | Recommended | Artifact version. |
| `provenance` | Recommended | Source or generation trace. |

## Node Classes

```text
Node
├── Source Node
├── Scenario Node
├── Disclosure Node
├── Agent Node
├── Theory Node
├── Hypothesis Node
├── Claim Node
├── Evidence Node
├── Metric Node
├── Score Node
├── Trust Node
├── Insight Node
├── Gap Node
├── Recommendation Node
├── Report Node
├── Certificate Node
├── Signature Node
└── Registry Node
```

## schema.org Mapping

| ProjectionBench Node | schema.org Type | pb Extension |
|---|---|---|
| Source Paper | `schema:ScholarlyArticle` | `pb:SourcePaper` |
| Scenario | `schema:Dataset` | `pb:BenchmarkScenario` |
| Disclosure Stage | `schema:CreativeWork` | `pb:DisclosureStage` |
| Agent | `schema:SoftwareApplication` | `pb:TheoryAgent` |
| Hypothesis | `schema:CreativeWork` | `pb:Hypothesis` |
| Claim | `schema:Claim` | `pb:Claim` |
| Metric | `schema:PropertyValue` | `pb:Metric` |
| Score | `schema:Rating` | `pb:Score` |
| Evaluation Run | `schema:Action` | `pb:EvaluationRun` |
| Report | `schema:Report` | `pb:EvaluationReport` |
| Certificate | `schema:CreativeWork` | `pb:CapabilityCertificate` |
| Recommendation | `schema:Recommendation` | `pb:Recommendation` |

## Example Source Node

```json
{
  "@id": "pb:source/arxiv-2605-30284",
  "@type": ["schema:ScholarlyArticle", "pb:SourcePaper"],
  "name": "ProjectionBench: Evaluating Scientific Hypothesis Generation in LLMs Under Progressive Information Disclosure",
  "identifier": "arXiv:2605.30284",
  "url": "https://arxiv.org/abs/2605.30284"
}
```

## Example Scenario Node

```json
{
  "@id": "pb:scenario/example-biomaterial",
  "@type": ["schema:Dataset", "pb:BenchmarkScenario"],
  "name": "Example Biomaterial Progressive Disclosure Scenario",
  "domain": "scientific-hypothesis-generation",
  "isBasedOn": {
    "@id": "pb:source/arxiv-2605-30284"
  }
}
```

## Example Claim Node

```json
{
  "@id": "pb:claim/example-biomaterial/1",
  "@type": ["schema:Claim", "pb:Claim"],
  "claimReviewed": "Hierarchical structure improves toughness in the polymer composite.",
  "isBasedOn": {
    "@id": "pb:stage/example-biomaterial/4"
  }
}
```

## Example Score Node

```json
{
  "@id": "pb:score/example-biomaterial",
  "@type": ["schema:Rating", "pb:Score"],
  "ratingValue": 0.950714,
  "bestRating": 1,
  "worstRating": 0,
  "ratingExplanation": "A+"
}
```

## Node Relations

Nodes become meaningful through typed edges.

```text
Scenario       -> isBasedOn       -> SourcePaper
Scenario       -> hasPart         -> DisclosureStage
Agent          -> generated       -> Hypothesis
Hypothesis     -> hasClaim        -> Claim
Claim          -> isBasedOn       -> Evidence
EvaluationRun  -> object          -> Scenario
EvaluationRun  -> agent           -> Agent
EvaluationRun  -> result          -> Score
EvaluationRun  -> result          -> Report
EvaluationRun  -> hasCertificate  -> Certificate
```

## No-Orphan Rule

No node should be orphaned unless it is a root registry node.

Examples:

- A claim must connect to a hypothesis or reference conclusion.
- A score must connect to an evaluation run.
- An insight must connect to a report or reconciliation.
- A certificate must connect to a subject, capability, score, and profile.
- A signature must connect to the artifact it signs.

## SurrealDB Mapping

In SurrealDB, every node can become a record.

```sql
CREATE claim:example_biomaterial_1 SET
  type = ["schema:Claim", "pb:Claim"],
  claimReviewed = "Hierarchical structure improves toughness in the polymer composite.",
  basedOn = stage:example_biomaterial_4;
```

A relation can be represented as an edge table.

```sql
RELATE hypothesis:example_biomaterial_stage_4->has_claim->claim:example_biomaterial_1;
```

## Final Rule

Use schema.org first. Use `pb:` only when ProjectionBench needs benchmark-specific precision.
