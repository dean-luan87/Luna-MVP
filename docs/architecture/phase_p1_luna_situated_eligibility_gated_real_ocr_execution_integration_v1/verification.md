# Verification

User-terminal Runner:

```bash
python3 -m capabilities.evaluation.situated_eligibility_gated_real_ocr_execution_integration.situated_eligibility_gated_real_ocr_execution_runner_v1
```

User-terminal Verifier:

```bash
python3 -m capabilities.evaluation.situated_eligibility_gated_real_ocr_execution_integration.situated_eligibility_gated_real_ocr_execution_verifier_v1
```

The Verifier checks that ineligible and not-required cases have no attempted
Provider call, while eligible cases use `LIVE_RUNTIME`, invoke the real
Provider/Model, produce the existing Runtime Observation/Gateway/Evidence/
CState chain, and do not use recorded results.  It also checks the dynamic
case’s single invocation count and the existing irrelevant-evidence guard.

## First terminal verification and audit

The first user-terminal verification reported `42/43` checks passing. The
only failure was `dynamic_real_provider_invocation_count_one`.

Static audit established that the Engine has one real OCR call site:
`RealOCRProviderExecutionEngineV1.run(...)`, below the Situated Eligibility
admission gate. The Dynamic case has no duplicate t1 call and no summary
projection that invokes OCR again. Its t0 record is blocked and its t1 record
is the sole real invocation for that Dynamic case.

The blocker was a verifier counting-scope defect. The Runner's top-level
`real_provider_invocation_count` and `real_model_invocation_count` aggregate
all records, including the independent eligible case. The verifier had
compared those aggregate fields with the Dynamic case's expected count of one.
The verifier now derives the Dynamic count only from the
`DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE` t0/t1 records, requiring the
attempted/provider/model invocation flags to identify one real invocation.

Classification: `VERIFIER_COUNTING_SCOPE_GAP`.

No cognition, gating, Provider Runtime, RapidOCR, Gateway, Evidence, or
downstream semantics were changed. No runtime was executed by the Agent.

## Final terminal verification

The post-fix user-terminal verification reported:

- `all_checks_passed=true`;
- `check_count=43`;
- `failed_checks=[]`;
- `operational_result=PASS`;
- `cognitive_logic_result=PASS`;
- `dynamic_real_provider_invocation_count_one=true`;
- Dynamic t0 remained ineligible with zero Provider invocation;
- Dynamic t1 became eligible and performed exactly one real RapidOCR
  invocation;
- `not_required_blocks_provider_execution=true`;
- `provider_runtime_admission_not_bypassed=true`;
- `recorded_provider_result_not_used=true`;
- `validation_errors_empty=true`.

The phase status is now `GO — VERIFIED — PHASE CLOSED`.
