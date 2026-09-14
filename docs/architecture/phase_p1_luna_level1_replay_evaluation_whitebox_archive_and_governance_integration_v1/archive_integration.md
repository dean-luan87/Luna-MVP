# Archive Integration

The Runner uses the existing `write_evaluation_run_record_v1` writer and canonical `evaluation_archive/level1_cognitive_runs/` root. Archive identity is immutable: a different payload under an existing run identity raises an archive conflict.

The `_eval_out` file is only a terminal Runner summary, never canonical history.
