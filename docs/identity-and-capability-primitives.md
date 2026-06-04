# Identity and Capability Primitives

ProjectionBench requires identity and capability as first-class primitives.

The core primitive set is:

```text
Artifact
Time
State
Context
Relation
Identity
Capability
```

## Identity

Identity answers:

```text
Who or what created, generated, evaluated, approved, verified, or certified this artifact?
```

Identity applies to humans, organizations, agents, models, teams, systems, tools, and roles.

## Identity Types

| Identity | schema.org Type | ProjectionBench Extension |
|---|---|---|
| Person | schema:Person | pb:PersonIdentity |
| Organization | schema:Organization | pb:OrganizationIdentity |
| Team | schema:Organization | pb:TeamIdentity |
| Role | schema:Role | pb:RoleIdentity |
| Agent | schema:SoftwareApplication | pb:AgentIdentity |
| Evaluator Agent | schema:SoftwareApplication | pb:EvaluatorAgent |
| Theory Agent | schema:SoftwareApplication | pb:TheoryAgent |
| Model | schema:SoftwareApplication | pb:ModelIdentity |
| Tool | schema:SoftwareApplication | pb:ToolIdentity |
| System | schema:SoftwareApplication | pb:SystemIdentity |

## Identity Relations

```text
Artifact
├── createdBy
├── generatedBy
├── ownedBy
├── evaluatedBy
├── reviewedBy
├── approvedBy
├── verifiedBy
├── certifiedBy
└── operatedBy
```

## Model Identity

Model identity must include:

- provider
- model name
- model version
- release date when known
- configuration
- context window when known
- tool access
- evaluation mode
- benchmark profile

## Agent Identity

Agent identity must include:

- agent name
- agent version
- runtime
- tools
- policies
- permissions
- memory mode
- execution mode

## Capability

Capability answers:

```text
What is this identity able to do, and how well can it do it in a given context?
```

Capabilities are measurable, versioned, and evaluable.

Examples:

- generate hypothesis
- revise theory
- extract claims
- compare claims
- detect contradiction
- ground claims in evidence
- create report
- approve artifact
- certify benchmark result

## Capability Artifact

```json
{
  "@id": "pb:capability/generate-hypothesis",
  "@type": ["schema:DefinedTerm", "pb:Capability"],
  "name": "generate_hypothesis",
  "description": "Ability to generate a hypothesis from a theory seed and disclosed evidence.",
  "measuredBy": {
    "@id": "pb:metric/claim-f1"
  }
}
```

## Identity-Capability Graph

```text
Identity
  ├── hasCapability → Capability
  ├── evaluatedBy → EvaluationRun
  ├── achievesScore → Score
  └── certifiedFor → Profile
```

## Why This Matters

A score is not meaningful without identity.

A benchmark is not useful unless it can say:

```text
This model / agent / system
has this capability
under this context
at this time
with this score
using this metric version.
```

Identity and capability make ProjectionBench useful for model comparison, agent evaluation, theory evaluation, certification, and enterprise governance.
