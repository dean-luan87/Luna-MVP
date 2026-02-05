from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_image_corrector")
"""
Image Corrector 测试脚本（F5.5）

测试图像补正 / 轻量增强模块
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

from core.vision.image_corrector import ImageCorrector

logger = logging.getLogger(__name__)


def create_test_image():
    """创建测试图像（包含低光、高光、噪声等）"""
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # 背景：中等灰度
    frame.fill(128)

    # 区域 1：低光区域（左上角）
    frame[0:height//3, 0:width//3] = [30, 30, 30]

    # 区域 2：高光区域（中间）
    mid_h, mid_w = height//2, width//2
    frame[mid_h-100:mid_h+100, mid_w-200:mid_w+200] = [250, 250, 250]

    # 区域 3：添加噪声（右上角）
    noise = np.random.randint(0, 50, (height//4, width//4, 3), dtype=np.uint8)
    frame[0:height//4, 3*width//4:] = noise

    # 区域 4：模糊区域（底部）
    blur_area = frame[3*height//4:, :].copy()
    blur_area = cv2.GaussianBlur(blur_area, (15, 15), 0)
    frame[3*height//4:, :] = blur_area

    return frame


def test_image_corrector_from_image():
    """从测试图像测试补正器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Image Corrector 测试（测试图像）")
    log.info("=" * 80")

    try:
        # 创建补正器
        log.info("\n📦 正在初始化 Image Corrector...")
        corrector = ImageCorrector()
        log.info("✅ Image Corrector 初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像（包含低光、高光、噪声）...")
        test_image = create_test_image()
        log.info(f"✅ 测试图像创建成功: {test_image.shape}")

        # 处理图像
        log.info("\n🔧 正在处理图像...")
        enhanced_image, meta = corrector.process(test_image)

        log.info("\n📊 处理统计:")
        for key, value in meta.items():
            status = "✅" if value else "❌"
            log.info(f"   {status} {key}: {value}")

        # 保存结果
        output_dir = "logs/image_corrector"
        os.makedirs(output_dir, exist_ok=True)

        original_path = os.path.join(output_dir, "test_original.jpg")
        enhanced_path = os.path.join(output_dir, "test_enhanced.jpg")

        cv2.imwrite(original_path, test_image)
        cv2.imwrite(enhanced_path, enhanced_image)

        log.info(f"\n💾 结果已保存:")
        log.info(f"   原图: {original_path}")
        log.info(f"   增强后: {enhanced_path}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_corrector_from_camera():
    """从摄像头测试补正器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Image Corrector 测试（摄像头）")
    log.info("=" * 80")

    try:
        # 创建补正器
        log.info("\n📦 正在初始化 Image Corrector...")
        corrector = ImageCorrector()
        log.info("✅ Image Corrector 初始化成功")

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
            enhanced_frame, meta = corrector.process(frame)

            # 每 30 帧打印一次统计
            if frame_count % 30 == 0:
                enabled_steps = [k for k, v in meta.items() if v]
                log.info(f"\n📊 帧 #{frame_count} 已启用步骤: {', '.join(enabled_steps)}")

            # 并排显示原图和增强后
            # 如果图像太大，先缩放
            h, w = frame.shape[:2]
            if w > 1920:
                scale = 1920 / w
                new_w = 1920
                new_h = int(h * scale)
                frame_display = cv2.resize(frame, (new_w, new_h))
                enhanced_display = cv2.resize(enhanced_frame, (new_w, new_h))
            else:
                frame_display = frame
                enhanced_display = enhanced_frame

            # 合并显示
            combined = np.hstack([frame_display, enhanced_display])

            # 添加标题
            cv2.putText(
                combined,
                "Original | Enhanced",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # 显示已启用步骤
            y_offset = 60
            for i, (key, value) in enumerate(meta.items()):
                if value:
                    text = f"{key}: ON"
                    color = (0, 255, 0)
                else:
                    text = f"{key}: OFF"
                    color = (128, 128, 128)
                cv2.putText(
                    combined,
                    text,
                    (10, y_offset + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                )

            cv2.imshow("Image Corrector", combined)

            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log.info("\n👋 用户退出")
                break
            elif key == ord('s'):
                # 保存当前帧
                output_dir = "logs/image_corrector"
                os.makedirs(output_dir, exist_ok=True)
                import time
                timestamp = int(time.time())
                original_path = os.path.join(output_dir, f"camera_original_{timestamp}.jpg")
                enhanced_path = os.path.join(output_dir, f"camera_enhanced_{timestamp}.jpg")
                cv2.imwrite(original_path, frame)
                cv2.imwrite(enhanced_path, enhanced_frame)
                log.info(f"\n💾 已保存: {original_path}, {enhanced_path}")

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
    log.info("🚀 Image Corrector 测试开始")
    log.info("=" * 80")

    import argparse
    parser = argparse.ArgumentParser(description="Image Corrector 测试")
    parser.add_argument(
        "--camera",
        action="store_true",
        help="使用摄像头进行测试（而不是测试图像）",
    )
    args = parser.parse_args()

    try:
        if args.camera:
            # 从摄像头测试
            success = test_image_corrector_from_camera()
        else:
            # 从测试图像测试
            success = test_image_corrector_from_image()

        if success:
            log.info(f"\n{'='*80}")
            log.info("🎉 所有测试完成！")
            log.info(f"{'='*80}")
            log.info("\n💡 提示:")
            log.info("   - 修改 core/vision/correct_config.py 可以调整参数")
            log.info("   - 使用 --camera 参数可以从摄像头测试")
            log.info("   - 所有子模块都可以通过配置开关控制是否启用")
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













