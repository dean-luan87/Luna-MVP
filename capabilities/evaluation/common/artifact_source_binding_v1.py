"""Fail-closed source and artifact provenance binding for current evidence."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping


TRUSTED_CURRENT_EVIDENCE = "TRUSTED_CURRENT_EVIDENCE"
UNBOUND_LEGACY_EVIDENCE = "UNBOUND_LEGACY_EVIDENCE"
REVERIFY_REQUIRED = "REVERIFY_REQUIRED"
BINDING_INVALID = "BINDING_INVALID"
BINDING_INCOMPLETE = "BINDING_INCOMPLETE"
WORKTREE_DIRTY = "WORKTREE_DIRTY"
SOURCE_MISMATCH = "SOURCE_MISMATCH"
ARTIFACT_MISMATCH = "ARTIFACT_MISMATCH"
ARTIFACT_DIGEST_UNAVAILABLE = "ARTIFACT_DIGEST_UNAVAILABLE"

_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_CANONICAL_BINDING_AUTHORITY = object()


class BindingVerificationResult(dict[str, Any]):
    """Result issued only by this module's canonical binding authority."""

    def __init__(
        self,
        *,
        trusted: bool,
        status: str,
        checks: Mapping[str, bool],
        errors: tuple[str, ...],
        actual_git_commit_sha: str | None,
        tracked_worktree_clean: bool | None,
        baseline_source_manifest_hash: str | None,
        authority: object,
    ) -> None:
        super().__init__(
            trusted=trusted,
            status=status,
            checks=dict(checks),
            errors=list(errors),
            actual_git_commit_sha=actual_git_commit_sha,
            tracked_worktree_clean=tracked_worktree_clean,
            baseline_source_manifest_hash=baseline_source_manifest_hash,
        )
        self._trusted = trusted
        self._status = status
        self._authority = authority

    @property
    def trusted(self) -> bool:
        return self._trusted

    @property
    def status(self) -> str:
        return self._status


def is_canonical_binding_result(value: Any) -> bool:
    return isinstance(value, BindingVerificationResult) and value._authority is _CANONICAL_BINDING_AUTHORITY


def sha256_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _repo_relative_path(repo_root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    candidate = Path(value)
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        return None
    path = repo_root / candidate
    try:
        resolved_root = repo_root.resolve()
        resolved = path.resolve(strict=False)
    except OSError:
        return None
    if resolved != resolved_root and resolved_root not in resolved.parents:
        return None
    if path.is_symlink() or not path.is_file():
        return None
    return path


def _git_head(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    head = result.stdout.strip()
    return head if re.fullmatch(r"[0-9a-f]{40,64}", head) else None


def _tracked_worktree_clean(repo_root: Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.returncode == 0 and not result.stdout.strip()


def _file_entries(binding: Mapping[str, Any]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for field in ("runner_path", "verifier_path"):
        entries.append((field, binding.get(field)))
    for field in ("fixture_paths", "contract_paths"):
        values = binding.get(field, ())
        if not isinstance(values, (list, tuple)):
            entries.append((field, None))
            continue
        for index, item in enumerate(values):
            if not isinstance(item, Mapping):
                entries.append((f"{field}[{index}]", None))
                continue
            entries.append((f"{field}[{index}]", item.get("path")))
    return entries


def verify_binding(
    binding: Mapping[str, Any],
    *,
    repo_root: Path,
    artifact_path: Path | None = None,
) -> BindingVerificationResult:
    """Verify a binding against independently observed Git/filesystem state."""
    checks: dict[str, bool] = {}
    errors: list[str] = []
    if not isinstance(binding, Mapping):
        return BindingVerificationResult(
            trusted=False,
            status=BINDING_INCOMPLETE,
            checks={},
            errors=("binding_not_mapping",),
            actual_git_commit_sha=None,
            tracked_worktree_clean=None,
            baseline_source_manifest_hash=None,
            authority=_CANONICAL_BINDING_AUTHORITY,
        )

    schema_ok = binding.get("schema_version") == "v1"
    checks["schema_version"] = schema_ok
    if not schema_ok:
        errors.append("schema_version_invalid")

    claimed_commit = binding.get("git_commit_sha")
    actual_commit = _git_head(repo_root)
    commit_ok = bool(claimed_commit and actual_commit and claimed_commit == actual_commit)
    checks["git_commit_matches_head"] = commit_ok
    if not actual_commit:
        errors.append("git_head_unavailable")
    elif not commit_ok:
        errors.append("git_commit_mismatch")

    claimed_worktree = binding.get("worktree_state")
    clean = _tracked_worktree_clean(repo_root)
    if claimed_worktree == "CLEAN" and clean is True:
        checks["worktree_state"] = True
    else:
        checks["worktree_state"] = False
        errors.append("worktree_not_clean_or_unavailable")

    entries = _file_entries(binding)
    paths: set[str] = set()
    files_ok = True
    for label, raw_path in entries:
        if not isinstance(raw_path, str) or raw_path in paths:
            files_ok = False
            errors.append(f"duplicate_or_invalid_path:{label}")
            continue
        paths.add(raw_path)
        path = _repo_relative_path(repo_root, raw_path)
        if path is None:
            files_ok = False
            errors.append(f"file_unavailable:{raw_path}")
            continue
        expected_digest = None
        if label == "runner_path":
            expected_digest = binding.get("runner_sha256")
        elif label == "verifier_path":
            expected_digest = binding.get("verifier_sha256")
        else:
            field, index_text = label.split("[", 1)
            index = int(index_text[:-1])
            item = binding[field][index]
            expected_digest = item.get("sha256") if isinstance(item, Mapping) else None
        digest_ok = isinstance(expected_digest, str) and _DIGEST_RE.fullmatch(expected_digest) and sha256_file(path) == expected_digest
        checks[f"digest:{raw_path}"] = bool(digest_ok)
        if not digest_ok:
            files_ok = False
            errors.append(f"source_digest_mismatch:{raw_path}")

    artifact_ok = True
    expected_artifact = binding.get("runner_artifact_sha256")
    if artifact_path is None:
        artifact_ok = False
        errors.append(ARTIFACT_DIGEST_UNAVAILABLE)
    elif not artifact_path.is_file() or artifact_path.is_symlink():
        artifact_ok = False
        errors.append("artifact_unavailable")
    elif not isinstance(expected_artifact, str) or not _DIGEST_RE.fullmatch(expected_artifact):
        artifact_ok = False
        errors.append("artifact_digest_missing")
    elif sha256_file(artifact_path) != expected_artifact:
        artifact_ok = False
        errors.append("artifact_digest_mismatch")
    checks["artifact_digest"] = artifact_ok

    required_scalars = (
        "input_manifest_sha256",
        "verification_timestamp",
        "verification_status",
        "proof_scope",
        "proof_tier",
    )
    scalars_ok = all(bool(binding.get(key)) for key in required_scalars)
    checks["required_authority_fields"] = scalars_ok
    if not scalars_ok:
        errors.append("required_authority_fields_missing")

    trusted = all(checks.values())
    status = TRUSTED_CURRENT_EVIDENCE if trusted else BINDING_INCOMPLETE
    if any("git_commit_mismatch" in error for error in errors):
        status = SOURCE_MISMATCH
    elif any("artifact_digest_mismatch" in error for error in errors):
        status = ARTIFACT_MISMATCH
    elif clean is False:
        status = WORKTREE_DIRTY
    elif binding.get("provenance_status") == UNBOUND_LEGACY_EVIDENCE:
        status = REVERIFY_REQUIRED
    return BindingVerificationResult(
        trusted=trusted,
        status=status,
        checks=dict(checks),
        errors=tuple(errors),
        actual_git_commit_sha=actual_commit,
        tracked_worktree_clean=clean,
        baseline_source_manifest_hash=binding.get("baseline_source_manifest_hash"),
        authority=_CANONICAL_BINDING_AUTHORITY,
    )


__all__ = [
    "ARTIFACT_DIGEST_UNAVAILABLE",
    "ARTIFACT_MISMATCH",
    "BINDING_INCOMPLETE",
    "BindingVerificationResult",
    "BINDING_INVALID",
    "REVERIFY_REQUIRED",
    "SOURCE_MISMATCH",
    "TRUSTED_CURRENT_EVIDENCE",
    "UNBOUND_LEGACY_EVIDENCE",
    "WORKTREE_DIRTY",
    "sha256_bytes",
    "sha256_file",
    "is_canonical_binding_result",
    "verify_binding",
]
