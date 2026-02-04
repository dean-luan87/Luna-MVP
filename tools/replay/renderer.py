from pprint import pprint
from .diff import diff_dict


def render_frame(frame, prev_frame=None):
    print("\n" + "=" * 60)
    print(f"[t = {frame['ts']:.2f}]")

    if prev_frame:
        print("\n[World Δ]")
        pprint(diff_dict(prev_frame["entities"], frame["entities"]))

        print("\n[Tasks Δ]")
        prev_tasks = {t["task"]: t for t in prev_frame.get("tasks", [])}
        curr_tasks = {t["task"]: t for t in frame.get("tasks", [])}
        pprint(diff_dict(prev_tasks, curr_tasks))

        print("\n[C Decision Δ]")
        pprint(diff_dict(prev_frame["c_decision"], frame["c_decision"]))
    else:
        print("\n[World]")
        pprint(frame["entities"])
        print("\n[Tasks]")
        pprint(frame["tasks"])
        print("\n[C Decision]")
        pprint(frame["c_decision"])
