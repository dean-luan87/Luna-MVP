# Cognitive Runtime Instance Lifecycle v1

## Definition

A Cognitive Runtime Instance Candidate represents one temporary, traceable execution context for an admitted Cognitive Process Candidate. It is not persistent State, a State Machine, a task plan, or a process executor.

## Example

```text
runtime_instance_id: airport_navigation_session_001_candidate
goal_reference: reach_gate_candidate
context_reference: airport_context_candidate
attention_allocation: gate_sign_attention_candidate
capability_bundle: visual_text_spatial_candidate
resource_budget: conservation_budget_candidate
workspace_reference: current_route_workspace_candidate
trace_reference: execution_trace_candidate
lifecycle: active_candidate
```

## Lifecycle

```text
Creation Candidate -> Admitted Candidate -> Active Candidate
  -> Adjusted / Suspended Candidate -> Closed / Retained Candidate
```

Lifecycle metadata is local to the temporary candidate context. It cannot mutate Reducer-owned State or assert that execution actually occurred.

## Boundary

Runtime Instance is not State. Runtime Instance is not Action. Runtime Instance is not a decision, capability invocation, model invocation, or memory record.

