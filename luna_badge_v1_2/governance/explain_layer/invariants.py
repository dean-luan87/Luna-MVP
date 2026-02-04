FORBIDDEN_TOKENS = {"STOP", "HOLD", "TAKEOVER"}


def assert_explain_invariants(output):
    for tag in output.explanation_tags:
        for token in FORBIDDEN_TOKENS:
            if token in tag:
                raise AssertionError("Explain layer leaked control semantics")
