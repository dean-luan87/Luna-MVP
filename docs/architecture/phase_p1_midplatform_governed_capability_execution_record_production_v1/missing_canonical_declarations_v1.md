# Missing Canonical Declarations

The producer detects the following blockers for the YOLO11n case:

1. No canonical `model_registry_v1.json` entry for
   `model-asset:yolo11n:weights-v1`.
2. No canonical Provider Registry entry for the `yolo` Provider family and
   its Provider contract/adapter lifecycle.
3. No canonical Capability↔Model governed binding declaration connecting the
   `object_detection` Capability/Slot to the YOLO11n Model Asset.
4. No canonical Model↔Provider governed binding declaration connecting the
   YOLO11n Model Asset to a Provider Registry declaration.
5. No non-controlled Runtime Admission record producer for the real path.
6. No owner-issued complete bundle containing all five upstream records.

The repository does contain supporting candidate evidence, but candidate
evidence is not promoted automatically:

- Model Contract Repository: YOLO11n candidate Model Asset and YOLO adapter
  contract.
- Official Capability Catalog: FPO/provider supporting mapping.
- Capability Registry: `object_detection` mapped to `detection_v1`, not to
  YOLO11n.

The correct owner actions are Model Governance, Provider Governance,
Capability Governance, and Runtime Admission respectively.  The integration
producer does not repair any declaration.

