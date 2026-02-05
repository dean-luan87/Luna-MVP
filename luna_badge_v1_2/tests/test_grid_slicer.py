from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_grid_slicer")
"""
Grid Slicer 测试脚本（F2）

测试空间切片模块
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

from capabilities.vision.types import SceneObj
from capabilities.vision.grid_slicer import (
    load_grid_config,
    generate_grid,
    assign_objects_to_grid,
    compute_risk_for_cell,
    build_grid_snapshot,
    save_grid_snapshot,
)

logger = logging.getLogger(__name__)


def test_grid_slicer():
    """测试网格切片功能"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Grid Slicer 测试")
    log.info("=" * 80")

    # 1. 加载网格配置
    log.info("\n📋 步骤 1: 加载网格配置")
    config = load_grid_config("config/grid_config.json")
    rows = config["rows"]
    cols = config["cols"]
    log.info(f"✅ 网格配置: {rows}×{cols} (rows×cols)")

    # 2. 构造假图像大小
    log.info("\n📐 步骤 2: 生成网格坐标")
    width = 1920
    height = 1080
    log.info(f"   图像尺寸: {width}×{height}")

    grid = generate_grid(width, height, rows, cols)
    log.info(f"✅ 生成 {len(grid)} 个格子")

    # 打印网格坐标（显示前几个）
    log.info(f"\n   网格坐标示例（前 5 个）:")
    for i, ((r, c), bbox) in enumerate(list(grid.items())[:5], 1):
        log.info(f"     [{i}] ({r},{c}): {bbox}")

    # 3. 构造虚拟检测结果
    log.info("\n🎯 步骤 3: 构造虚拟检测结果")
    
    # person at bottom-center（底部中心）
    # 假设 bottom-center 大约是 (row=4, col=1) 在 5×3 网格中
    person_bbox = [
        width // 3 + width // 6,      # x1
        height - height // 5 - 100,   # y1 (底部)
        width // 3 + width // 3,      # x2
        height - 50,                  # y2 (底部)
    ]
    person = SceneObj(cls="person", conf=0.9, bbox=person_bbox)
    log.info(f"   ✅ person: {person.bbox} (center: {person.center()})")

    # obstacle at mid-left（中间左侧）
    obstacle_bbox = [
        50,                           # x1 (左侧)
        height // 2 - 50,            # y1 (中间)
        200,                          # x2
        height // 2 + 50,            # y2 (中间)
    ]
    obstacle = SceneObj(cls="obstacle", conf=0.8, bbox=obstacle_bbox)
    log.info(f"   ✅ obstacle: {obstacle.bbox} (center: {obstacle.center()})")

    # stairs at top-center（顶部中心）
    stairs_bbox = [
        width // 3 + width // 6,      # x1
        50,                           # y1 (顶部)
        width // 3 + width // 3,      # x2
        150,                          # y2 (顶部)
    ]
    stairs = SceneObj(cls="stairs", conf=0.85, bbox=stairs_bbox)
    log.info(f"   ✅ stairs: {stairs.bbox} (center: {stairs.center()})")

    detections = [person, obstacle, stairs]
    log.info(f"✅ 构造了 {len(detections)} 个虚拟检测对象")

    # 4. 分配对象到网格
    log.info("\n📍 步骤 4: 分配对象到网格")
    grid_cells = assign_objects_to_grid(detections, grid, rows, cols)
    
    # 统计每个格子的对象数量
    log.info(f"\n   每个格子的对象数量:")
    for r in range(rows):
        for c in range(cols):
            obj_count = len(grid_cells[(r, c)]["objects"])
            if obj_count > 0:
                counts = grid_cells[(r, c)]["counts"]
                log.info(f"     ({r},{c}): {obj_count} 个对象 {counts}")

    # 5. 计算风险
    log.info("\n⚠️ 步骤 5: 计算风险矩阵")
    heatmap_risks = []
    for r in range(rows):
        row_risks = []
        for c in range(cols):
            risk = compute_risk_for_cell(grid_cells[(r, c)], r, rows)
            row_risks.append(risk)
            if risk > 0:
                log.info(f"     ({r},{c}): 风险 = {risk:.2f}")
        heatmap_risks.append(row_risks)

    # 打印风险矩阵
    log.info(f"\n   风险矩阵 ({rows}×{cols}):")
    for r, row_risks in enumerate(heatmap_risks):
        risk_str = " ".join([f"{risk:.2f}".rjust(6) for risk in row_risks])
        log.info(f"     行 {r}: [{risk_str}]")

    # 6. 构建网格快照
    log.info("\n📸 步骤 6: 构建网格快照")
    snapshot = build_grid_snapshot(grid_cells, rows, cols)
    
    log.info(f"✅ 网格快照创建成功")
    log.info(f"   时间戳: {snapshot['timestamp']}")
    log.info(f"   网格大小: {snapshot['grid_size']}")
    log.info(f"   安全路径候选: {snapshot['safe_path_candidates']}")

    # 7. 保存快照
    log.info("\n💾 步骤 7: 保存网格快照")
    filepath = save_grid_snapshot(snapshot)
    if filepath:
        log.info(f"✅ 快照已保存: {filepath}")
    else:
        log.info(f"⚠️ 快照保存失败")

    # 8. 打印完整快照（JSON 格式）
    log.info(f"\n📄 完整快照内容:")
    log.info("json.dumps(snapshot, indent=2, ensure_ascii=False)")

    return True


def test_grid_config_change():
    """测试配置变更（验证可扩展性）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 网格配置变更测试（验证可扩展性）")
    log.info("=" * 80")

    # 测试不同的网格配置
    test_configs = [
        {"rows": 3, "cols": 3},
        {"rows": 5, "cols": 3},
        {"rows": 7, "cols": 3},
    ]

    width = 1920
    height = 1080

    for config in test_configs:
        rows = config["rows"]
        cols = config["cols"]
        log.info(f"\n📐 测试 {rows}×{cols} 网格:")
        
        grid = generate_grid(width, height, rows, cols)
        log.info(f"   ✅ 生成 {len(grid)} 个格子")
        
        # 验证所有格子都存在
        expected_count = rows * cols
        actual_count = len(grid)
        if actual_count == expected_count:
            log.info(f"   ✅ 格子数量正确: {actual_count}")
        else:
            log.info(f"   ❌ 格子数量错误: 期望 {expected_count}, 实际 {actual_count}")
            return False

    log.info(f"\n✅ 所有配置测试通过")
    return True


def main():
    """主函数"""
    log.info("🚀 Grid Slicer 测试开始")
    log.info("=" * 80")

    try:
        # 1. 基础功能测试
        success1 = test_grid_slicer()

        if not success1:
            log.info("\n❌ 基础功能测试失败")
            return 1

        # 2. 配置变更测试
        success2 = test_grid_config_change()

        if not success2:
            log.info("\n❌ 配置变更测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 修改 config/grid_config.json 可以改变网格大小")
        log.info("   - 例如改为 3×7: {\"rows\": 7, \"cols\": 3}")
        log.info("   - 所有代码无需修改即可支持新配置")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
























