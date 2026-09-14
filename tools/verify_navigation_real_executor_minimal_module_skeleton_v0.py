# -*- coding: utf-8 -*-
"""
Local verification for Navigation Real Executor Minimal Module Skeleton v0.

Goals:
- A: module importable, identity fixed
- B: accept_executor_input returns placeholder/not_implemented and does NOT execute actions
- C: emit_executor_status returns placeholder/inactive (NOT running/completed/failed)
- D: raise_executor_exception returns standardized placeholder object and preserves semantics

Usage (repo root):
  PYTHONPATH=. python3 tools/verify_navigation_real_executor_minimal_module_skeleton_v0.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap_repo_root() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def main() -> int:
    _bootstrap_repo_root()

    from capabilities.navigation.runtime import navigation_real_executor_v0 as ex  # noqa: E402

    def assert_true(v: bool, msg: str) -> None:
        if not v:
            raise AssertionError(msg)

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    ok_all = True

    # A) import + identity fixed
    ident = ex.get_executor_identity()
    print("=== A import + identity ===")
    print("  identity:", ident)
    a_ok = (
        isinstance(ident, dict)
        and ident.get("executor_identity") == ex.EXECUTOR_IDENTITY_V0
        and ident.get("is_skeleton") is True
        and ident.get("can_execute_real_actions") is False
    )
    print("  预期: identity 固定 + is_skeleton →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    # B) accept input returns placeholder/not_implemented
    print("=== B accept_executor_input ===")
    res_b = ex.accept_executor_input(navigation_real_executor_input_v0={"executor_input_scope": "anything"})
    print("  result:", res_b)
    b_ok = (
        isinstance(res_b, dict)
        and res_b.get("result_scope") == ex.EXECUTOR_INPUT_SCOPE_V0
        and res_b.get("status") == "not_implemented"
        and isinstance(res_b.get("payload"), dict)
        and res_b["payload"].get("execute_attempted") is False
    )
    print("  预期: not_implemented + no execute →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    # C) emit status returns placeholder/inactive
    print("=== C emit_executor_status ===")
    st = ex.emit_executor_status()
    print("  status:", st)
    c_ok = (
        isinstance(st, dict)
        and st.get("executor_status_scope") == ex.EXECUTOR_STATUS_SCOPE_V0
        and st.get("takeover_state") == "inactive_skeleton_placeholder"
        and st.get("execution_state") == "not_started_placeholder"
        and st.get("consume_mode") == "skeleton_placeholder"
    )
    # No fabrication rule: ensure not pretending to be running/completed/failed.
    forbidden = {"execution_running", "execution_completed", "execution_failed", "execution_interrupted", "active"}
    c_ok = c_ok and str(st.get("execution_state") or "") not in forbidden
    print("  预期: placeholder/inactive →", "OK" if c_ok else "FAIL")
    ok_all = ok_all and c_ok

    # D) exception placeholder preserves semantics
    print("=== D raise_executor_exception ===")
    res_d = ex.raise_executor_exception(exc=ValueError("x"), context={"k": "v"})
    print("  exception:", res_d)
    d_ok = (
        isinstance(res_d, dict)
        and res_d.get("executor_exception_scope") == ex.EXECUTOR_EXCEPTION_SCOPE_V0
        and res_d.get("exception_status") == "reported_placeholder"
        and res_d.get("exception_type") == "ValueError"
        and res_d.get("exception_message") == "x"
        and isinstance(res_d.get("context"), dict)
        and res_d["context"].get("k") == "v"
    )
    print("  预期: 标准占位异常对象 + 不吞语义 →", "OK" if d_ok else "FAIL")
    ok_all = ok_all and d_ok

    print("")
    if ok_all:
        print("VERIFY_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0: ALL_OK")
        return 0
    print("VERIFY_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0: FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

