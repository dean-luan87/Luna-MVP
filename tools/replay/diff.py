def diff_dict(prev: dict, curr: dict) -> dict:
    diff = {}
    keys = set(prev.keys()) | set(curr.keys())
    for k in keys:
        if prev.get(k) != curr.get(k):
            diff[k] = {
                "from": prev.get(k),
                "to": curr.get(k),
            }
    return diff
