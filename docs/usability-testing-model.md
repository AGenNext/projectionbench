# Usability Testing Model

Source reference: https://www.geeksforgeeks.org/software-testing/usability-testing/

## Definition

Usability Testing is a structured evaluation method used to determine whether intended users can understand, navigate, operate, complete tasks, recover from errors, and feel satisfied while using a product, system, workflow, agent, interface, report, or artifact.

In ProjectionBench, usability testing is modeled as a benchmark profile.

```text
Usability Testing
= Profile
= evaluates User Experience Capability
= under User + Task + Context + Constraint
= using Observation + Feedback + Outcome
= producing Score + Insight + Recommendation
```

## Canonical Model

```text
User
  + Task
  + Context
  + Constraint
  + Observation
  + Feedback
  + Outcome
  -> Usability Metrics
  -> Usability Score
  -> Insight
  -> Recommendation
```

## Evaluation Contract Mapping

| ProjectionBench Field | Usability Testing Meaning |
|---|---|
| Subject | Product, UI, workflow, agent, report, dashboard, artifact |
| Capability | Usability |
| Objective | Enable target users to complete intended tasks successfully |
| Constraint | Accessibility, cognitive load, time, error tolerance, policy, security |
| Context | User type, device, environment, expertise, accessibility need |
| Evidence | Observations, logs, surveys, recordings, feedback, analytics |
| Prediction | Intended user behavior or task path |
| Outcome | Actual user behavior, task completion, errors, satisfaction |
| Reconciliation | Gap between intended and observed experience |
| Score | Usability score |
| Insight | What worked, failed, confused users, or needs improvement |

## Model Fields

### Subject

What is being tested?

Examples:

- product
- interface
- workflow
- agent
- dashboard
- report
- artifact

### User

Who is using it?

Examples:

- evaluator
- researcher
- IT admin
- product manager
- auditor
- developer
- business user

### Task

What must the user complete?

Examples:

- understand score
- find evidence
- check signature
- compare models
- export report
- approve certificate

### Context

Where and under what conditions?

Examples:

- device
- environment
- domain
- time pressure
- user expertise
- accessibility need
- workflow stage

### Constraint

What must the system respect?

Examples:

- accessibility
- cognitive load
- error tolerance
- time limit
- policy
- security
- auditability

### Observation

What actually happened?

Examples:

- clicks
- time taken
- errors
- hesitation
- abandonment
- searches
- backtracking
- misinterpretation

### Feedback

What did the user say?

Examples:

- confusing
- clear
- too slow
- hard to find
- trustworthy
- not enough evidence

### Outcome

Did the user succeed?

Examples:

- completed
- partially completed
- failed
- completed with help
- completed with errors

## Metrics

```text
UsabilityScore
├── TaskCompletion
├── Effectiveness
├── Efficiency
├── Learnability
├── ErrorTolerance
├── Satisfaction
├── Accessibility
├── Discoverability
├── Consistency
└── CognitiveLoad
```

## Scoring Model

```text
UsabilityScore =
0.20 × TaskCompletion
+ 0.15 × Effectiveness
+ 0.15 × Efficiency
+ 0.10 × Learnability
+ 0.10 × ErrorTolerance
+ 0.10 × Satisfaction
+ 0.10 × Accessibility
+ 0.05 × Discoverability
+ 0.03 × Consistency
+ 0.02 × CognitiveLoad
```

## Example Use Case

Subject:

```text
ProjectionBench result page
```

Objective:

```text
Allow an evaluator to understand benchmark score, trust, insights, gaps, recommendations, and signature status within 60 seconds.
```

Insight examples:

- Users can find the score but cannot understand verification status.
- Users trust the number but miss the fixture warning.
- Users need a visible score breakdown and signature badge.

Recommendation examples:

- Add verification badge.
- Separate fixture from generated result.
- Show calculation beside score.
- Expose source, signature, and trust status above the fold.

## JSON-LD Mapping

| Artifact | schema.org Type | ProjectionBench Extension |
|---|---|---|
| Usability Test | schema:ReviewAction | pb:UsabilityEvaluation |
| Test Scenario | schema:CreativeWork | pb:UsabilityScenario |
| User Task | schema:Action | pb:UserTask |
| User Feedback | schema:Review | pb:UserFeedback |
| Observation | schema:Observation | pb:UsabilityObservation |
| Score | schema:Rating | pb:UsabilityScore |
| Recommendation | schema:Recommendation | pb:Recommendation |
| Report | schema:Report | pb:EvaluationReport |

## Rule

A usability score is not valid unless it is linked to:

- subject
- target user
- task
- context
- constraints
- observations
- feedback or outcome
- metric calculation
- insight
- recommendation

## Final Definition

Usability Testing in ProjectionBench evaluates whether a subject can support intended users in completing intended tasks effectively, efficiently, accessibly, and satisfactorily under defined context and constraints.
