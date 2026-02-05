from luna_badge_v1_2.governance.explain_layer.schema import ExplainOutput, SCHEMA_VERSION


def test_schema_version_fixed():
    output = ExplainOutput(explanation_tags=[], episodes=[], confidence="LOW")
    assert output.schema_version == SCHEMA_VERSION
