# Migration Integrity Validation Architecture

## Mandatory validation dimensions

### 1. Architecture completeness

The post-migration architecture must contain Field, Personal Cognitive Network,
Role, Relationship, Experience, Intent, Causal, Decision, and Action nodes. Each
node must have a canonical owner, status, source assets, target position, and
dependency contract.

### 2. Asset ownership completeness

Every mapped asset must end in one of `aligned`, `preserved`, `adapted`, `blocked`,
or `retired_candidate`. “TBD” and unassigned owners block the freeze. Capability
assets such as OCR/Vision remain in the Capability Layer; Field State Reducer
remains under Field; Task Manager remains orchestration; Model Manager remains
Capability Governance.

### 3. Boundary integrity

The validation must prove that Task Manager does not perform causal judgment,
Model Manager does not generate cognitive conclusions, OCR/Vision evidence cannot
become fact without admission, Memory cannot directly mutate the cognitive core,
Personal Cognitive Network cannot absorb source ownership, and Intent/Causal
layers cannot execute decisions or actions.

### 4. Cognitive chain integrity

The required chain is:

```text
Input → Environment Understanding → Field → Intent
→ Context Retrieval / Personal Cognitive Network Projection
→ A/B Route Boundary → Decision → Action → Feedback → Experience
```

Every edge requires a producer, consumer, contract reference, candidate/fact
semantics, failure behavior, trace reference, and compatibility result. A missing
edge blocks the freeze decision.

### 5. Regression integrity

The future controlled validation must cover Vision Pipeline, OCR Pipeline, Model
Admission, Task Manager, Field State Reducer, and Protocol Manager. Existing
module baselines and their ready evidence remain the reference. Architecture
alignment must not silently change public APIs, owners, candidate semantics,
trace/replay behavior, or forbidden authorities.

## Result

The integrity phase may return `validated`, `blocked`, or `remediation_required`.
It cannot activate Runtime or freeze the baseline by itself. Only the subsequent
Architecture Freeze Decision can promote the candidate after user V2 and ChatGPT
V3 governance.

