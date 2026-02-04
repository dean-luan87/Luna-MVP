from .schema import ExplainOutput
from .invariants import assert_explain_invariants


def assemble(tags, episodes, confidence):
    output = ExplainOutput(
        explanation_tags=tags,
        episodes=episodes,
        confidence=confidence,
    )
    assert_explain_invariants(output)
    return output
