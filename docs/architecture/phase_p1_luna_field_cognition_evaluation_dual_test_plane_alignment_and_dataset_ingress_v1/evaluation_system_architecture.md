# Luna Field Cognition Evaluation System

## Final structure

**Plane A — Luna Cognitive Evaluation** is primary. It evaluates the A-Route
Field Cognition Brain: what Luna needs to know, how it observes, uses
Evidence, revises Hypotheses, assesses Sufficiency, re-observes, stops, and
hands off to Decision Governance.

**Plane B — External Capability Fitness Evaluation** evaluates object
detection, OCR, RF-DETR, YOLO, SLAM, VLM, and other implementations only as
external means of producing Evidence.

**Shared infrastructure** consists of Evaluation World / Observation Corpus,
Dataset Registry, Cognitive Test Cases, Cognitive White-box Trace, Luna
Cognitive Execution Profile, failure/gap refs, TestBoard evidence, and
cross-plane comparison refs.

## Independence rule

Plane B PASS does not imply Plane A PASS. Plane B failure does not imply Plane
A failure if Luna correctly recognizes uncertainty, forms a gap, re-observes,
and reaches the appropriate cognition state.

Evaluation observes and records; it does not mutate Goal, Attention, Evidence,
Current World, Field, Decision, Task, Action, Model binding, or runtime policy.
