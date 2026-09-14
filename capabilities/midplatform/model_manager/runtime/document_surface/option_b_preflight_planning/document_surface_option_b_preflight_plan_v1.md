# Option B Preflight Planning v1

Planning-only phase for A1/C1 `admitted_for_preflight_candidate` scope.

**Allowed:** Define preflight checklist, abort conditions, trace fields, output boundaries.  
**Forbidden:** Preflight execution, Option B execution, segmentation, download/install, image read, active registry, runtime activation.

## Preflight candidates

- A1 `family_a_classical_helper_ok_candidate` — classical_lightweight_segmentation_helper
- C1 `family_c_document_specific_surface_model_ok_for_preflight` — document_specific_segmentation_surface_model

Blocked candidates (A2/B1/B2/B3/C2/D1) remain blocked reference only.

## Next phase

`OptionB-Preflight-DryRun-v1-001` — validate checks block correctly; still no execution.
