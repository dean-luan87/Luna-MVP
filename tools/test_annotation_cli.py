#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-4: 最小测试（不碰 runtime）

- 构造 1 条 fake annotation_task
- 模拟输入（patch builtins.input）
- 生成 1 条 answer
- 用 guard_annotations_schema.py 校验通过
"""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import subprocess
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    with tempfile.TemporaryDirectory(prefix="anno_test_") as tmp:
        base = Path(tmp)

        # 1) fake episodes_index.jsonl
        idx_dir = base / "library_store" / "v1.1"
        idx_dir.mkdir(parents=True)
        (idx_dir / "episodes_index.jsonl").write_text(
            json.dumps(
                {
                    "version_tag": "v1.1",
                    "session_id": "s1",
                    "episode_id": "SAFETY_CHANGE_42",
                    "path": "v1.1/episodes/20260209/s1/SAFETY_CHANGE_42",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        # 2) fake annotation_tasks.jsonl
        out_dir = base / "outputs" / "v1.1"
        out_dir.mkdir(parents=True)
        task_id = "s1_SAFETY_CHANGE_42_SAFETY_0"
        (out_dir / "annotation_tasks.jsonl").write_text(
            json.dumps(
                {
                    "task_id": task_id,
                    "version_tag": "v1.1",
                    "session_id": "s1",
                    "episode_id": "SAFETY_CHANGE_42",
                    "question": "安全等级发生变化：请判断是否属于误判或真实风险？",
                    "context": "trigger_type=SAFETY_CHANGE",
                    "created_at": "2026-02-09T10:00:00Z",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        answers_path = base / "annotations" / "v1.1" / "answers.jsonl"
        answers_path.parent.mkdir(parents=True, exist_ok=True)

        # 3) run annotation_cli.main() with patched input + argv
        annotation_cli = load_module(ROOT / "tools" / "annotation_cli.py", "annotation_cli")
        argv = [
            "annotation_cli.py",
            "--version-tag",
            "v1.1",
            "--tasks-path",
            str(out_dir / "annotation_tasks.jsonl"),
            "--answers-path",
            str(answers_path),
        ]
        with patch("builtins.input", side_effect=["wet_floor", "0.8"]):
            old_argv = sys.argv
            try:
                sys.argv = argv
                annotation_cli.main()
            finally:
                sys.argv = old_argv

        if not answers_path.is_file():
            print("FAIL: answers.jsonl not written")
            return 1

        # 4) guard pass
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "guard_annotations_schema.py"),
                "--base-dir",
                str(base / "library_store"),
                "--version-tag",
                "v1.1",
                "--answers-path",
                str(answers_path),
                "--tasks-path",
                str(out_dir / "annotation_tasks.jsonl"),
            ],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            print("FAIL: guard exited", r.returncode)
            print(r.stdout)
            print(r.stderr)
            return 1
        if "PASS" not in r.stdout:
            print("FAIL: guard did not report PASS")
            print(r.stdout)
            return 1

    print("PASSED: annotation_cli + guard (fake task, patched input)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

