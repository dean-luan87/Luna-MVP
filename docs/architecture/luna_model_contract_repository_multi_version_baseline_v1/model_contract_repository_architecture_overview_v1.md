# Model Contract Repository Multi-Version Baseline

The canonical owner is the existing `Model Manager / Model Governance` subsystem.
This phase adds a narrow repository and resolver beneath that owner. It does not
own observation, decision, task, field, context, or evidence semantics.

The frozen chain is:

`Model Asset Identity → Contract Resolution → Compatibility Validation → Model Manager Admission`

Asset, loader, provider adapter, capability, and canonical evidence versions are
independent. The current `yolov5n.pt` resolves uniquely to its declared local
YOLOv5 loader contract, then remains blocked because the local source package is
not registered. No inference, download, or provider invocation occurs here.
