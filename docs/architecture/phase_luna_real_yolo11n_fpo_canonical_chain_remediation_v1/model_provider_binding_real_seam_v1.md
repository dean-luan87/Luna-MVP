# Model↔Provider Binding Real Seam v1

Validation requires:

- Provider Governance ownership/lifecycle ownership;
- model asset and model-version continuity with Capability↔Model binding and
  Executable Capability;
- compatible Provider contract or binding reference;
- no Model↔Provider invalidation;
- preserved trace/provenance.

The FPO Provider adapter receives the binding reference. It does not create a
Provider binding, select a Provider family, or invoke Provider Admission.

