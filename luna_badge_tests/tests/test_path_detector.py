from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_path_detector")
"""
Path Detector 测试脚本（F6）

测试可走路径识别模块
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

from vision.path_detector import PathDetector
from vision.hazard_detector import HazardDetector

logger = logging.getLogger(__name__)


def create_test_image_with_path():
    """创建包含可走路径的测试图像"""
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # 背景：地面（灰色）
    frame.fill(128)

    # 底部区域：更亮的地面（可走区域）
    frame[int(height * 0.7):, :] = [140, 140, 140]

    # 中间：可走路径（明亮的走廊）
    path_width = width // 3
    path_start = width // 3
    frame[:, path_start:path_start + path_width] = [160, 160, 160]

    # 左侧障碍：深色物体
    cv2.rectangle(frame, (50, height//3), (200, 2*height//3), (50, 50, 50), -1)

    # 右侧障碍：深色物体
    cv2.rectangle(frame, (width - 200, height//3), (width - 50, 2*height//3), (50, 50, 50), -1)

    # 中间上方：高光区域（可能被压制的区域）
    cv2.rectangle(frame, (width//2 - 100, 100), (width//2 + 100, 300), (250, 250, 250), -1)

    return frame


def visualize_walkable_grid(walkable_grid: np.ndarray, frame: np.ndarray, output_path: str = None):
    """
    可视化可走路径网格

    Args:
        walkable_grid: 可走路径网格（0/1）
        frame: 原图
        output_path: 输出路径（可选）
    """
    h, w = frame.shape[:2]
    rows, cols = walkable_grid.shape

    # 创建覆盖层
    overlay = frame.copy()
    tile_h = h // rows
    tile_w = w // cols

    for i in range(rows):
        for j in range(cols):
            y1 = i * tile_h
            y2 = (i + 1) * tile_h if i < rows - 1 else h
            x1 = j * tile_w
            x2 = (j + 1) * tile_w if j < cols - 1 else w

            walkable = walkable_grid[i, j]

            # 根据可走性设置颜色
            if walkable:
                color = (0, 255, 0)  # 绿色 - 可走
                alpha = 0.3
            else:
                color = (0, 0, 255)  # 红色 - 不可走
                alpha = 0.5

            # 绘制半透明覆盖层
            overlay_tile = overlay[y1:y2, x1:x2].copy()
            cv2.rectangle(
                overlay_tile,
                (0, 0),
                (overlay_tile.shape[1], overlay_tile.shape[0]),
                color,
                -1
            )
            overlay[y1:y2, x1:x2] = cv2.addWeighted(
                overlay[y1:y2, x1:x2],
                1.0 - alpha,
                overlay_tile,
                alpha,
                0
            )

            # 显示状态
            status_text = "GO" if walkable else "NO"
            cv2.putText(
                overlay,
                status_text,
                (x1 + 10, y1 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
            )

    if output_path:
        cv2.imwrite(output_path, overlay)

    return overlay


def test_path_detector():
    """测试路径检测器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Path Detector 测试")
    log.info("=" * 80")

    try:
        # 创建危险检测器（F4）
        log.info("\n📦 正在初始化 Hazard Detector (F4)...")
        hazard_detector = HazardDetector()
        log.info("✅ Hazard Detector 初始化成功")

        # 创建路径检测器（F6）
        log.info("\n📦 正在初始化 Path Detector (F6)...")
        path_detector = PathDetector(hazard_detector=hazard_detector)
        log.info("✅ Path Detector 初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像（包含可走路径和障碍）...")
        test_image = create_test_image_with_path()
        log.info(f"✅ 测试图像创建成功: {test_image.shape}")

        # 处理图像
        log.info("\n🔍 正在检测可走路径...")
        walkable_grid, walkable_scores = path_detector.process(test_image)

        log.info(f"\n📊 可走路径网格 ({walkable_grid.shape[0]}×{walkable_grid.shape[1]}):")
        for i in range(walkable_grid.shape[0]):
            row_display = " ".join([
                f"{'✅' if walkable_grid[i, j] else '❌'}"
                for j in range(walkable_grid.shape[1])
            ])
            log.info(f"   行 {i}: {row_display}")

        log.info(f"\n📊 可走性分数:")
        for i in range(walkable_scores.shape[0]):
            row_scores = " ".join([
                f"{walkable_scores[i, j]:.2f}".rjust(5)
                for j in range(walkable_scores.shape[1])
            ])
            log.info(f"   行 {i}: [{row_scores}]")

        # 统计
        total_tiles = walkable_grid.size
        walkable_count = np.sum(walkable_grid)
        log.info(f"\n📈 统计:")
        log.info(f"   总 tiles: {total_tiles}")
        log.info(f"   可走 tiles: {walkable_count} ({walkable_count/total_tiles*100:.1f}%)")
        log.info(f"   不可走 tiles: {total_tiles - walkable_count} ({(total_tiles - walkable_count)/total_tiles*100:.1f}%)")

        # 可视化
        log.info("\n🎨 生成可走路径可视化...")
        output_dir = "logs/path_detector"
        os.makedirs(output_dir, exist_ok=True)

        original_path = os.path.join(output_dir, "test_original.jpg")
        walkable_path = os.path.join(output_dir, "test_walkable_grid.jpg")

        cv2.imwrite(original_path, test_image)
        visualized = visualize_walkable_grid(walkable_grid, test_image, walkable_path)

        log.info(f"💾 结果已保存:")
        log.info(f"   原图: {original_path}")
        log.info(f"   可走路径网格: {walkable_path}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_path_detector_from_camera():
    """从摄像头测试路径检测器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Path Detector 测试（摄像头）")
    log.info("=" * 80")

    try:
        # 创建检测器
        log.info("\n📦 正在初始化检测器...")
        hazard_detector = HazardDetector()
        path_detector = PathDetector(hazard_detector=hazard_detector)
        log.info("✅ 检测器初始化成功")

        # 打开摄像头
        log.info("\n📹 正在打开摄像头...")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            log.info("❌ 无法打开摄像头")
            return False

        log.info("✅ 摄像头打开成功")
        log.info("\n💡 提示:")
        log.info("   - 按 'q' 键退出")
        log.info("   - 按 's' 键保存当前帧")

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                log.info("⚠️ 无法读取摄像头画面")
                break

            frame_count += 1

            # 处理图像
            walkable_grid, walkable_scores = path_detector.process(frame)

            # 可视化
            visualized = visualize_walkable_grid(walkable_grid, frame)

            # 每 30 帧打印一次统计
            if frame_count % 30 == 0:
                walkable_count = np.sum(walkable_grid)
                total_tiles = walkable_grid.size
                log.info(f"\n📊 帧 #{frame_count}: 可走 {walkable_count}/{total_tiles} tiles ({walkable_count/total_tiles*100:.1f}%)")

            # 显示
            cv2.imshow("Path Detector", visualized)

            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log.info("\n👋 用户退出")
                break
            elif key == ord('s'):
                # 保存当前帧
                output_dir = "logs/path_detector"
                os.makedirs(output_dir, exist_ok=True)
                import time
                timestamp = int(time.time())
                original_path = os.path.join(output_dir, f"camera_original_{timestamp}.jpg")
                walkable_path = os.path.join(output_dir, f"camera_walkable_{timestamp}.jpg")
                cv2.imwrite(original_path, frame)
                cv2.imwrite(walkable_path, visualized)
                log.info(f"\n💾 已保存: {original_path}, {walkable_path}")

        cap.release()
        cv2.destroyAllWindows()

        log.info(f"\n✅ 测试完成，共处理 {frame_count} 帧")
        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Path Detector 测试开始")
    log.info("=" * 80")

    import argparse
    parser = argparse.ArgumentParser(description="Path Detector 测试")
    parser.add_argument(
        "--camera",
        action="store_true",
        help="使用摄像头进行测试（而不是测试图像）",
    )
    args = parser.parse_args()

    try:
        if args.camera:
            # 从摄像头测试
            success = test_path_detector_from_camera()
        else:
            # 从测试图像测试
            success = test_path_detector()

        if success:
            log.info(f"\n{'='*80}")
            log.info("🎉 所有测试完成！")
            log.info(f"{'='*80}")
            log.info("\n💡 提示:")
            log.info("   - 修改 vision/path_detector/config.py 可以调整参数")
            log.info("   - 使用 --camera 参数可以从摄像头测试")
            log.info("   - 绿色 = 可走，红色 = 不可走")
            return 0
        else:
            log.info(f"\n{'='*80}")
            log.info("❌ 测试失败")
            log.info(f"{'='*80}")
            return 1

    except KeyboardInterrupt:
        log.info("\n\n👋 用户中断")
        return 0
    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())













