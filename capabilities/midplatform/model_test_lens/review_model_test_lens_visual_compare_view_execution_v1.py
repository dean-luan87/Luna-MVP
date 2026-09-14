# -*- coding: utf-8 -*-
"""P1 Model Test Lens Visual Compare View — review v1 (delegates to overlay review)."""

from capabilities.midplatform.model_test_lens.review_model_test_lens_visual_overlay_layer_execution_v1 import (
    run_compare_review,
)

if __name__ == "__main__":
    import json
    print(json.dumps(run_compare_review(), indent=2))
