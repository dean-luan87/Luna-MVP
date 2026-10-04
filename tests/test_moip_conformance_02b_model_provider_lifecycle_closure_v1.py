from capabilities.midplatform.model_manager.engines import model_provider_routing_lifecycle_closure_v1 as closure
from capabilities.midplatform.model_manager.registry import provider_registry_loader_v1 as loader


def _state(*, lifecycle="active", admission="admitted", status="BOUNDED_STATIC_CURRENT_STATE"):
    return {
        "read_status": status,
        "source_revision": "declaration:test:v1" if status == "BOUNDED_STATIC_CURRENT_STATE" else None,
        "currentness_basis": "locked_test_declaration" if status == "BOUNDED_STATIC_CURRENT_STATE" else None,
        "lifecycle_state": lifecycle,
        "admission_status": admission,
    }


def _provider():
    return {"provider_id": "provider:test", "model_id": "model:test"}


def _patch(monkeypatch, provider_state=None, model_state=None):
    monkeypatch.setattr(closure, "read_provider_current_state", lambda _: provider_state or _state())
    monkeypatch.setattr(closure, "read_model_current_state", lambda _: model_state or _state())


def test_active_admitted_provider_and_model_pass(monkeypatch):
    _patch(monkeypatch)
    assert closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["accepted"]


def test_provider_admitted_not_active_rejects(monkeypatch):
    _patch(monkeypatch, provider_state=_state(lifecycle="admitted"))
    assert "provider_lifecycle_not_active" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_provider_active_pending_rejects(monkeypatch):
    _patch(monkeypatch, provider_state=_state(admission="pending"))
    assert "provider_not_admitted" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_model_candidate_pending_rejects(monkeypatch):
    _patch(monkeypatch, model_state=_state(lifecycle="candidate", admission="pending"))
    result = closure.evaluate_model_provider_routing_lifecycle_closure(_provider())
    assert {"model_lifecycle_not_active", "model_not_admitted"}.issubset(result["reasons"])


def test_model_admitted_not_active_rejects(monkeypatch):
    _patch(monkeypatch, model_state=_state(lifecycle="admitted"))
    assert "model_lifecycle_not_active" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_model_active_pending_rejects(monkeypatch):
    _patch(monkeypatch, model_state=_state(admission="pending"))
    assert "model_not_admitted" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_unknown_provider_read_rejects(monkeypatch):
    _patch(monkeypatch, provider_state=_state(status="UNKNOWN"))
    assert "provider_current_state_unknown" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_unknown_model_read_rejects(monkeypatch):
    _patch(monkeypatch, model_state=_state(status="UNKNOWN"))
    assert "model_current_state_unknown" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_provider_revision_mismatch_rejects(monkeypatch):
    _patch(monkeypatch, provider_state={**_state(), "source_revision": None})
    assert "provider_current_state_unknown" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_model_revision_mismatch_rejects(monkeypatch):
    _patch(monkeypatch, model_state={**_state(), "currentness_basis": None})
    assert "model_current_state_unknown" in closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["reasons"]


def test_missing_provider_identity_rejects_before_reads(monkeypatch):
    monkeypatch.setattr(closure, "read_provider_current_state", lambda _: (_ for _ in ()).throw(AssertionError("must not read")))
    assert closure.evaluate_model_provider_routing_lifecycle_closure({"model_id": "model:test"})["reasons"] == ("missing_provider_identity",)


def test_missing_model_reference_rejects(monkeypatch):
    _patch(monkeypatch)
    result = closure.evaluate_model_provider_routing_lifecycle_closure({"provider_id": "provider:test"})
    assert "model_reference_missing" in result["reasons"]


def test_model_families_metadata_cannot_rescue_model(monkeypatch):
    _patch(monkeypatch, model_state=_state(lifecycle="candidate", admission="pending"))
    assert not closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["accepted"]


def test_capability_status_cannot_rescue_provider_or_model(monkeypatch):
    _patch(monkeypatch, provider_state=_state(status="UNKNOWN"))
    assert not closure.evaluate_model_provider_routing_lifecycle_closure(_provider())["accepted"]


def test_ocr_real_declarations_close():
    ocr = next(item for item in loader.load_provider_registry()["providers"] if item.get("model_id") == "ocr_v1")
    assert closure.evaluate_model_provider_routing_lifecycle_closure(ocr)["accepted"]


def test_internvl_is_excluded():
    provider = next(item for item in loader.load_provider_registry()["providers"] if item.get("model_id") == "internvl2_5")
    assert provider not in closure.filter_model_provider_routing_lifecycle_eligible([provider])


def test_gemini_is_excluded():
    provider = next(item for item in loader.load_provider_registry()["providers"] if item.get("model_id") == "gemini_vision")
    assert provider not in closure.filter_model_provider_routing_lifecycle_eligible([provider])


def test_yolo_rejects_model_provider_closure():
    provider = next(item for item in loader.load_provider_registry()["providers"] if item.get("model_id") == "yolo11n")
    assert not closure.evaluate_model_provider_routing_lifecycle_closure(provider)["accepted"]


def test_controlled_evaluation_is_not_changed():
    assert loader.is_provider_routing_eligible({"provider_id": "provider:test", "lifecycle_state": "active", "admission_status": "admitted"})


def test_result_has_no_broad_authority_fields(monkeypatch):
    _patch(monkeypatch)
    result = closure.evaluate_model_provider_routing_lifecycle_closure(_provider())
    assert not {"production_ready", "globally_eligible", "runtime_authorized"}.intersection(result)


def test_filter_uses_shared_model_provider_closure(monkeypatch):
    _patch(monkeypatch)
    assert closure.filter_model_provider_routing_lifecycle_eligible([_provider()]) == [_provider()]


def test_owner_reads_and_closure_import_without_cycle():
    from capabilities.midplatform.model_manager.lifecycle import model_current_state_read_v1
    from capabilities.midplatform.model_manager.registry import provider_current_state_read_v1
    from capabilities.midplatform.model_manager.registry import provider_registry_loader_v1

    assert model_current_state_read_v1.read_model_current_state
    assert provider_current_state_read_v1.read_provider_current_state
    assert provider_registry_loader_v1.load_provider_registry
