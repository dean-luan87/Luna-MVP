# -*- coding: utf-8 -*-
"""Doc-local verifier entry for Field State Reducer controlled skeleton implementation v1.

This wrapper delegates to the canonical verifier under tools/evaluation/midplatform.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.evaluation.midplatform.verify_field_state_reducer_controlled_skeleton_implementation_v1 import (  # noqa: E501
    main,
)


if __name__ == "__main__":
    raise SystemExit(main())
