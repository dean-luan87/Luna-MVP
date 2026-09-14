#!/usr/bin/env bash
# 在仓库根目录执行。把新导出的窗口 JSONL 放进 analyze_unified_env_shadow_out/windows/ 后，
# 把下面示例里的文件名换成你的即可。
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${REPO_ROOT}/analyze_unified_env_shadow_out"
WINDOWS="${OUT_DIR}/windows"
PY="${REPO_ROOT}/tools/analyze_unified_env_min_wiring_v1.py"

usage() {
  echo "用法（在仓库根目录 Luna-Workspace-Min 下）："
  echo "  ./tools/analyze_unified_env_window.sh <你的窗口.jsonl>"
  echo ""
  echo "推荐：把导出文件保存到固定目录后再分析，例如："
  echo "  ${WINDOWS}/window_round02.jsonl"
  echo "  ./tools/analyze_unified_env_window.sh analyze_unified_env_shadow_out/windows/window_round02.jsonl"
  exit 1
}

[[ $# -ge 1 ]] || usage

JSONL="$1"
if [[ "${JSONL}" != /* ]]; then
  JSONL="${REPO_ROOT}/${JSONL}"
fi

if [[ ! -f "${JSONL}" ]]; then
  echo "错误：找不到文件: ${JSONL}" >&2
  echo "请确认路径；新文件请先保存到 ${WINDOWS}/ 再写相对路径。" >&2
  exit 1
fi

exec python3 "${PY}" "${JSONL}" --out-dir "${OUT_DIR}"
