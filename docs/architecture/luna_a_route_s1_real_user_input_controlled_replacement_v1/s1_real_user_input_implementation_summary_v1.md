# S1 Implementation Summary

The new adapter is a narrow integration asset under the existing A Route
Orchestration Governance owner. It accepts a user-supplied text argument,
performs structural normalization, preserves sensitivity/correction/trace
metadata, and constructs the already canonical `ProductLoopInputV1`.

The S1 Runner always retains the S0 fixture path. Its default mode runs the
20 S1 controlled cases plus all 40 S0 cases; `--input` additionally exercises
the real user-input surface while keeping all downstream stages synthetic and
controlled. The adapter uses caller-supplied immutable seen IDs for duplicate
detection and has no hidden mutable state.
