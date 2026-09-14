# Provider Adapter Boundary

`provider_client_v1.py` uses the official `inference_sdk.InferenceHTTPClient`
transport in explicit real mode. The SDK is transport only; it is not a Luna
canonical type or authority owner.

The client requires:

- explicit `real_mode=True`;
- a valid governed request containing Provider Admission, Runtime Admission,
  Capability/Model and Model/Provider refs;
- `ROBOFLOW_API_KEY`;
- `ROBOFLOW_API_URL` as the Inference Server base URL (or
  `INFERENCE_SERVER_URL`);
- `ROBOFLOW_WORKSPACE`;
- `ROBOFLOW_WORKFLOW_ID`;
- an existing local image file;
- no invalidation refs.

The request carries `workflow_output_mapping` for the `detections` and `ocr`
outputs. The mapping is a governed configuration seam, not a speculative
list of native keys. It may address a mapping root or the one-image result
sequence using explicit paths such as `$.detections` or `$[0].detections`,
according to the declared Workflow output shape. The workflow receives the
image under the official `image` input name.

Structural mode accepts only an explicitly supplied synthetic native payload
and marks `actual_provider_response=false`. Real mode does not accept a native
fixture payload and uses the selected external transport.

The native payload is consumed only by `evidence_translator_v1.py`. The
normalized output exposes Detection/OCR candidates, provider/model/workflow
refs, versions, trace and provenance, but not the native Roboflow payload.
Provider confidence remains evidence metadata and cannot set Sufficiency.
