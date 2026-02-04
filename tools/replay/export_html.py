import json
import argparse
from pathlib import Path


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Timeline Replay</title>
<style>
body {{
  font-family: monospace;
  background: #0f0f0f;
  color: #e0e0e0;
  margin: 0;
}}
header {{
  position: sticky;
  top: 0;
  background: #111;
  border-bottom: 1px solid #333;
  padding: 10px;
  z-index: 10;
}}
input, label {{
  font-family: monospace;
  font-size: 14px;
}}
.controls {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}}
.controls > div {{
  display: flex;
  gap: 6px;
  align-items: center;
}}
.frame {{
  border-bottom: 1px solid #333;
  padding: 10px;
}}
.ts {{
  color: #6cf;
}}
.section {{
  margin-top: 6px;
}}
.key {{
  color: #9cdcfe;
}}
pre {{
  background: #1e1e1e;
  padding: 6px;
  overflow-x: auto;
}}
.small {{
  color: #aaa;
  font-size: 12px;
}}
.hidden {{
  display: none;
}}
</style>
</head>
<body>

<header>
  <div class="controls">
    <div>
      <label>Entity contains:</label>
      <input id="entityFilter" placeholder="e.g. traffic_light or elevator_1" size="28"/>
    </div>
    <div>
      <label>Task contains:</label>
      <input id="taskFilter" placeholder="e.g. TrafficLightTask" size="24"/>
    </div>
    <div>
      <label><input type="checkbox" id="onlyChanged" checked/> Only changed frames</label>
    </div>
    <div>
      <span class="small" id="countLabel"></span>
    </div>
  </div>
</header>

<div id="frames">
{frames}
</div>

<script>
function applyFilters() {{
  const ef = document.getElementById("entityFilter").value.trim();
  const tf = document.getElementById("taskFilter").value.trim();
  const onlyChanged = document.getElementById("onlyChanged").checked;

  const frames = document.querySelectorAll(".frame");
  let shown = 0;
  frames.forEach(fr => {{
    const entities = fr.getAttribute("data-entities") || "";
    const tasks = fr.getAttribute("data-tasks") || "";
    const changed = fr.getAttribute("data-changed") === "1";

    let ok = true;

    if (ef.length > 0 && !entities.includes(ef)) ok = false;
    if (tf.length > 0 && !tasks.includes(tf)) ok = false;
    if (onlyChanged && !changed) ok = false;

    fr.classList.toggle("hidden", !ok);
    if (ok) shown++;
  }});

  document.getElementById("countLabel").textContent =
    `shown ${{shown}} / ${{frames.length}}`;
}}

["entityFilter", "taskFilter", "onlyChanged"].forEach(id => {{
  document.getElementById(id).addEventListener("input", applyFilters);
  document.getElementById(id).addEventListener("change", applyFilters);
}});

applyFilters();
</script>

</body>
</html>
"""


def diff(prev: dict, curr: dict) -> dict:
    if prev is None:
        return curr
    out = {}
    keys = set(prev.keys()) | set(curr.keys())
    for k in keys:
        if prev.get(k) != curr.get(k):
            out[k] = {"from": prev.get(k), "to": curr.get(k)}
    return out


def render_block(title: str, data) -> str:
    return f"""
    <div class="section">
      <div class="key">{title}</div>
      <pre>{json.dumps(data, ensure_ascii=False, indent=2)}</pre>
    </div>
    """


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("timeline", help="timeline jsonl file")
    parser.add_argument("--out", default="timeline.html")
    args = parser.parse_args()

    frames_html = []
    prev = None

    with open(args.timeline, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            frame = json.loads(line)

            if prev is None:
                d_entities = frame["entities"]
                d_tasks = frame["tasks"]
                d_c = frame["c_decision"]
            else:
                d_entities = diff(prev["entities"], frame["entities"])
                d_tasks = diff(
                    {t["task"]: t for t in prev["tasks"]},
                    {t["task"]: t for t in frame["tasks"]},
                )
                d_c = diff(prev["c_decision"], frame["c_decision"])

            changed = 1 if (len(d_entities) or len(d_tasks) or len(d_c)) else 0

            # 用于浏览器过滤：把 entity_id / task_name 拼成字符串
            entities_str = " ".join(sorted(frame["entities"].keys()))
            tasks_str = " ".join(sorted([t.get("task", "") for t in frame["tasks"]]))

            frames_html.append(f"""
            <div class="frame"
                 data-changed="{changed}"
                 data-entities="{entities_str}"
                 data-tasks="{tasks_str}">
              <div class="ts">t = {frame['ts']:.2f}</div>
              {render_block("World Δ", d_entities)}
              {render_block("Tasks Δ", d_tasks)}
              {render_block("C Decision Δ", d_c)}
            </div>
            """)

            prev = frame

    html = HTML_TEMPLATE.format(frames="".join(frames_html))
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"[OK] exported to {args.out}")


if __name__ == "__main__":
    main()
