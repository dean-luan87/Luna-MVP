from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = find_repo_root(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_external_provisioning.yolo11n_external_provisioning_fixture_v1 import (  # noqa: E402
    build_yolo11n_external_provisioning_cases_v1,
    evaluate_yolo11n_external_provisioning_case_v1,
)
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_external_provisioning.yolo11n_external_provisioning_types_v1 import (  # noqa: E402
    resolve_yolo11n_external_provisioning_v1,
    to_dict,
)


OUT = ROOT / "_eval_out/s3_yolo11n_external_asset_provisioning_and_admission_verification_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def _external_candidate(args: argparse.Namespace) -> dict[str, Any] | None:
    if not args.source_file:
        return None
    candidate: dict[str, Any] = {
        "target_model_asset_id": "model-asset:yolo11n:weights-v1",
        "source_file_ref": args.source_file,
        "observed_path": args.source_file,
        "provenance_ref": args.provenance_ref,
        "dependency_status": args.dependency_status,
    }
    if args.declared_checksum:
        candidate["declared_checksum"] = args.declared_checksum
    if args.observed_checksum:
        candidate["observed_checksum"] = args.observed_checksum
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="Controlled YOLO11n external asset readiness; no model loading.")
    parser.add_argument("--source-file")
    parser.add_argument("--declared-checksum")
    parser.add_argument("--observed-checksum")
    parser.add_argument("--dependency-status", default="PYTHON_DEPENDENCY_UNRESOLVED")
    parser.add_argument("--provenance-ref", default="provenance:user-terminal-external-asset")
    args = parser.parse_args()
    external = _external_candidate(args)
    case_results = [evaluate_yolo11n_external_provisioning_case_v1(case) for case in build_yolo11n_external_provisioning_cases_v1()]
    current = case_results[0]["admission"] if case_results else {}
    external_result = None
    mode = "SYNTHETIC_REGRESSION"
    if external is not None:
        external_result = to_dict(resolve_yolo11n_external_provisioning_v1(external))
        current = external_result
        mode = "EXTERNAL_PROVISIONING_READINESS"
    results = [jsonable(item) for item in case_results]
    failed = [item["scenario_id"] for item in results if not item["passed"]]
    physical = current.get("physical", {}) if mode.startswith("EXTERNAL") else current.get("physical", {})
    provisioning = current.get("provisioning", {}) if mode.startswith("EXTERNAL") else current.get("provisioning", {})
    summary = {
        "mode": mode,
        "owner": "Model Manager / Model Governance",
        "target_model": "YOLO11n",
        "target_asset_id": current.get("target_asset_id"),
        "expected_governed_path": current.get("expected_governed_path"),
        "scenario_count": len(results),
        "all_cases_passed": not failed if results else None,
        "failed_case_ids": failed,
        "provisioning_status": provisioning.get("provisioning_status"),
        "physical_asset_status": physical.get("physical_asset_status"),
        "identity_status": current.get("model_identity_status"),
        "checksum_status": current.get("checksum_status"),
        "dependency_status": current.get("dependency_status"),
        "contract_statuses": {
            "model": current.get("model_contract_status"),
            "loader": current.get("loader_contract_status"),
            "provider_adapter": current.get("provider_adapter_status"),
            "capability": current.get("capability_contract_status"),
            "evidence": current.get("evidence_contract_status"),
        },
        "technical_admission_status": current.get("technical_admission_status"),
        "commercial_license_status": current.get("commercial_license_status"),
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "automatic_dependency_install": False,
        "synthetic_regression_preserved": True,
        "external_readiness": jsonable(external_result) if external_result is not None else None,
    }
    trace = {
        "reverse_trace": ["technical_admission", "dependency_probe_result", "checksum", "physical_asset", "provisioning_record", "model_asset_contract"],
        "provenance_grants_authority": False,
        "copy_executed": False,
        "model_load_executed": False,
        "current_trace_ref": current.get("trace_ref"),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s3_yolo11n_external_asset_provisioning_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolo11n_external_asset_provisioning_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolo11n_external_asset_provisioning_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
