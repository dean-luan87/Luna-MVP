# Synthetic regression contract

The synthetic command runs the six candidate-only phases and never invokes a Provider, model, YOLO, OCR, camera, Action, Learning, Memory mutation, or Experience mutation.

Every selected phase must return zero, `all_cases_passed=true`, `all_checks_passed=true`, and empty failure arrays. The harness does not reconstruct scenario logic.
