import json
import time
from datetime import datetime

import psutil

OUT_FILE = "../logs/heat_10min.json"


def get_temp():
  temps = psutil.sensors_temperatures()
  if not temps:
    return None
  # 尝试常见 key
  for key in ["cpu-thermal", "coretemp", "Tdie"]:
    if key in temps:
      entries = temps[key]
      if entries:
        return entries[0].current
  # 随便拿一个
  first = list(temps.values())[0]
  if first:
    return first[0].current
  return None


def main():
  samples = []
  print("[HEAT] Start 10 min monitoring ...")
  start = time.time()
  for i in range(600):
    cpu = psutil.cpu_percent(interval=1.0)
    temp = get_temp()
    ts = time.time()
    samples.append(
      {
        "idx": i,
        "ts": ts,
        "iso": datetime.fromtimestamp(ts).isoformat(),
        "cpu": cpu,
        "temp": temp,
      }
    )
    print(f"[HEAT] {i:03d} cpu={cpu:.1f}% temp={temp}")

  with open(OUT_FILE, "w") as f:
    json.dump(samples, f, indent=2)
  print("[HEAT] done, saved to", OUT_FILE)


if __name__ == "__main__":
  main()

