# vision_pipeline/b2/v03/validation/test_validation.py
"""
快速测试验收脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入验收器
from b2_v05_validation import B2V05Validator

def test_validator():
    """测试验收器基本功能"""
    print("测试 B2V05Validator...")
    
    validator = B2V05Validator()
    
    # 检查常量
    assert len(validator.ALLOWED_GATE_MODES) == 3, "Gate Mode 应该是 3 种"
    assert len(validator.ALLOWED_EVIDENCE_STATES) == 4, "Evidence 状态应该是 4 种"
    assert len(validator.ALLOWED_IMPACTS) == 6, "Impact 应该是 6 种"
    
    print("✅ 验收器常量检查通过")
    print(f"   Gate Modes: {validator.ALLOWED_GATE_MODES}")
    print(f"   Evidence States: {validator.ALLOWED_EVIDENCE_STATES}")
    print(f"   Allowed Impacts: {validator.ALLOWED_IMPACTS}")
    
    # 测试结果对象
    from b2_v05_validation import ValidationResult
    result = ValidationResult()
    result.add_pass("测试项1")
    result.add_warning("测试项2", "这是警告")
    result.add_fail("测试项3", "这是失败")
    
    assert len(result.passed) == 1
    assert len(result.warnings) == 1
    assert len(result.failed) == 1
    assert not result.is_all_passed()
    
    print("✅ ValidationResult 功能正常")
    
    print("\n" + "=" * 70)
    print("验收脚本基本功能测试通过！")
    print("=" * 70)

if __name__ == "__main__":
    test_validator()
