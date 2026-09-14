import pytest

from luna_badge_v1_2.governance.explain_layer.assembler import assemble
from luna_badge_v1_2.governance.explain_layer.invariants import assert_explain_invariants


def test_assemble_explain_output_fields():
    output = assemble(tags=["RISK_ACCELERATION_PERSISTENT"], episodes=["SAFE"], confidence="HIGH")
    assert output.schema_version == "explain.v1"
    assert isinstance(output.explanation_tags, list)
    assert isinstance(output.episodes, list)
    assert output.confidence in {"LOW", "MEDIUM", "HIGH"}


def test_explain_invariants_reject_forbidden():
    class _Dummy:
        explanation_tags = ["STOP_IMMEDIATE"]

    with pytest.raises(AssertionError):
        assert_explain_invariants(_Dummy())
