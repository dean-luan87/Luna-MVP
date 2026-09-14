# Installation and Runtime Requirements

## Required package/image

Real mode uses the lightweight official Roboflow client package
`inference-sdk` and `InferenceHTTPClient`. The agent does not install it.
No full `inference` package, GPU image, Docker image or model download is
required by this PoC transport boundary. Repository Python 3.10+ syntax is
assumed.

User-terminal installation command:

```sh
python3 -m pip install inference-sdk
```

The repository currently has no dependency pin for this package. The user
should select and record a compatible version before a repeatable trial.

## Real-provider requirements

- Roboflow account/workspace and an approved workflow/model declaration;
- Inference Server base URL represented by `ROBOFLOW_API_URL` (or the
  repository-supported fallback `INFERENCE_SERVER_URL`);
- `ROBOFLOW_WORKSPACE`;
- `ROBOFLOW_WORKFLOW_ID`;
- API key represented by `ROBOFLOW_API_KEY`;
- a local static image file;
- valid governed Capability/Model/Runtime/Provider Admission references;
- explicit external-network permission.

No secret is stored in the repository or Provider Registry.

The workflow must expose one image input named `image`. Detection and OCR
output paths must be supplied through the governed
`workflow_output_mapping` in the real input; the adapter does not guess
native output keys. The real input must also replace every
`USER_REQUIRED:*` governance/configuration placeholder before execution; the
request builder fails closed while any remains.

## Licensing and deployment

Roboflow service, workflow, model and dataset terms must be reviewed by the
user. Existing Roboflow Universe dataset assets already require per-dataset
license/source admission. This PoC does not implement commercial licensing,
deployment, camera access, continuous video, Jetson or TensorRT optimization.
