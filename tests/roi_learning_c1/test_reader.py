import json

from roi_learning_c1.reader import read_timeline_jsonl


def test_reader_reads_lines(tmp_path):
    p = tmp_path / "t.jsonl"
    p.write_text(
        json.dumps({"a": 1}) + "\n" + json.dumps({"b": 2}) + "\n",
        encoding="utf-8",
    )
    frames = list(read_timeline_jsonl(str(p)))
    assert frames[0]["a"] == 1
    assert frames[1]["b"] == 2
