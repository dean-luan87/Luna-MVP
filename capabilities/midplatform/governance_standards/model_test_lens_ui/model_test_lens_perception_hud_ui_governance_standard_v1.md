# Model Test Lens Perception HUD UI Governance Standard V1

Canonical path for governance_standards library.

## Scope

All Model Test Lens model test pages (Segmentation, Detection, OCR, SLAM, Depth, ASR, TTS, Speaker, Face, VLM).

## Mandatory references

- `capabilities/midplatform/model_test_lens/standards/ui/model_test_lens_ui_standard_v1.md`
- `capabilities/midplatform/model_test_lens/standards/perception_hud/perception_hud_ui_template_standard_v1.md`
- `capabilities/midplatform/model_test_lens/standards/perception_hud/perception_hud_model_adapter_requirements_v1.json`

## Rules

1. **all_future_model_test_pages_must_follow** Model Test Lens UI Standard V1
2. Default view must include Visual Compare or HUD-equivalent
3. Reasoning panel with observations, uncertainty, recommendations is required
4. HUD is read-only; uses existing envelope only
5. Candidate outputs must not be presented as facts
6. No navigation instructions or speech output from HUD
7. Advanced and Developer modes must remain available

## Registry

See `model_test_lens_ui_standard_registry_v1.json`.
