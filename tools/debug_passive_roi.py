# -*- coding: utf-8 -*-
"""直接验证 passive_roi 在 pipeline 中的计算"""

import sys
from pathlib import Path
import numpy as np
import cv2

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from vision_pipeline.pipeline_controller import PipelineController

# 两帧有差异的合成图
h, w = 240, 320
frame1 = np.ones((h, w, 3), dtype=np.uint8) * 128
frame2 = frame1.copy()
cv2.rectangle(frame2, (30, 20), (70, 60), (200, 200, 200), -1)  # 40x40 块
cv2.rectangle(frame2, (200, 150), (250, 200), (180, 180, 180), -1)  # 50x50 块

pc = PipelineController()
pc._update_frame_context(frame1, ts=0)
print(f"Frame 0 (无 last_gray): roi_count={pc.roi_count}")

pc._update_frame_context(frame2, ts=1/30)
print(f"Frame 1 (有 diff): roi_count={pc.roi_count}, motion_instability={pc.motion_instability:.3f}")

# 再一帧，块移动
frame3 = frame1.copy()
cv2.rectangle(frame3, (35, 25), (75, 65), (200, 200, 200), -1)
cv2.rectangle(frame3, (205, 155), (255, 205), (180, 180, 180), -1)
pc._update_frame_context(frame3, ts=2/30)
print(f"Frame 2 (块移动): roi_count={pc.roi_count}")

# 直接测 passive_roi 函数
from vision_perception_b1.passive_roi import compute_passive_roi_count
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
diff = cv2.absdiff(gray1, gray2)
print(f"\nDirect: diff mean={np.mean(diff):.1f}, max={np.max(diff)}, roi_count={compute_passive_roi_count(diff, h*w)}")
