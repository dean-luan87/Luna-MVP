# examples/b2_v03_align_validate.py
from __future__ import annotations
import json
from vision_pipeline.b2.v03.align_validator import parse_expected, find_match


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    human = load_json("human_timeline.json")
    b2 = list(load_jsonl("b2_v03_timeline.jsonl"))

    tolerance = {"L1": 6.0, "L2": 4.0, "L3": 2.5}

    used = set()
    ok = late = miss = 0

    for h in human:
        t = h["t_video"]
        lvl = h.get("level", "L2")
        expected = parse_expected(h.get("expected", ""))
        max_dt = tolerance.get(lvl, 4.0)

        m = find_match(b2, t, expected, max_dt)
        if m is None:
            miss += 1
            print(f"[MISS] {h['t_str']} {h.get('label','')}")
            continue

        idx = b2.index(m)
        used.add(idx)

        dt = m["_dt"]
        tag = "OK" if dt <= max_dt * 0.5 else "LATE"
        if tag == "OK":
            ok += 1
        else:
            late += 1

        print(f"[{tag}] {h['t_str']} → B2 {m['t_str']} {m['decision']} Δ={dt:.2f}s")

    fp = 0
    for i, e in enumerate(b2):
        if i in used:
            continue
        if e.get("decision") and e["decision"] != "NO_CHANGE":
            fp += 1
            print(f"[FP] B2 {e['t_str']} {e['decision']}")

    print(f"OK={ok} LATE={late} MISS={miss} FP={fp}")


if __name__ == "__main__":
    main()

