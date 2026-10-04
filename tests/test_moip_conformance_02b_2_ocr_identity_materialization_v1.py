import json
from pathlib import Path

from capabilities.midplatform.model_manager.registry.provider_current_state_read_v1 import (
    read_provider_current_state,
)
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    filter_routing_eligible,
    is_provider_routing_eligible,
    load_provider_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"


def _providers():
    return load_provider_registry()["providers"]


def _provider(model_id):
    return next(item for item in _providers() if item.get("model_id") == model_id)


def test_ocr_declaration_materializes_proven_provider_id():
    assert _provider("ocr_v1")["provider_id"] == "provider:ocr_v1"


def test_ocr_provider_owner_read_succeeds():
    assert read_provider_current_state("provider:ocr_v1")["read_status"] == "BOUNDED_STATIC_CURRENT_STATE"


def test_ocr_owner_read_returns_exact_identity():
    assert read_provider_current_state("provider:ocr_v1")["identity_ref"] == "provider:ocr_v1"


def test_ocr_lifecycle_and_admission_are_unchanged():
    record = _provider("ocr_v1")
    assert record["lifecycle_state"] == "active"
    assert record["admission_status"] == "admitted"


def test_internvl_legacy_record_remains_visible():
    assert _provider("internvl2_5")["model_id"] == "internvl2_5"


def test_internvl_has_no_synthesized_provider_id():
    assert "provider_id" not in _provider("internvl2_5")


def test_internvl_is_excluded_from_production_pool():
    assert not is_provider_routing_eligible(_provider("internvl2_5"))


def test_gemini_legacy_record_remains_visible():
    assert _provider("gemini_vision")["model_id"] == "gemini_vision"


def test_gemini_has_no_synthesized_provider_id():
    assert "provider_id" not in _provider("gemini_vision")


def test_gemini_is_excluded_from_production_pool():
    assert not is_provider_routing_eligible(_provider("gemini_vision"))


def test_yolo_identity_is_unchanged():
    assert _provider("yolo11n")["provider_id"] == "provider:yolo:local:v1"


def test_yolo_controlled_identity_reference_is_unchanged():
    assert _provider("yolo11n")["provider_id"] == "provider:yolo:local:v1"
    assert _provider("yolo11n")["model_id"] == "yolo11n"


def test_missing_provider_id_cannot_fallback_to_model_id():
    record = {"model_id": "legacy", "lifecycle_state": "active", "admission_status": "admitted"}
    assert not is_provider_routing_eligible(record)


def test_missing_provider_id_cannot_enter_active_production_pool():
    record = {"model_id": "legacy", "lifecycle_state": "active", "admission_status": "admitted"}
    assert record not in filter_routing_eligible([record])


def test_raw_registry_inspection_preserves_legacy_records():
    raw = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    ids = {item.get("model_id") for item in raw["providers"]}
    assert {"internvl2_5", "gemini_vision"}.issubset(ids)
