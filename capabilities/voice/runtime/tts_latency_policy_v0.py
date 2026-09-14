# -*- coding: utf-8 -*-
"""
Latency policy primitives (v0).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LatencyPolicyV0:
    soft_latency_warning_ms: int = 800
    first_response_budget_ms: int = 1200
    hard_timeout_ms: int = 2000

    def classify_total_latency(self, latency_ms: int) -> str:
        ms = int(latency_ms or 0)
        if ms > self.hard_timeout_ms:
            return "hard_timeout_exceeded"
        if ms > self.first_response_budget_ms:
            return "high_latency_risk"
        if ms > self.soft_latency_warning_ms:
            return "soft_latency_warning"
        return "normal"

