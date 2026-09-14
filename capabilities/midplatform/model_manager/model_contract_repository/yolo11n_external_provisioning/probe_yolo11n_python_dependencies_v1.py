from __future__ import annotations

import importlib
import json
from typing import Any, Dict, Optional, Tuple


DEPENDENCY_PROBE_CONTRACT_V1 = (
    ("ultralytics", "required", ">=8.0.0"),
    ("torch", "conditional", None),
    ("torchvision", "conditional", None),
    ("PIL", "required_by_provider_path", None),
    ("cv2", "required_by_provider_path", None),
)


def _version_tuple(value: Optional[str]) -> Optional[Tuple[int, ...]]:
    if not value:
        return None
    parts = []
    for token in value.split("."):
        digits = "".join(char for char in token if char.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts) if parts else None


def _check_version(observed: Optional[str], constraint: Optional[str]) -> Optional[bool]:
    if not observed or not constraint:
        return None
    if constraint.startswith(">="):
        left = _version_tuple(observed)
        right = _version_tuple(constraint[2:])
        return bool(left is not None and right is not None and left >= right)
    return None


def probe_dependency(name: str, required_or_conditional: str, constraint: Optional[str]) -> Dict[str, Any]:
    try:
        module = importlib.import_module(name)
        observed = getattr(module, "__version__", None)
        compatible = _check_version(str(observed) if observed is not None else None, constraint)
        return {
            "dependency_name": name,
            "required_or_conditional": required_or_conditional,
            "declared_constraint": constraint,
            "observed_version": str(observed) if observed is not None else None,
            "import_available": True,
            "version_compatible": compatible,
            "verification_status": "PYTHON_DEPENDENCY_VERIFIED" if compatible is not False else "PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE",
            "error_ref": None,
        }
    except ImportError as exc:
        return {
            "dependency_name": name,
            "required_or_conditional": required_or_conditional,
            "declared_constraint": constraint,
            "observed_version": None,
            "import_available": False,
            "version_compatible": False,
            "verification_status": "PYTHON_DEPENDENCY_MISSING",
            "error_ref": f"import:{type(exc).__name__}",
        }
    except Exception as exc:
        return {
            "dependency_name": name,
            "required_or_conditional": required_or_conditional,
            "declared_constraint": constraint,
            "observed_version": None,
            "import_available": None,
            "version_compatible": None,
            "verification_status": "PYTHON_DEPENDENCY_UNRESOLVED",
            "error_ref": f"probe:{type(exc).__name__}",
        }


def main() -> int:
    results = [probe_dependency(*item) for item in DEPENDENCY_PROBE_CONTRACT_V1]
    print(json.dumps({"model_load_executed": False, "network_access": False, "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
