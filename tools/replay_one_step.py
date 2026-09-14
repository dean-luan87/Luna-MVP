#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补丁 v1 最小自测：输入 obs.json，输出 engagement 状态（可选 rhythm）。
不依赖摄像头、不读日志行数、不读 self.last_ts 之外的外部时间。
用法: python3 tools/replay_one_step.py [obs.json]
"""
import json
import sys
from pathlib import Path

# 项目根
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from runtime.observation_builders import build_observation_frame
from intervention.engagement_v0 import get_engagement_v0
from intervention.rhythm_v0 import get_rhythm_v0


def load_obs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def obs_dict_to_frame(d: dict):
    # 支持扁平格式或 logger 输出的嵌套格式（含 "obs"）
    o = d.get("obs", d)
    return build_observation_frame(
        ts=float(d.get("ts", 0)),
        dt=float(d.get("dt", 0)),
        seq=int(d.get("seq", 0)),
        sampled=bool(d.get("sampled", True)),
        motion=float(o.get("motion", 0)),
        path=float(o.get("path", 0)),
        branch=float(o.get("branch", 0)),
        roi=int(o.get("roi", 0)),
        pal=float(o.get("pal", 0)),
        complexity=float(o.get("complexity", 0)),
        vc=float(o.get("vc", 0)),
        frame_quality=str(o.get("frame_quality", "GOOD")),
        control_mode=str(o.get("control_mode", "NONE")),
    )


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else _ROOT / "artifacts" / "obs_sample.json"
    if not path.exists():
        # 写一份样例 obs 供测试
        sample = {
            "ts": 3.0,
            "dt": 1.0,
            "seq": 1,
            "sampled": True,
            "motion": 0.2,
            "path": 0.2,
            "branch": 0.1,
            "roi": 2,
            "pal": 0.25,
            "complexity": 0.55,
            "vc": 0.7,
            "frame_quality": "GOOD",
            "control_mode": "GUARDED",
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample, f, indent=2, ensure_ascii=False)
        print(f"已创建样例 {path}，请再次运行以回放")

    obs_d = load_obs(path)
    obs = obs_dict_to_frame(obs_d)

    # 仅用 obs 与默认 eligibility 推 rhythm（不依赖外部时间）
    task_state = "ACTIVE"
    eligible = True
    rhythm_state = get_rhythm_v0().tick(
        now=obs.ts,
        pal=obs.pal,
        eligible=eligible,
        vc=obs.vc,
        task_state=task_state,
    )
    eng = get_engagement_v0().on_observation(obs, rhythm_state=rhythm_state)

    print("engagement:", eng.level, "advice_scale=", eng.advice_scale, "pal_lookahead_m=", eng.pal_lookahead_m, "speak_cooldown_s=", eng.speak_cooldown_s)
    print("rhythm_state:", rhythm_state)
    print("obs.ts / dt / seq / sampled:", obs.ts, obs.dt, obs.seq, obs.sampled)


if __name__ == "__main__":
    main()
