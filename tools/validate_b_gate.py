import argparse
import json
from pathlib import Path
from typing import Dict, List


REQUIRED_LANGUAGE_FIELDS = {"text", "type", "source", "timestamp"}


def load_trace(path: Path) -> List[dict]:
    records = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def check_language_output(records: List[dict]) -> Dict[str, bool]:
    has_language = False
    fields_ok = True
    for record in records:
        language_output = record.get("language_output")
        if not language_output:
            continue
        has_language = True
        if not isinstance(language_output, dict):
            fields_ok = False
            continue
        if not REQUIRED_LANGUAGE_FIELDS.issubset(language_output.keys()):
            fields_ok = False
    return {
        "trace_has_language_output": has_language,
        "language_fields_present": fields_ok if has_language else False,
    }


def check_no_decision_leak(records: List[dict]) -> bool:
    for record in records:
        language_output = record.get("language_output")
        if not isinstance(language_output, dict):
            continue
        for forbidden in ("decision", "reason", "selected_result", "abilities"):
            if forbidden in language_output:
                return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True, help="trace jsonl path")
    parser.add_argument("--out", help="optional output json path")
    args = parser.parse_args()

    records = load_trace(Path(args.trace))
    lang_checks = check_language_output(records)
    no_leak = check_no_decision_leak(records)

    result = {
        "trace_records": len(records),
        "checks": {
            **lang_checks,
            "no_decision_leak": no_leak,
        },
        "gate_pass": all([lang_checks["trace_has_language_output"],
                          lang_checks["language_fields_present"],
                          no_leak]),
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    print(output)

    if not result["gate_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
