# Roboflow Provider Declaration

The existing Provider Registry now contains a candidate declaration:

`provider:roboflow:vision:poc:v1`

It records:

- Provider Governance ownership;
- `roboflow` provider family;
- external API execution mode;
- workflow/model refs;
- Provider contract `v1`;
- object detection and text recognition support;
- dependency/runtime requirement refs;
- source versions, provenance and invalidation refs;
- `candidate` lifecycle and `pending` admission status.

The declaration explicitly sets `capability_owner=false`, `model_owner=false`,
`provider_admission_implied=false`, `provider_invocation_implied=false` and
`model_loading_implied=false`.

Actual workflow/model declarations and Provider Admission promotion remain
governed prerequisites. The declaration does not itself make the external
service executable.

