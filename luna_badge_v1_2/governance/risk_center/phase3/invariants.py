FORBIDDEN_READS = {"decision", "authority", "c_decision"}


def assert_phase3_invariants(context: dict) -> None:
    for key in FORBIDDEN_READS:
        if key in context:
            raise AssertionError(f"Phase-3 read forbidden field: {key}")
