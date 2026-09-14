# Cognitive Analysis Controlled DryRun Execution Plan v1

## 1. Definition and frozen scope

The future A3 Controlled DryRun is a fixture-only, deterministic validation of
the Cognitive Analysis object chain, reference closure, lifecycle, permission
boundary, failure semantics, and negative guards. It is a validation
orchestrator, not a cognitive-analysis engine.

It must freeze the following result flags:

```text
fixture_assembled=true
real_analysis_executed=false
runtime_executed=false
simulation_only=true
model_invoked=false
network_invoked=false
database_invoked=false
observation_executed=false
decision_executed=false
state_writeback=false
```

The DryRun does not prove analysis truth, hypothesis correctness, meaningful
confidence, model capability, Context runtime integration, executable
Decision, or production readiness.

## 2. Actual asset mapping

| Planned concern | Actual asset / structure | DryRun planning rule |
| --- | --- | --- |
| Object types | `core/cognitive_analysis_types_v1.py` | Validate the nine frozen dataclasses; do not add a tenth runtime object. |
| Controlled values | `core/cognitive_analysis_enums_v1.py` | Use the actual enum members, not free-text substitutes. |
| Authority flags | `core/cognitive_analysis_invariants_v1.py` | Preserve Context-only input and Reducer-only State mutation constants. |
| Fixture container | `fixtures/cognitive_analysis_fixture_v1.py:CognitiveAnalysisFixtureV1` | Treat it as the future case bundle. |
| Fixture source | `build_cognitive_analysis_fixtures_v1()` | Load its eight fixed cases without mutation. |
| Static result | `validators/...:StaticValidationResultV1` | Consume `subject_ref`, `issues`, and derived `valid`; verifier must independently recheck fields. |
| A2 Context mapping | A3 uses string `source_context_ref`, version, provenance and `trace_ref` | No A2 Context runtime or parallel Context type is permitted. |

The required external Case IDs map to current fixture IDs as follows:

| Planned Case ID | Actual fixture `case_id` |
| --- | --- |
| `A3_DR_CASE_001_SUPPORTED_SINGLE_HYPOTHESIS` | `case_01_supported` |
| `A3_DR_CASE_002_UNRESOLVED_COMPETING_HYPOTHESES` | `case_02_competing` |
| `A3_DR_CASE_003_CONTRADICTED_HYPOTHESIS` | `case_03_contradicted` |
| `A3_DR_CASE_004_CONTEXT_INSUFFICIENT_BLOCKED` | `case_04_insufficient` |
| `A3_DR_CASE_005_REVOKED_EVIDENCE_STALE` | `case_05_revoked` |
| `A3_DR_CASE_006_TEMPORAL_UNKNOWN_CONDITIONAL` | `case_06_temporal_unknown` |
| `A3_DR_CASE_007_GAP_REFINEMENT_OBSERVATION_REQUEST` | `case_07_gap_request` |
| `A3_DR_CASE_008_STATE_WRITEBACK_DENIED` | `case_08_writeback_denied` |

## 3. Five future validation levels

1. **Object validation** — required fields, enum instances, provenance,
   `trace_ref`, and fixed flags.
2. **Reference validation** — Admission→Frame, Frame/Context→Hypothesis,
   Assessment→Hypothesis, Set→Hypotheses, Gap→Frame/source gap,
   Request→Refinement, Sufficiency→Frame/Context, and Result→all existing
   objects.
3. **Semantic consistency** — blocked/insufficient, revoked, temporal
   unknown, unresolved competing hypotheses, stale lifecycle, and denied
   writeback semantics.
4. **Permission/runtime boundary** — candidate-only Observation Request,
   no Decision admission, no State writeback, `runtime_executed=false`,
   `simulation_only=true`, and Reducer-only mutation authority.
5. **Negative guard** — no Fact promotion, unknown completion, forced
   dominant candidate, execution, Context/Snapshot/State mutation, or external
   capability access.

## 4. Future Runner and Verifier responsibilities

The future Runner may load fixed fixtures, invoke pure validators, perform the
five checks, collect deterministic results, and write declared output files.
It must not modify a fixture, fill missing fields, use time/random IDs, call
models/runtimes, or mark a caught failure as PASS.

The future Verifier must independently read Runner output and recheck case
count/uniqueness, expected statuses, reference closure, checks, warnings,
runtime flags, State writeback, file presence, and Contract reference. It must
not trust only the Runner's final boolean.

## 5. Planned pass, fail, and blocker criteria

PASS requires eight observed/passed cases, zero failures/blockers/dangling or
cross-case references, all frozen flags, and all negative guards. Expected
warnings may remain; unexpected warnings must be reported rather than ignored.

A missing fixture, dangling/cross-case reference, blocked Context with an
effective complete conclusion, revoked Evidence as support, unknown time as
valid, forced dominant candidate, enabled execution/writeback, external call,
fixture mutation, or verifier self-trust is a blocker.
