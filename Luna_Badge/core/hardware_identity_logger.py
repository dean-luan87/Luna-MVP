"""
模块4：硬件编码记录机制
实现文件：core/hardware_identity_logger.py
"""
import json
import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any


class HardwareIdentityLogger:
    """
    硬件编码记录机制
    功能：记录设备唯一编码（序列号）、激活时间、使用次数等，绑定账号
    """
    
    def __init__(self, log_path="data/hardware_id.json"):
        self.log_path = log_path
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
    
    def hardware_identity_logger(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        """
        记录设备硬件身份信息
        
        Args:
            account_id: 绑定的账号ID
            
        Returns:
            硬件身份信息
        """
        # 检查是否已有记录
        if os.path.exists(self.log_path):
            record = self.load_hardware_record()
            if record:
                # 更新启动次数
                record['boot_count'] = record.get('boot_count', 0) + 1
                record['last_boot_time'] = datetime.now().isoformat()
                
                # 如果提供了账号ID且未绑定，则绑定
                if account_id and not record.get('account_id'):
                    record['account_id'] = account_id
                
                self.save_hardware_record(record)
                return record
        
        # 创建新记录
        record = {
            "serial": str(uuid.uuid4()),
            "first_activation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "boot_count": 1,
            "last_boot_time": datetime.now().isoformat(),
            "account_id": account_id
        }
        
        self.save_hardware_record(record)
        return record
    
    def save_hardware_record(self, record: Dict[str, Any]) -> bool:
        """
        保存硬件记录到文件
        
        Args:
            record: 硬件记录字典
            
        Returns:
            是否保存成功
        """
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存硬件记录失败: {e}")
            return False
    
    def load_hardware_record(self) -> Optional[Dict[str, Any]]:
        """
        加载硬件记录
        
        Returns:
            硬件记录字典，如果不存在则返回None
        """
        if not os.path.exists(self.log_path):
            return None
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载硬件记录失败: {e}")
            return None
    
    def bind_account(self, account_id: str) -> bool:
        """
        绑定账号
        
        Args:
            account_id: 账号ID
            
        Returns:
            是否绑定成功
        """
        record = self.load_hardware_record()
        if not record:
            record = self.hardware_identity_logger()
        
        record['account_id'] = account_id
        return self.save_hardware_record(record)
    
    def get_serial_number(self) -> Optional[str]:
        """
        获取设备序列号
        
        Returns:
            序列号
        """
        record = self.load_hardware_record()
        return record.get('serial') if record else None
    
    def get_boot_count(self) -> int:
        """
        获取启动次数
        
        Returns:
            启动次数
        """
        record = self.load_hardware_record()
        return record.get('boot_count', 0) if record else 0
    
    def upload_to_backend(self, backend_url: str = "https://api.luna.ai/hardware/register") -> bool:
        """
        上传硬件信息到后台（预留接口）
        
        Args:
            backend_url: 后台API地址
            
        Returns:
            是否上传成功
        """
        record = self.load_hardware_record()
        if not record:
            return False
        
        # TODO: 实现实际上传逻辑
        print(f"准备上传硬件信息到: {backend_url}")
        print(f"数据: {json.dumps(record, indent=2)}")
        
        return True


def demo_hardware_logger():
    """演示硬件编码记录功能"""
    print("\n" + "=" * 60)
    print("模块4：硬件编码记录机制演示")
    print("=" * 60)
    
    logger = HardwareIdentityLogger()
    
    # 初始化硬件记录
    print("\n1. 初始化硬件记录...")
    record = logger.hardware_identity_logger()
    print(f"   ✓ 序列号: {record['serial']}")
    print(f"   ✓ 首次激活: {record['first_activation']}")
    print(f"   ✓ 启动次数: {record['boot_count']}")
    
    # 绑定账号
    print("\n2. 绑定账号...")
    account_id = "user_12345"
    success = logger.bind_account(account_id)
    if success:
        print(f"   ✓ 已绑定账号: {account_id}")
    
    # 再次启动（模拟）
    print("\n3. 模拟第二次启动...")
    record = logger.hardware_identity_logger(account_id)
    print(f"   ✓ 启动次数: {record['boot_count']}")
    print(f"   ✓ 最后启动时间: {record['last_boot_time']}")
    
    # 获取信息
    print("\n4. 获取硬件信息...")
    serial = logger.get_serial_number()
    boot_count = logger.get_boot_count()
    print(f"   ✓ 序列号: {serial}")
    print(f"   ✓ 总启动次数: {boot_count}")
    
    # 上传到后台（模拟）
    print("\n5. 上传到后台（模拟）...")
    logger.upload_to_backend()


if __name__ == "__main__":
    demo_hardware_logger()
