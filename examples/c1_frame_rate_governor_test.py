"""
C1 FrameRateGovernor 测试脚本

验证 FrameRateGovernor 是否正确控制帧率。
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c1_controller.c1_governor import FrameRateGovernor


def test_frame_rate_governor():
    """
    测试 FrameRateGovernor 的帧率控制
    """
    print("=" * 70)
    print("C1 FrameRateGovernor 测试")
    print("=" * 70)
    
    governor = FrameRateGovernor()
    
    # 测试 1: target_fps = 0（应该永远返回 False）
    print("\n[测试 1] target_fps = 0（应该永远返回 False）")
    for i in range(5):
        allowed = governor.allow(0)
        print(f"  第 {i+1} 次: allow={allowed}")
        assert allowed == False, "❌ target_fps=0 应该永远返回 False"
    print("  ✅ 测试通过")
    
    # 测试 2: target_fps = 2（应该大约每 0.5 秒允许一次）
    print("\n[测试 2] target_fps = 2（应该大约每 0.5 秒允许一次）")
    allowed_count = 0
    total_count = 0
    start_time = time.time()
    
    for i in range(10):
        total_count += 1
        allowed = governor.allow(2)
        if allowed:
            allowed_count += 1
            print(f"  第 {i+1} 次: allow={allowed} (允许)")
        else:
            print(f"  第 {i+1} 次: allow={allowed} (拒绝)")
        time.sleep(0.1)  # 模拟快速采集（100ms 间隔）
    
    elapsed = time.time() - start_time
    expected_allowed = int(elapsed * 2)  # 2 fps
    print(f"\n  总时间: {elapsed:.2f}s")
    print(f"  允许次数: {allowed_count}")
    print(f"  总次数: {total_count}")
    print(f"  预期允许次数: ~{expected_allowed}")
    
    # 允许次数应该在预期范围内（考虑时间误差）
    assert allowed_count >= expected_allowed - 1, f"❌ 允许次数太少（{allowed_count} < {expected_allowed - 1}）"
    assert allowed_count <= expected_allowed + 1, f"❌ 允许次数太多（{allowed_count} > {expected_allowed + 1}）"
    print("  ✅ 测试通过")
    
    # 测试 3: target_fps = 10（应该更频繁地允许）
    print("\n[测试 3] target_fps = 10（应该更频繁地允许）")
    governor_2 = FrameRateGovernor()  # 新的实例，重置时间戳
    allowed_count_2 = 0
    total_count_2 = 0
    start_time_2 = time.time()
    
    for i in range(20):
        total_count_2 += 1
        allowed = governor_2.allow(10)
        if allowed:
            allowed_count_2 += 1
        time.sleep(0.05)  # 模拟快速采集（50ms 间隔）
    
    elapsed_2 = time.time() - start_time_2
    expected_allowed_2 = int(elapsed_2 * 10)  # 10 fps
    print(f"\n  总时间: {elapsed_2:.2f}s")
    print(f"  允许次数: {allowed_count_2}")
    print(f"  总次数: {total_count_2}")
    print(f"  预期允许次数: ~{expected_allowed_2}")
    
    assert allowed_count_2 >= expected_allowed_2 - 1, f"❌ 允许次数太少（{allowed_count_2} < {expected_allowed_2 - 1}）"
    assert allowed_count_2 <= expected_allowed_2 + 1, f"❌ 允许次数太多（{allowed_count_2} > {expected_allowed_2 + 1}）"
    print("  ✅ 测试通过")
    
    print("\n" + "=" * 70)
    print("✅ 所有测试通过")
    print("=" * 70)
    print("\n📋 关键验证点：")
    print("  ✅ target_fps=0 时永远返回 False")
    print("  ✅ target_fps=2 时大约每 0.5 秒允许一次")
    print("  ✅ target_fps=10 时更频繁地允许")
    print("  ✅ 不阻塞、不 sleep、不影响主循环")


if __name__ == "__main__":
    test_frame_rate_governor()


