from typing import TextIO
from .schema import TimelineFrame


class TimelineRecorder:
    def __init__(self, fp: TextIO):
        self.fp = fp

    def record(self, frame: TimelineFrame):
        self.fp.write(frame.to_json() + "\n")
        self.fp.flush()
