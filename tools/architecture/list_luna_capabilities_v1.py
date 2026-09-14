from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_REGISTRY = Path("capabilities/registry/luna_capability_registry_v1.json")


def _load_registry(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _select_capabilities(
    capabilities: List[Dict[str, Any]],
    status: str | None,
    capability_id: str | None,
    ready_only: bool,
    blocked_only: bool,
) -> List[Dict[str, Any]]:
    rows = capabilities
    if status:
        rows = [c for c in rows if c.get("lifecycle_status") == status]
    if capability_id:
        rows = [c for c in rows if c.get("capability_id") == capability_id]
    if ready_only:
        rows = [
            c for c in rows if c.get("lifecycle_status") == "functional_module_ready"
        ]
    if blocked_only:
        rows = [c for c in rows if c.get("lifecycle_status") == "blocked"]
    return rows


def _print_summary(rows: List[Dict[str, Any]]) -> None:
    if not rows:
        print("No capabilities matched.")
        return
    print(f"matched_capabilities={len(rows)}")
    for row in rows:
        print(
            " | ".join(
                [
                    str(row.get("capability_id", "")),
                    str(row.get("capability_name", "")),
                    str(row.get("lifecycle_status", "")),
                    str(row.get("module_version", "")),
                ]
            )
        )


def _print_dependencies(rows: List[Dict[str, Any]]) -> None:
    if not rows:
        print("No capabilities matched.")
        return
    for row in rows:
        print(f"capability_id={row.get('capability_id')}")
        print(
            f"depends_on={json.dumps(row.get('dependencies', []), ensure_ascii=False)}"
        )
        print(f"dependents={json.dumps(row.get('dependents', []), ensure_ascii=False)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List Luna capabilities from registry (read-only)."
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to luna capability registry json",
    )
    parser.add_argument(
        "--status", type=str, default=None, help="Filter by lifecycle status"
    )
    parser.add_argument(
        "--capability-id", type=str, default=None, help="Show one capability"
    )
    parser.add_argument(
        "--show-dependencies", action="store_true", help="Show dependency info"
    )
    parser.add_argument("--ready", action="store_true", help="Show ready modules only")
    parser.add_argument(
        "--blocked", action="store_true", help="Show blocked modules only"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output full json for selected rows"
    )
    args = parser.parse_args()

    data = _load_registry(args.registry)
    capabilities = data.get("capabilities", [])
    selected = _select_capabilities(
        capabilities=capabilities,
        status=args.status,
        capability_id=args.capability_id,
        ready_only=args.ready,
        blocked_only=args.blocked,
    )

    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0

    if args.show_dependencies:
        _print_dependencies(selected)
    else:
        _print_summary(selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
