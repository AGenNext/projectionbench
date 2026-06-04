from projectionbench.evaluator import Evaluator, harmonic_mean
from projectionbench.models import Claim, Hypothesis


def test_harmonic_mean_zero_safe():
    assert harmonic_mean(0, 0) == 0.0


def test_claim_f1_positive_for_matching_claims():
    evaluator = Evaluator()
    generated = [
        Hypothesis(
            id="pb:hypothesis/test/1",
            stage="1",
            text="Hierarchical structure improves toughness.",
            claims=[
                Claim(
                    id="pb:claim/test/1",
                    text="Hierarchical structure improves toughness in the polymer composite.",
                )
            ],
        )
    ]
    reference = [
        Claim(
            id="pb:reference/test/1",
            text="Hierarchical structure improves toughness in the polymer composite.",
        )
    ]
    score = evaluator.score(generated, reference, "Hierarchical structure improves toughness in the polymer composite.")
    metrics = {metric.name: metric.value for metric in score.metrics}
    assert metrics["claim_f1"] > 0.9
    assert metrics["groundedness"] > 0.0
    assert score.overall > 0.0


def test_consistency_detects_simple_contradiction():
    evaluator = Evaluator()
    claims = [
        Claim(id="pb:claim/a", text="The composite improves crack resistance."),
        Claim(id="pb:claim/b", text="The composite reduces crack resistance."),
    ]
    assert evaluator.consistency(claims) < 1.0
