"""
VisionDispatcher - MoE调度器
统一运行 YOLO / SegFormer / Depth / Flow
"""


class VisionDispatcher:
    def __init__(self, yolo, segformer, depth, flow):
        self.yolo = yolo
        self.seg = segformer
        self.depth = depth
        self.flow = flow

    def run_all(self, frame, prev_frame=None):
        return {
            "det": self.yolo.detect(frame),
            "seg": self.seg.segment(frame),
            "depth": self.depth.estimate(frame),
            "flow": self.flow.compute(frame, prev_frame)
        }

























