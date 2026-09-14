#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3: 人类标注 CLI — 读 annotation_tasks，人类输入答案，追加写 annotations/。
不改 runtime/、不写回 library_store/、不生成“正确答案”、不引入模型推理。
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HELP_TEXT = """\
可用指令（在 answer 提示处输入）：
  :skip   跳过本题（不写入）
  :quit   退出（已写入的答案不会丢）
  :help   显示本帮助
"""


def load_tasks(tasks_path: str) -> list:
    out = []
    if not os.path.isfile(tasks_path):
        return out
    with open(tasks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def load_answered_task_ids(answers_path: str) -> set:
    out = set()
    if not os.path.isfile(answers_path):
        return out
    with open(answers_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            tid = row.get("task_id")
            if tid:
                out.add(tid)
    return out


def append_answer(answers_path: str, row: dict) -> None:
    os.makedirs(os.path.dirname(answers_path), exist_ok=True)
    with open(answers_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def _safe_str(x) -> str:
    if x is None:
        return ""
    return str(x)


def _extract_trigger_type(task: dict) -> str:
    # 优先字段，其次从 context 中抽取 trigger_type=XXX
    tt = task.get("trigger_type")
    if tt:
        return _safe_str(tt)
    ctx = _safe_str(task.get("context"))
    needle = "trigger_type="
    if needle in ctx:
        after = ctx.split(needle, 1)[1].strip()
        # 到空格/逗号/; 之前
        for sep in [" ", ",", ";", "]"]:
            if sep in after:
                after = after.split(sep, 1)[0]
        return after
    return ""


def _sort_key(task: dict):
    return (
        _safe_str(task.get("session_id")),
        _safe_str(task.get("episode_id")),
        _safe_str(task.get("task_id")),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Phase 3.3: Human Annotation CLI (read outputs/, write annotations/)."
    )
    parser.add_argument("--version-tag", default="v1.1", help="Version tag (default: v1.1)")
    parser.add_argument(
        "--tasks-path",
        default=None,
        help="annotation_tasks.jsonl 路径；默认 outputs/<version>/annotation_tasks.jsonl",
    )
    parser.add_argument(
        "--answers-path",
        default=None,
        help="answers.jsonl 路径；默认 annotations/<version>/answers.jsonl",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="仅打印进度统计，不进入交互",
    )
    args = parser.parse_args()

    version = args.version_tag
    tasks_path = args.tasks_path or str(ROOT / "outputs" / version / "annotation_tasks.jsonl")
    answers_path = args.answers_path or str(ROOT / "annotations" / version / "answers.jsonl")

    if not os.path.isfile(tasks_path):
        print(f"未找到任务文件: {tasks_path}", file=sys.stderr)
        sys.exit(1)

    tasks = load_tasks(tasks_path)
    answered = load_answered_task_ids(answers_path)
    tasks_sorted = sorted(tasks, key=_sort_key)
    pending = [t for t in tasks_sorted if t.get("task_id") not in answered]

    total = len(tasks_sorted)
    done = len(answered)
    todo = len(pending)
    print(f"version_tag:  {version}")
    print(f"tasks_path:   {tasks_path}")
    print(f"answers_path: {answers_path}")
    print(f"进度: total={total} answered={done} pending={todo}")
    if args.stats_only:
        return

    if not pending:
        print("没有待标注任务，已全部完成。")
        return

    print("\n进入标注模式：每答完一题会立即追加写入 answers.jsonl，可随时中断再恢复。\n")
    for i, task in enumerate(pending, 1):
        task_id = task.get("task_id") or ""
        episode_id = task.get("episode_id") or ""
        question = task.get("question") or ""
        context = task.get("context") or ""
        trigger_type = _extract_trigger_type(task)
        options = task.get("options")

        print(f"--- [{i}/{len(pending)}] task_id: {task_id} ---")
        print(f"  episode_id:   {episode_id}")
        if trigger_type:
            print(f"  trigger_type: {trigger_type}")
        print(f"  context:      {context}")
        print(f"  question:     {question}")
        if options is not None:
            print(f"  options:      {options}")

        try:
            raw = input("  answer（必填，或输入 :help）: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已中断，已答题目已保存。")
            break

        if not raw:
            print("  跳过（未输入）\n")
            continue
        if raw == ":help":
            print(HELP_TEXT)
            # 重新问一次
            try:
                raw = input("  answer（必填，或输入 :skip/:quit）: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n已中断，已答题目已保存。")
                break
        if raw == ":skip":
            print("  已跳过。\n")
            continue
        if raw == ":quit":
            print("  已退出。\n")
            break

        try:
            conf_raw = input("  confidence (可选，回车=1.0): ").strip()
        except (EOFError, KeyboardInterrupt):
            conf_raw = ""

        confidence = 1.0
        if conf_raw:
            try:
                confidence = float(conf_raw)
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                confidence = 1.0

        row = {
            "version_tag": task.get("version_tag") or version,
            "session_id": task.get("session_id") or "",
            "episode_id": episode_id,
            "task_id": task_id,
            "answer": raw,
            "confidence": confidence,
            "annotator": "human",
            "annotated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        append_answer(answers_path, row)
        print("  已写入。\n")

    print(f"答案写入: {answers_path}")


if __name__ == "__main__":
    main()

