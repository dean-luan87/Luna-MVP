# Negative Guards

The controlled package asserts false for:

- brain_runtime_execution;
- provider_invocation;
- model_inference;
- yolo;
- ocr;
- camera;
- action_execution;
- learning;
- memory_mutation;
- experience_mutation;
- autonomous_scheduling;
- authority_manager_created;
- permission_manager_created;
- loop_manager_created;
- loop_planner_created;
- loop_semantic_judgment;
- loop_sufficiency_judgment;
- loop_need_selection;
- loop_hypothesis_generation;
- b_recursive_delegation;
- b_concern_creation;
- cross_concern_grant_use;
- cross_loop_state_mutation;
- semantic_compression.

Candidate and synthetic mode are true. These guards do not authorize runtime
execution.
