#!/usr/bin/env bash
# 打包 Cursor agent-transcripts，便于清理左侧超长对话历史。
# 用法:
#   ./scripts/archive_cursor_agent_transcripts.sh                    # 仅打包
#   ./scripts/archive_cursor_agent_transcripts.sh --delete-after-zip # 打包后删除源目录
#   KEEP_UUID=7973a276-6d64-41d2-95b5-90bbe1ffdab7 ./scripts/...   # 保留指定会话

set -euo pipefail

WORKSPACE_LABEL="${WORKSPACE_LABEL:-Users-luanlei-Desktop-Luna-Workspace-Min}"
CURSOR_PROJECTS="${CURSOR_PROJECTS:-$HOME/.cursor/projects}"
SRC="${SRC:-$CURSOR_PROJECTS/$WORKSPACE_LABEL/agent-transcripts}"
ARCHIVE_ROOT="${ARCHIVE_ROOT:-$HOME/Desktop/Luna-Core/_archive/cursor_agent_transcripts}"
KEEP_UUID="${KEEP_UUID:-}"
DELETE_AFTER=0

for arg in "$@"; do
  case "$arg" in
    --delete-after-zip) DELETE_AFTER=1 ;;
    --help|-h)
      echo "Usage: KEEP_UUID=<uuid> $0 [--delete-after-zip]"
      exit 0
      ;;
  esac
done

if [[ ! -d "$SRC" ]]; then
  echo "源目录不存在: $SRC" >&2
  exit 1
fi

STAMP=$(date +%Y%m%d_%H%M%S)
OUT_DIR="$ARCHIVE_ROOT/$WORKSPACE_LABEL/$STAMP"
mkdir -p "$OUT_DIR"

MANIFEST="$OUT_DIR/manifest.json"
echo '{"archived_at":"'"$STAMP"'","source":"'"$SRC"'","sessions":[' > "$MANIFEST"

first=1
total_bytes=0
archived_count=0

for dir in "$SRC"/*; do
  [[ -d "$dir" ]] || continue
  uuid=$(basename "$dir")
  if [[ -n "$KEEP_UUID" && "$uuid" == *"$KEEP_UUID"* ]]; then
    echo "保留: $uuid"
    continue
  fi
  size=$(du -sk "$dir" | awk '{print $1}')
  total_bytes=$((total_bytes + size * 1024))
  zip_path="$OUT_DIR/${uuid}.zip"
  (cd "$SRC" && zip -rq "$zip_path" "$uuid")
  snippet=""
  jsonl="$dir/${uuid}.jsonl"
  if [[ -f "$jsonl" ]]; then
    snippet=$(python3 -c "
import json,sys
p=sys.argv[1]
for line in open(p,encoding='utf-8'):
    o=json.loads(line)
    if o.get('role')=='user':
        t=o.get('message',{}).get('content',[])
        if t and isinstance(t[0],dict): print((t[0].get('text') or '')[:120].replace(chr(10),' '))
        break
" "$jsonl" 2>/dev/null || true)
  fi
  [[ $first -eq 1 ]] || echo ',' >> "$MANIFEST"
  first=0
  printf '{"uuid":"%s","size_kb":%s,"zip":"%s","snippet":"%s"}' \
    "$uuid" "$size" "$(basename "$zip_path")" "$(echo "$snippet" | sed 's/"/\\"/g')" >> "$MANIFEST"
  archived_count=$((archived_count + 1))
  if [[ "$DELETE_AFTER" -eq 1 ]]; then
    rm -rf "$dir"
  fi
done

echo ']}' >> "$MANIFEST"

echo "已打包 $archived_count 个会话 → $OUT_DIR"
echo "合计约 $(( total_bytes / 1024 / 1024 )) MB"
echo "清单: $MANIFEST"
if [[ -n "$KEEP_UUID" ]]; then
  echo "已保留 UUID 含: $KEEP_UUID"
fi
if [[ "$DELETE_AFTER" -eq 1 ]]; then
  echo "已删除源 transcript 目录（保留项除外）"
else
  echo "未删除源文件。确认无误后执行: $0 --delete-after-zip"
fi
