# Roboflow External Perception Provider Integration Asset Audit v1

**Phase:** `Phase-P1-Roboflow-External-Perception-Provider-Integration-Asset-Audit-v1-001`  
**Canonical physical root:** `/Users/luanlei/Desktop/Luna-Core`  
**Disposition:** repository inspection and planning only

No Python, project runner, verifier, network request, Roboflow call, model
load, dependency installation, or runtime mutation was performed for this
audit.

## 1. Executive Summary

Luna already has the principal ownership and evidence boundaries needed to
treat Roboflow as an external perception provider. The canonical owner is
**Provider Governance**. Roboflow should attach through the existing Provider
Registry, Model Registry/model-provider binding surfaces, and the existing
Field Perception Orchestrator/Observation-to-Evidence adapter boundary.

The repository does not yet contain a repository-backed declaration for the
requested first workflow:

```text
provider       = roboflow
workspace      = lei-luan
workflow_id    = custom-workflow
capability     = object_detection
model          = rf-detr-small
input          = image
primary output = predictions
```

The current declaration is a generic Roboflow POC entry and points to
`workflow:roboflow:vision-poc:v1` plus generic POC model references. No
repository occurrence of `lei-luan`, `custom-workflow`, or `rf-detr-small`
was found in the inspected `capabilities/`, `docs/`, and `configs/` trees.
Consequently, the first RF-DETR smoke is **not yet ready for an honest
governed runtime implementation**. The missing work is a declaration and
binding extension, not a new Provider architecture.

The shortest intended path is:

```text
Observation / Capability request
  → existing capability and slot resolution
  → existing governed model/provider binding references
  → Runtime / Provider admission boundary
  → one Roboflow Provider adapter
  → inference_sdk.InferenceHTTPClient.run_workflow
  → adapter-private native result
  → Luna-normalized Detection evidence candidate
  → Observation Gateway evidence boundary
  → Current World candidate where required
  → A / existing cognitive consumer
```

Roboflow must never become an owner of Need, Attention, Evidence semantics,
Current World, Field, Hypothesis, Sufficiency, Decision, Task, Action,
Memory, or Brain outcome authority.

## 2. Existing Asset Inventory

### 2.1 Governance and registry assets

| Asset | Evidence | Status | Audit disposition |
|---|---|---|---|
| Provider registry | `capabilities/midplatform/model_manager/registry/provider_registry_v1.json` (`LunaProviderRegistryV1`) | Existing registry with legacy and newer candidate entries | Reuse and minimally extend; do not create a Roboflow registry |
| Roboflow provider declaration | same file, `roboflow_vision_poc` entry, lines 294–336 | Candidate/pending, external API, Provider Governance owner | Reusable boundary declaration, but generic POC only |
| Capability registry and slot | `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`, `object_detection` and `slot:object-detection:vision:v1` | Existing slot; `UNBOUND`, candidate-only | Reuse; no direct YOLO/Roboflow binding at slot level |
| Model registry | `capabilities/midplatform/model_manager/registries/model_registry_v1.json` | Existing model declarations, including YOLO11n; no RF-DETR | Extend only under Model Governance for `rf-detr-small` |
| Capability/model binding registry | `capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json` | Existing object-detection ↔ YOLO11n binding; Capability Governance lifecycle owner | Extend with a real RF-DETR binding only after model declaration exists |
| Model/provider binding registry | `capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json` | Existing YOLO ↔ local provider binding; Provider Governance lifecycle owner | Extend with Roboflow binding metadata; no duplicate binding hierarchy |
| Provider registry loader | `capabilities/midplatform/model_manager/registry/provider_registry_loader_v1.py` | Existing loader | Reuse for future declaration discovery |
| Declaration baseline validator | `capabilities/midplatform/model_manager/registry/declaration_baseline_controlled/` | Controlled validator/verifier for existing declaration baseline | Reuse/extend later; not changed here |

The registry surface is not internally uniform: the provider registry contains
older model-oriented provider rows and newer governed candidate rows. This is
an integration risk, but not evidence for creating a second registry.

### 2.2 Model Contract Repository

`capabilities/midplatform/model_manager/model_contract_repository/` contains
the reusable `ModelAssetContractV1`, `LoaderContractV1`,
`ProviderAdapterContractV1`, `CapabilityContractV1`, `EvidenceContractV1`,
and resolution/compatibility records. The resolver supports explicit model
asset identity and compatibility records. The repository also contains
YOLO11n-specific provisioning/readiness assets. Those are useful conventions,
but they do not declare RF-DETR and must not be copied into a new Roboflow
model manager.

Classification:

- `ModelAssetContractV1` and contract resolution: **REUSE** for declarations.
- YOLO11n provisioning/readiness fixtures and probes: **LEGACY or
  model-specific reference**, not a Roboflow declaration.
- Physical dependency/checksum probes: **OUT OF SCOPE** for this audit and
  not allowed for declaration-only onboarding.

### 2.3 Provider runtime and FPO assets

| Asset | Evidence | Status |
|---|---|---|
| Provider Manager runtime skeleton | `capabilities/midplatform/provider_manager_runtime_skeleton/` | Planning/dry-run skeleton; explicit no runtime activation/real provider runtime |
| Provider runtime governance | `capabilities/midplatform/provider_runtime_governance/` | Planning/governance skeleton; not a connected external provider dispatcher |
| Generic FPO visual handoff | `field_perception_visual_handoff_*`, `field_perception_visual_invocation_*` under `capabilities/midplatform/field_perception_orchestrator/integration/` | Existing candidate-only request/capability/model handoff surface |
| Existing real visual evidence types | `field_perception_real_vision_evidence_types_v1.py` | Existing `VisionProviderAdmissionCandidateV1`, native detection record, visual evidence candidate, Gateway handoff candidate |
| Existing Gateway adapter | `capabilities/midplatform/core/observation_gateway/integration/real_visual_evidence_gateway_adapter_v1.py` | Existing evidence admission boundary; produces candidate-only observation/evidence records |
| Active observation control | `field_perception_active_observation_control_types_v1.py` and engine | Existing demand/request/requirement/sufficiency/next-cycle candidates; A/FPO control boundary |
| Existing Roboflow PoC | `capabilities/midplatform/field_perception_orchestrator/integration/roboflow_provider_poc/` | Controlled PoC candidate; not canonical registry or production runtime |
| Existing real YOLO path | `.../yolo11n_single_frame_execution/` and `field_perception_real_vision_provider_adapter_v1.py` | YOLO-specific controlled/compatibility path; not a generic Roboflow abstraction |

The FPO/vision adapter family already expresses the needed distinction between
provider-native records and Luna-owned evidence. The existing Roboflow PoC
should therefore be treated as a narrow candidate integration to be aligned
with these assets, not as a source for a parallel Provider layer.

## 3. Canonical Owner Findings

### A. Roboflow owner

Roboflow belongs to **Provider Governance** as an external Vision Execution
Provider declaration and provider-facing compatibility binding.

Evidence:

- `provider_registry_v1.json` assigns the existing Roboflow POC entry to
  `Provider Governance` and explicitly sets `capability_owner: false` and
  `model_owner: false`.
- The frozen architecture assigns Provider Governance the provider identity,
  provider-facing binding lifecycle, Provider Admission, and invocation
  boundary.
- Model Governance remains the source of model identity/declarations.
- Capability Governance remains the source of capability/slot and
  Capability↔Model binding lifecycle.

Roboflow is not a Capability Registry owner, Model Manager owner, FPO semantic
owner, World State owner, or Decision owner.

### B. Provider Manager assessment

**Decision: existing declaration/registry surface can be reused, but the
Provider Manager runtime skeleton is not suitable as a new canonical owner and
needs no new parallel runtime implementation.**

The existing registry and `ProviderAdapterContractV1` provide enough shape for
provider identity, contract, adapter, supported capabilities, and lifecycle
metadata. The runtime skeletons are explicitly planning/dry-run assets, not an
already-connected external Provider abstraction. The minimum future extension
is to carry governed workflow/deployment configuration and the actual
Roboflow adapter contract through the existing registry/binding surface.

This is a **minimum extension to existing Provider Governance assets**, not a
new `ProviderSelector`, `ProviderManager`, or workflow-specific client family.

### C. Most defensible object-detection call chain

The existing assets support the following conceptual chain without forcing
unrelated layers:

```text
ObservationDemandCandidateV1 / ObservationRequestCandidateV1
  → CapabilityRequirementCandidateV1
  → Capability Registry + Universal Capability Slot
  → Capability↔Model governed binding
  → Runtime Admission / executable candidate
  → VisionProviderAdmissionCandidateV1
  → one external Roboflow provider adapter
  → Provider Result (native, private)
  → VisualDetectionEvidenceCandidateV1
  → ObservationGatewayEvidenceHandoffCandidateV1
  → Gateway candidate/admission boundary
  → CurrentWorldCandidateV1 if the current flow requests it
  → A-owned interpretation/reassessment
```

The current `object_detection` slot declares `RawFrameReferenceV1` input and
`evidence:visual-detection-candidate:v1` output. Its `UNBOUND` state and
`model_binding_owned_elsewhere: true` correctly keep Slot separate from Model.

The existing Provider Registry's capability-first records should not be
interpreted as permission for FPO or a model-specific helper to select a
provider outside the governed binding/admission path.

## 4. Reusable Assets

The following assets should be reused in a future implementation phase:

1. `LunaProviderRegistryV1` and its loader for Provider Governance identity
   and lifecycle references.
2. `LunaCapabilityRegistryV1` and the existing universal object-detection
   slot for capability/slot identity.
3. `ModelAssetContractV1`, `ProviderAdapterContractV1`,
   `CapabilityContractV1`, and `EvidenceContractV1` for declarations and
   compatibility references.
4. `VisionProviderAdmissionCandidateV1` for bounded provider admission input;
   its existing fields include capability/model/provider session refs, trace,
   provenance, candidate-only and mutation guards.
5. `ProviderNativeDetectionRecordV1` for adapter-private normalized native
   provider records.
6. `VisualDetectionEvidenceCandidateV1` and
   `ObservationGatewayEvidenceHandoffCandidateV1` for Luna evidence and
   Gateway handoff.
7. `ObservationDemandCandidateV1`, `ObservationRequestCandidateV1`, and
   `CapabilityRequirementCandidateV1` for upstream request context.
8. `CurrentWorldCandidateV1` and active observation sufficiency/next-cycle
   candidates as downstream candidate surfaces only.
9. Existing trace/provenance/source-version fields in the FPO and Gateway
   records.
10. Model Test Lens TestBoard/MUEP/result-envelope conventions for a future
    candidate evaluation artifact, without turning Test Lens into a Provider
    or Evidence owner.

## 5. Assets That Must Be Extended

No existing code is modified in this audit. The minimum future extensions are:

### 5.1 Real Roboflow declaration set

Extend existing governance registries with owner-controlled declarations for:

- a `rf-detr-small` Model Governance asset: model identity, version, weights
  declaration, loader/dependency declaration, object-detection capability
  declaration, external workflow/deployment metadata, lifecycle, source
  versions, and provenance;
- a Capability Governance binding from the existing object-detection slot to
  that model asset;
- a Provider Governance Roboflow provider/workflow binding for
  `custom-workflow`, workspace `lei-luan`, provider contract/version, adapter,
  input/output mapping, and compatibility metadata;
- any required deployment/workflow profile only if an existing registry
  concept cannot express it.

The new declaration must not be created by a Runner or fixture and must not
be marked admitted merely because the workflow name is known.

### 5.2 External provider adapter contract

The existing Roboflow PoC `provider_client_v1.py` already uses the official
SDK route and is a usable candidate boundary. A future implementation should
align its provider declaration with the implementation dependency: the
registry currently declares `dependency:python:stdlib:urllib` while the
client imports `inference_sdk.InferenceHTTPClient` (client lines 203–210).
That is declaration/implementation drift to resolve under Provider
Governance; it is not a reason to preserve a fabricated HTTP transport.

### 5.3 Evaluation output alignment

If the external smoke is displayed in Model Test Lens, add only the minimum
mapping from the external provider trial to the existing TestBoard/MUEP or
runner-output envelope. Provider identity, workflow/model refs, trace, and
candidate boundary must remain present in the trial manifest/result. Do not
make MUEP a canonical Evidence schema.

## 6. Assets That Must NOT Be Duplicated

Do not create any of the following:

- `roboflow_rf_detr_client.py`, `roboflow_depth_client.py`, or one client per
  workflow/model;
- a Roboflow-specific Capability Registry or Model Registry;
- a unified AI registry with ownership over Capability, Model, and Provider;
- a Provider Selector, Model Selector, Runtime Manager, FPO Manager, or
  Binding Manager;
- a second `VisionExecutionProvider` abstraction if the existing
  `ProviderAdapterContractV1` plus FPO/provider boundary can carry the same
  contract;
- a raw-response-as-Evidence type;
- a Roboflow-to-World-Fact or Roboflow-to-Decision shortcut;
- a custom canonical `_eval_out` schema parallel to TestBoard/MUEP.

## 7. Proposed Minimal Integration Path

The future implementation should wire one generic adapter to registered
workflow metadata:

```text
1. Existing Observation/Capability request
2. Existing Capability and Slot resolution
3. Capability Governance binding to a declared model asset
4. Model Governance declaration lookup
5. Provider Governance model/provider/workflow compatibility binding
6. Runtime/Provider admission refs (not invented by FPO)
7. FPO builds a bounded request from those refs
8. Roboflow adapter calls the official SDK only in explicit real mode
9. Native result remains private to the adapter
10. Adapter emits normalized candidate records
11. Existing Gateway validates/admit-handoffs Evidence candidate
12. Existing Current World/A path consumes candidates
```

The adapter may perform request construction, transport, response
normalization, metadata correlation, and error translation. It may not infer
the exit, form Hypothesis, decide Sufficiency, select another Provider, or
create a Decision.

## 8. Roboflow Workflow Binding Analysis

### Current repository state

The current provider declaration contains `workflow_ref` and supported model
references, but only for the generic POC workflow:

```text
provider_ref  = provider:roboflow:vision:poc:v1
workflow_ref  = workflow:roboflow:vision-poc:v1
models        = model:roboflow:object-detection:poc:v1,
                model:roboflow:ocr:poc:v1
```

The current PoC request type also has `workflow_ref` and a configurable
`workflow_output_mapping`; its structural fixture maps `detections` to
`$predictions` and `ocr` to `$ocr`. These are candidate integration fields,
not proof that the requested `custom-workflow` exists as a governed Luna
declaration.

### Recommended classification

`workflow_id` is provider/deployment/workflow configuration associated with a
Provider binding. It is not Capability identity and not Model identity. The
model asset may reference the workflow as a deployment/compatibility
declaration when the model is externally hosted, but workflow lifecycle must
remain with Provider Governance.

Use an existing provider registry/binding field if it can carry:

- provider workspace/tenant reference;
- workflow identity/version;
- input contract name (`image`);
- declared output mapping (`predictions`, and OCR only if the workflow
  actually emits it);
- deployment/runtime profile reference;
- source version and provenance.

If current schemas cannot carry these fields, extend the narrowest existing
Provider Registry or Model↔Provider binding schema. Do not create a parallel
workflow registry without a separate architecture review.

### Twelve-workflow expansion

No formal repository registry for the user-described twelve workflows was
found in the inspected trees. The repository therefore cannot yet prove a
registry-style expansion for all twelve. The correct target remains:

```text
one generic Roboflow Provider adapter
+ multiple governed workflow/provider bindings
```

Each binding supplies provider/workflow/capability/input/output/model or
deployment metadata. A workflow-specific client is not justified.

## 9. Raw Response Boundary

The raw Roboflow response must terminate at the Roboflow Provider adapter.
The current PoC provides the correct shape:

- `RoboflowNativeResultV1.payload` is explicitly adapter-private;
- `RoboflowNormalizedProviderResultV1` carries normalized candidate outputs;
- `VisualDetectionEvidenceCandidateV1` carries Luna-owned detection evidence
  fields;
- the Gateway adapter converts visual evidence into candidate-only Gateway
  records with `fact_declared: false` and no source mutation.

The boundary is:

```text
raw Roboflow SDK result
  ≠ Provider Result contract
  ≠ Luna Evidence candidate
  ≠ Current World truth
  ≠ Field mutation
  ≠ Decision
```

Native keys must not be copied into canonical Luna types without a governed
output mapping. For the RF-DETR workflow, `predictions` should be a declared
workflow output mapping, not a hardcoded universal Roboflow schema assumption.

## 10. Evidence / Normalization Boundary

Detection and OCR remain separate evidence families. The existing PoC types
already separate `detection_evidence` from `ocr_evidence`; the existing
Gateway `PerceptionEvidenceV1` carries provider/model/region/temporal,
confidence-candidate, uncertainty, contradiction, trace, provenance, and
`fact_declared: false`.

Required future behavior:

- provider confidence is evidence metadata only;
- evidence uncertainty and contradiction refs remain explicit;
- missing OCR is a valid result, not automatic semantic failure;
- conflicting Detection/OCR records remain independently traceable;
- no normalized record may claim World Truth;
- Gateway admission/fact admission remains a separate governed boundary.

The existing MUEP runner policy reinforces this: detection/OCR outputs are
candidate envelopes, require fact admission before fact write, and forbid
navigation/fact labels. MUEP is an evaluation protocol, not a substitute for
the Observation Gateway or Evidence contract.

## 11. Model Test Lens Integration Finding

Model Test Lens is a local static model-testing/observation surface, not a
canonical external Provider or Evidence owner.

Evidence:

- `model_test_lens_types_v1.py` says the Lens reads `_tmp_eval_out`, TestBoard,
  and test assets and visualizes candidate output, metrics, failure modes, and
  trace.
- `local_runner_bridge_types_v1.py` uses `_tmp_eval_out/model_test_lens_local_runner_bridge`,
  requires TestBoard, and describes a candidate-only job/result surface.
- `standards/muep/README.md` defines candidate-only evaluation results and
  explicitly says scores do not grant runtime readiness.
- `schemas/controlled_runner_execution/runner_output_envelope_policy_v1.json`
  forbids direct fact/navigation output and requires fact admission before
  fact write.

Finding: Test Lens can later observe a Roboflow trial if a runner/test
manifest maps provider result metadata into the existing evaluation output
and trace conventions. It does not currently prove that it can directly
consume an external Roboflow result as canonical Evidence. No UI change is
allowed or needed in this audit.

### Smoke output decision

The repository has an `_tmp_eval_out` convention and formal MUEP/TestBoard
artifacts. Do not make `raw_response.json`, `normalized_evidence.json`, or a
new Roboflow `_eval_out` layout a canonical schema. A future smoke may use the
existing TestBoard/result-manifest location, with any raw SDK payload retained
only as adapter-private diagnostic material and with explicit candidate-only
flags.

## 12. Credential Boundary

The existing Roboflow PoC client reads credentials/configuration from the
process environment in `provider_client_v1.py` lines 175–190:

- `ROBOFLOW_API_KEY`;
- `ROBOFLOW_API_URL` or `INFERENCE_SERVER_URL`;
- `ROBOFLOW_WORKSPACE`;
- `ROBOFLOW_WORKFLOW_ID`.

The client does not store a secret in a repository file or Provider Registry.
The credential boundary should remain an external environment/secret
configuration boundary owned by deployment/runtime operations, while Provider
Governance owns the declaration that a credential is required. No key file,
registry secret, or committed `.env` was created.

The requested first real values are:

```text
ROBOFLOW_API_KEY = user secret, external only
ROBOFLOW_API_URL = https://serverless.roboflow.com (Inference Server base URL)
ROBOFLOW_WORKSPACE = lei-luan
ROBOFLOW_WORKFLOW_ID = custom-workflow
```

These values are user-provided runtime configuration, not repository-backed
governance declarations. The current repo does not contain the workspace or
workflow declaration needed to connect them to a governed binding.

## 13. Negative Guards

Any future Roboflow integration must preserve all of the following:

- no World State ownership;
- no Field State mutation;
- no Intent mutation;
- no Attention Need creation or final priority assignment;
- no Capability Resolution ownership;
- no Model identity/lifecycle ownership;
- no Runtime Admission ownership;
- no Provider binding lifecycle duplication;
- no Provider semantic fallback or autonomous re-observation;
- no Hypothesis formation by the Provider;
- no Sufficiency decision from provider confidence;
- no Decision, Task, or Action creation/execution;
- no Memory/Experience mutation;
- no direct Truth admission;
- no direct UI ownership;
- no bypass of Capability/Model/Provider governance;
- `candidate_only = true` for trial outputs;
- `truth_declared = false`, `fact_declared = false`, and source mutation false
  until the canonical owner/admission boundary says otherwise.

## 14. First Smoke Test Plan

This is a future plan, not an execution result.

### Input

- local/static image reference supplied through an Observation request;
- object-detection capability request;
- existing object-detection slot and governed binding refs;
- RF-DETR model/deployment declaration once registered;
- Roboflow Provider/workflow binding once registered;
- full-frame ROI or existing Observation frame/ROI reference;
- trace, provenance, source versions, and invalidation refs.

### Provider call

Use the official SDK transport already present in the PoC candidate:

```python
InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=<external secret>,
).run_workflow(
    workspace_name="lei-luan",
    workflow_id="custom-workflow",
    images={"image": <local image>},
    use_cache=True,
)
```

The code block is a target contract only; it was not executed. The current
client implementation uses `parameters={}` rather than an explicit
`use_cache=True` argument. That transport/configuration difference should be
resolved in a later implementation phase against the selected SDK version;
this audit does not change it.

### Result path

```text
SDK result
  → adapter-private native result
  → normalized detection candidate(s)
  → Gateway evidence handoff candidate
  → candidate-only visual evidence
  → Current World candidate if requested by the existing path
  → downstream A/cognitive consumer
```

The first smoke should stop before Field mutation, World Truth, Decision,
Task, Action, or any autonomous second observation. If later cognition finds
an information gap, it should return a Luna-owned next-observation candidate
for review rather than letting Roboflow loop.

### Evaluation questions

The smoke should inspect structure rather than encode which detected object is
the exit:

- did the result correlate to the request/frame/ROI?
- are provider/workflow/model refs retained?
- are detection candidates separate from truth?
- did the evidence cross the existing Gateway boundary?
- are trace/provenance/source versions reversible?
- did no Provider result create a Decision or World Truth?

## 15. Risks / Blockers

### Structural blockers

**B1 — P1 — Missing RF-DETR governed declaration set.**  There is no
repository-backed `rf-detr-small` Model Registry declaration, no binding from
the existing object-detection slot to that model, and no
`custom-workflow`/`lei-luan` Provider Governance binding. A real implementation
must stop closed until these declarations exist.

**B2 — P2 — Provider declaration/implementation drift.** The Roboflow
Provider Registry entry declares `urllib`, while the current PoC imports
`inference_sdk`. The official SDK route is the stated target, but the
dependency declaration must be aligned by a future Provider Governance change.

**B3 — P2 — External result-to-Test-Lens mapping is not a canonical Evidence
path.** Test Lens has evaluation envelopes and trace conventions, but the
repository does not yet prove a registered external-provider result manifest
that carries all Roboflow metadata into those artifacts.

**B4 — P2 — Credential/configuration is external and unregistered.** The
environment names exist in the PoC client, but no secret is intentionally
available in repository assets and no actual workflow ID/configuration is
declared.

### Non-blocking design risks

- The existing Provider Registry mixes historical and newer record shapes;
  future extension must avoid accidentally treating legacy model rows as
  canonical lifecycle owners.
- A workflow that outputs only `predictions` does not prove OCR support. OCR
  must remain a separately declared capability/workflow output unless the
  selected workflow declaration explicitly supplies it.
- Remote-provider licensing, data handling, retention, workspace policy, and
  deployment terms require user/provider review. No commercial deployment
  decision is made here.

## 16. Recommended Next Phase

`Phase-P1-Luna-Roboflow-RFDETR-Provider-Declaration-And-Observation-Evidence-Seam-Implementation-v1-001`

That phase should first add/extend the existing owner-controlled declarations
and then wire one generic Roboflow adapter into the existing Observation and
Evidence boundary. It should not add a new registry or execute the Provider
until declaration, dependency, credential, workflow, and evidence mapping
reviews are complete.

## 17. Stop Conditions

Stop before implementation or execution if any of the following remains true:

- RF-DETR model identity/version/declaration is missing;
- object-detection Capability↔Model binding is missing or stale;
- Roboflow Provider/workflow binding is missing or owner-ambiguous;
- selected workflow input/output mapping is not declared;
- SDK dependency/version is not pinned or transport contract is unresolved;
- credential boundary is not externally prepared;
- raw provider schema would leak into Luna canonical records;
- evidence cannot enter the existing Gateway candidate/admission boundary;
- Provider, FPO, or Test Lens would gain semantic/World/Decision authority;
- verification requires a hardcoded answer or fixture-only success.

## Audit Disposition

The architecture is **compatible in principle but not implementation-ready for
the requested RF-DETR workflow**. The correct next step is a declaration and
binding seam review/implementation under existing governance owners. This
audit created documentation only and made no runtime or source-code change.
