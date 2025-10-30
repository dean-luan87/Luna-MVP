"""
模块5：联网机制设计（参考 Apple Watch）
实现文件：core/network_connection_strategy.py
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import qrcode
from io import BytesIO


class NetworkConnectionStrategy:
    """
    联网机制设计
    功能：配网流程：支持语音配置 / 扫码 / 蓝牙辅助；预留IoT卡
    """
    
    def __init__(self, config_path="data/network_config.json"):
        self.config_path = config_path
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
    
    def network_connection_strategy(self, method: str = "voice"):
        """
        联网策略主入口
        
        Args:
            method: 配网方式，可选 'voice', 'qr_code', 'bluetooth'
        """
        print("\n" + "=" * 60)
        print("Luna 网络配置")
        print("=" * 60)
        
        if method == "voice":
            self.voice_guided_setup()
        elif method == "qr_code":
            self.qr_code_setup()
        elif method == "bluetooth":
            self.bluetooth_setup()
        else:
            print("不支持的配网方式")
    
    def voice_guided_setup(self):
        """语音引导配网"""
        print("\nLuna: 你好，我们来设置网络连接。")
        print("你可以说'开始配网'或者'使用蓝牙配网'")
        print("\n提示：你也可以打开配套APP，扫描二维码进行快速配网。")
        
        # 引导用户选择
        print("\n请选择配网方式：")
        print("1) 语音配网")
        print("2) 扫描二维码")
        print("3) 蓝牙配网")
        
        choice = input("请输入选项（1-3）: ").strip()
        
        if choice == "1":
            self._voice_input_wifi()
        elif choice == "2":
            self.qr_code_setup()
        elif choice == "3":
            self.bluetooth_setup()
        else:
            print("无效选项，使用默认语音配网")
            self._voice_input_wifi()
    
    def _voice_input_wifi(self):
        """语音输入Wi-Fi信息"""
        print("\n--- 语音配网流程 ---")
        
        # 获取Wi-Fi名称
        print("\nLuna: 请告诉我你要连接的Wi-Fi名称：")
        ssid = input("Wi-Fi名称: ").strip()
        
        if not ssid:
            print("未输入Wi-Fi名称")
            return
        
        # 获取密码
        print("\nLuna: 现在请输入密码，你可以一个字一个字告诉我：")
        password = input("Wi-Fi密码: ").strip()
        
        # 尝试连接
        if self._connect_to_wifi(ssid, password):
            print(f"\n✓ 已连接到: {ssid}")
            self._save_network_config(ssid, password)
        else:
            print("\n✗ 连接失败，请检查Wi-Fi名称和密码")
    
    def qr_code_setup(self):
        """二维码配网"""
        print("\n--- 二维码配网流程 ---")
        print("Luna: 请打开配套APP，扫描以下二维码进行快速配网：")
        
        # 生成配网二维码
        qr_data = {
            "device_id": self._get_device_id(),
            "setup_time": datetime.now().isoformat(),
            "type": "wifi_setup"
        }
        
        self._generate_qr_code(qr_data)
        print("\n请用APP扫描上方二维码")
    
    def bluetooth_setup(self):
        """蓝牙配网（预留接口）"""
        print("\n--- 蓝牙配网流程 ---")
        print("Luna: 蓝牙配网功能正在开发中...")
        print("你可以使用语音配网或扫描二维码的方式配置网络。")
    
    def iot_card_setup(self):
        """IoT卡/eSIM配网（预留接口）"""
        print("\n--- IoT卡配网流程 ---")
        print("Luna: eSIM功能正在开发中...")
        print("目前请使用Wi-Fi或蓝牙方式进行网络配置。")
    
    def _connect_to_wifi(self, ssid: str, password: str) -> bool:
        """
        尝试连接到Wi-Fi（模拟实现）
        
        Args:
            ssid: Wi-Fi名称
            password: Wi-Fi密码
            
        Returns:
            是否连接成功
        """
        # TODO: 实现实际Wi-Fi连接逻辑
        # 这里模拟连接
        print(f"\n正在连接到 {ssid}...")
        import time
        time.sleep(1)
        
        # 模拟连接成功
        return True
    
    def _save_network_config(self, ssid: str, password: str):
        """保存网络配置"""
        config = {
            "ssid": ssid,
            "connected_at": datetime.now().isoformat(),
            "method": "voice"
        }
        
        # 不保存密码明文，只保存加密后的哈希
        import hashlib
        config['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def _get_device_id(self) -> str:
        """获取设备ID"""
        from core.hardware_identity_logger import HardwareIdentityLogger
        logger = HardwareIdentityLogger()
        return logger.get_serial_number() or "unknown_device"
    
    def _generate_qr_code(self, data: dict):
        """生成二维码（模拟）"""
        # TODO: 使用qrcode库生成实际二维码
        qr_data_str = json.dumps(data)
        print("\n【二维码】")
        print("=" * 50)
        print(qr_data_str)
        print("=" * 50)
    
    def get_network_status(self) -> Dict[str, Any]:
        """获取网络状态"""
        status = {
            "connected": False,
            "ssid": None,
            "signal_strength": None,
            "ip_address": None
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                status['connected'] = True
                status['ssid'] = config.get('ssid')
                status['connected_at'] = config.get('connected_at')
        
        return status


def demo_network_strategy():
    """演示联网机制"""
    strategy = NetworkConnectionStrategy()
    
    print("\n请选择配网方式：")
    print("1) 语音配网")
    print("2) 二维码配网")
    print("3) 蓝牙配网")
    print("4) IoT卡配网")
    
    choice = input("请输入选项（1-4）: ").strip()
    
    methods = {
        "1": "voice",
        "2": "qr_code",
        "3": "bluetooth",
        "4": "iot"
    }
    
    method = methods.get(choice, "voice")
    
    if method == "iot":
        strategy.iot_card_setup()
    else:
        strategy.network_connection_strategy(method)


if __name__ == "__main__":
    demo_network_strategy()
