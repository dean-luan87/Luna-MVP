from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_hazard_detector")
"""
Hazard Detector 测试脚本（F4）

测试危险因素增强识别模块
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

try:
    import cv2
    import numpy as np
except ImportError:
    log.info("❌ OpenCV 或 NumPy 未安装")
    sys.exit(1)

from vision.hazard_detector import HazardDetector
from vision.hazard_detector.edge_detector import EdgeDetector
from vision.hazard_detector.texture_analyzer import TextureAnalyzer
from vision.hazard_detector.shape_analyzer import ShapeAnalyzer

logger = logging.getLogger(__name__)


def create_test_image_with_hazards():
    """创建包含危险因素的测试图像"""
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # 背景：灰色地面
    frame.fill(128)

    # 危险 1：边缘（桌边/墙角）- 左上角水平线
    cv2.line(frame, (0, 200), (width//3, 200), (255, 255, 255), 5)

    # 危险 2：异常占位物体（箱子）- 中间左侧
    x1, y1, x2, y2 = width//4, height//2-50, width//4+150, height//2+100
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 2)

    # 危险 3：台阶纹理 - 底部中间
    for i in range(5):
        y = height - 100 - i * 20
        x1_line = width//2 - 100
        x2_line = width//2 + 100
        cv2.line(frame, (x1_line, y), (x2_line, y), (180, 180, 180), 2)

    # 危险 4：复杂纹理区域（水坑/斑马线）- 右上方
    pattern_size = 40
    for i in range(height//4, height//2, pattern_size):
        for j in range(width//2, width, pattern_size):
            if (i // pattern_size + j // pattern_size) % 2 == 0:
                cv2.rectangle(
                    frame,
                    (j, i),
                    (j + pattern_size, i + pattern_size),
                    (50, 50, 50),
                    -1
                )

    return frame


def visualize_risk_map(risk_map: np.ndarray, frame: np.ndarray, output_path: str = None):
    """
    可视化风险热力图

    Args:
        risk_map: 风险矩阵
        frame: 原图
        output_path: 输出路径（可选）
    """
    h, w = frame.shape[:2]
    rows, cols = risk_map.shape

    # 创建热力图覆盖层
    overlay = frame.copy()
    result = frame.copy()
    tile_h = h // rows
    tile_w = w // cols

    for i in range(rows):
        for j in range(cols):
            y1 = i * tile_h
            y2 = (i + 1) * tile_h if i < rows - 1 else h
            x1 = j * tile_w
            x2 = (j + 1) * tile_w if j < cols - 1 else w

            risk = risk_map[i, j]

            # 根据风险等级设置颜色和透明度
            if risk < 0.3:
                color = (0, 255, 0)  # 绿色 - 低风险
                alpha = 0.2
            elif risk < 0.6:
                color = (0, 165, 255)  # 橙色 - 中风险
                alpha = 0.4
            else:
                color = (0, 0, 255)  # 红色 - 高风险
                alpha = 0.6

            # 绘制半透明覆盖层
            overlay_tile = overlay[y1:y2, x1:x2].copy()
            cv2.rectangle(overlay_tile, (0, 0), (overlay_tile.shape[1], overlay_tile.shape[0]), color, -1)
            result[y1:y2, x1:x2] = cv2.addWeighted(result[y1:y2, x1:x2], 1.0 - alpha, overlay_tile, alpha, 0)

            # 显示风险分数
            risk_text = f"{risk:.2f}"
            cv2.putText(
                result,
                risk_text,
                (x1 + 10, y1 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

    if output_path:
        cv2.imwrite(output_path, result)

    return result


def test_hazard_detector():
    """测试危险检测器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Hazard Detector 测试")
    log.info("=" * 80")

    try:
        # 创建检测器
        log.info("\n📦 正在初始化 Hazard Detector...")
        detector = HazardDetector()
        log.info("✅ Hazard Detector 初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像（包含危险因素）...")
        test_image = create_test_image_with_hazards()
        log.info(f"✅ 测试图像创建成功: {test_image.shape}")

        # 计算风险
        log.info("\n🔍 正在计算风险热力图...")
        result = detector.compute_risk_with_details(test_image)
        risk_map = result["risk_map"]
        details = result["details"]

        log.info(f"\n📊 风险热力图 ({risk_map.shape[0]}×{risk_map.shape[1]}):")
        for i in range(risk_map.shape[0]):
            row_risks = " ".join([f"{risk_map[i, j]:.2f}".rjust(6) for j in range(risk_map.shape[1])])
            log.info(f"   行 {i}: [{row_risks}]")

        # 打印详细信息（前几个高风险的 tile）
        log.info(f"\n📋 高风险区域详情:")
        sorted_tiles = sorted(details.items(), key=lambda x: x[1]["risk"], reverse=True)
        for (i, j), detail in sorted_tiles[:5]:
            risk_level = detector.get_risk_level(detail["risk"])
            log.info(f"   Tile ({i},{j}): 风险={detail['risk']:.2f} ({risk_level})")
            log.info(f"      边缘密度: {detail['edge_density']:.3f}")
            log.info(f"      纹理跳跃: {detail['texture_jump']:.2f}")
            log.info(f"      形状异常: {detail['shape_abnormal']:.3f}")

        # 获取安全路径候选
        safe_paths = detector.get_safe_path_candidates(risk_map, top_k=3)
        log.info(f"\n✅ 安全路径候选（列索引，按风险从低到高）: {safe_paths}")

        # 可视化
        log.info("\n🎨 生成风险热力图可视化...")
        output_dir = "logs/hazard_detector"
        os.makedirs(output_dir, exist_ok=True)

        original_path = os.path.join(output_dir, "test_original.jpg")
        heatmap_path = os.path.join(output_dir, "test_risk_heatmap.jpg")

        cv2.imwrite(original_path, test_image)
        visualized = visualize_risk_map(risk_map, test_image, heatmap_path)

        log.info(f"💾 结果已保存:")
        log.info(f"   原图: {original_path}")
        log.info(f"   风险热力图: {heatmap_path}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_individual_components():
    """测试各个组件"""
    log.info("\n" + "=" * 80)
    log.info("🧪 组件单独测试")
    log.info("=" * 80")

    try:
        # 创建测试 tile
        test_tile = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

        # 测试边缘检测器
        log.info("\n🔍 测试 Edge Detector...")
        edge_detector = EdgeDetector()
        edge_density, edge_map = edge_detector.detect(test_tile)
        log.info(f"   ✅ 边缘密度: {edge_density:.3f}")

        # 测试纹理分析器
        log.info("\n🔍 测试 Texture Analyzer...")
        texture_analyzer = TextureAnalyzer()
        texture_jump = texture_analyzer.analyze(test_tile)
        log.info(f"   ✅ 纹理跳跃: {texture_jump:.2f}")

        # 测试形状分析器
        log.info("\n🔍 测试 Shape Analyzer...")
        shape_analyzer = ShapeAnalyzer()
        shape_abnormal = shape_analyzer.analyze(edge_map)
        log.info(f"   ✅ 形状异常度: {shape_abnormal:.3f}")

        log.info(f"\n✅ 所有组件测试通过")
        return True

    except Exception as e:
        log.info(f"\n❌ 组件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scalability():
    """测试可扩展性"""
    log.info("\n" + "=" * 80)
    log.info("🧪 可扩展性测试")
    log.info("=" * 80")

    test_image = create_test_image_with_hazards()

    # 测试不同的网格配置
    test_configs = [
        (3, 3),
        (3, 5),
        (5, 3),
        (5, 5),
    ]

    log.info("\n📐 测试不同网格配置:")

    for rows, cols in test_configs:
        try:
            detector = HazardDetector(rows=rows, cols=cols)
            result = detector.compute_risk_with_details(test_image)
            risk_map = result["risk_map"]
            avg_risk = float(np.mean(risk_map))
            max_risk = float(np.max(risk_map))
            log.info(f"   ✅ {rows}×{cols}: 平均风险={avg_risk:.3f}, 最大风险={max_risk:.3f}")
        except Exception as e:
            log.info(f"   ❌ {rows}×{cols}: 失败 - {e}")
            return False

    log.info(f"\n✅ 所有配置测试通过")
    return True


def main():
    """主函数"""
    log.info("🚀 Hazard Detector 测试开始")
    log.info("=" * 80")

    try:
        # 1. 组件单独测试
        success1 = test_individual_components()

        if not success1:
            log.info("\n❌ 组件测试失败")
            return 1

        # 2. 完整功能测试
        success2 = test_hazard_detector()

        if not success2:
            log.info("\n❌ 完整功能测试失败")
            return 1

        # 3. 可扩展性测试
        success3 = test_scalability()

        if not success3:
            log.info("\n❌ 可扩展性测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 风险热力图已保存到 logs/hazard_detector/")
        log.info("   - 风险分数范围: 0.0 (安全) ~ 1.0 (危险)")
        log.info("   - 安全路径候选是按列风险从低到高排序")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

