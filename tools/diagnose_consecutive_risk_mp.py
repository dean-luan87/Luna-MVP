#!/usr/bin/env python3
"""Same minimal diagnostic, parallel over files. GLOBAL MAX consecutive >= 0.55."""
import json
from pathlib import Path
from multiprocessing import Pool

suite_path = Path("outputs/d1_runs/phase4_seed_sweep/lam_0.40/seed_42")

def one_file(p):
    path = Path(p)
    m = 0
    cur = 0
    with open(path) as f:
        for line in f:
            r = json.loads(line).get("risk_used_for_decision", 0)
            if r >= 0.55:
                cur += 1
                m = max(m, cur)
            else:
                cur = 0
    return m

def main():
    files = [str(p) for p in suite_path.rglob("replay_output.jsonl")]
    with Pool() as pool:
        per_file_max = pool.map(one_file, files, chunksize=200)
    global_max = max(per_file_max) if per_file_max else 0
    print("GLOBAL MAX consecutive >=0.55:", global_max)

if __name__ == "__main__":
    main()
