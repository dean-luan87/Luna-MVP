# Verification

From `/Users/luanlei/Desktop/Luna-Core`:

```bash
python -m capabilities.evaluation.level1_cognitive_evaluation_run.run_minimum_sufficient_cognition_loop_controlled_replay_v1
python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_minimum_sufficient_cognition_loop_controlled_replay_v1 _eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1/runner_summary_v1.json
```

The Verifier fails closed on missing canonical loop refs, broken cycle linkage, unavailable zero-fill, invalid governance, or archive/White-box defects.
