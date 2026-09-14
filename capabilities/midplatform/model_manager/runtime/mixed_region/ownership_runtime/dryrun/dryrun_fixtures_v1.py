# -*- coding: utf-8 -*-
"""Ownership Runtime DryRun — deterministic scene fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.planning_fixtures_v1 import (
    PLANNING_FIXTURES,
    blocked_entity_ids,
    get_fixture,
)

DRYRUN_FIXTURE_KEYS = tuple(PLANNING_FIXTURES.keys())

__all__ = ["DRYRUN_FIXTURE_KEYS", "get_fixture", "blocked_entity_ids", "PLANNING_FIXTURES"]
