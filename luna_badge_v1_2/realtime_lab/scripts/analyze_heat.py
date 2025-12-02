import json
from pathlib import Path

import statistics as stats

DATA_FILE = Path("../logs/heat_10min.json")


def main():
  if not DATA_FILE.exists():
    print("no heat_10min.json, please run heat_stress_10min.py first")
    return

  data = json.loads(DATA_FILE.read_text())
  cpus = [d["cpu"] for d in data]
  temps = [d["temp"] for d in data if d["temp"] is not None]

  print("===== HEAT ANALYSIS (10min) =====")
  print("samples:", len(data))
  print("cpu avg:", stats.mean(cpus), "max:", max(cpus))
  if temps:
    print("temp avg:", stats.mean(temps), "max:", max(temps))
  else:
    print("temp: not available on this device")


if __name__ == "__main__":
  main()

