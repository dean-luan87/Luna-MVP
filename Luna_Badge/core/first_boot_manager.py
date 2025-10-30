"""
模块2：首次开机流程（新建/继承账号）
实现文件：core/first_boot_manager.py
"""
import os
import time
import json
from datetime import datetime
from typing import Optional
from core.whisper_recognizer import get_whisper_recognizer
from core.tts_manager import speak


class FirstBootManager:
    """
    首次开机管理模块
    功能：判断是否首次开机，进入初始化流程
    """
    
    def __init__(self, flag_path="data/initialized.flag"):
        self.flag_path = flag_path
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.flag_path), exist_ok=True)
    
    def first_boot_check(self) -> bool:
        """
        判断是否首次开机：检测标志文件
        
        Returns:
            True表示首次开机，False表示已初始化
        """
        return not os.path.exists(self.flag_path)
    
    def mark_device_initialized(self):
        """标记设备已初始化，防止重复引导"""
        try:
            with open(self.flag_path, 'w', encoding='utf-8') as f:
                f.write(f"initialized_at: {datetime.now().isoformat()}\n")
            return True
        except Exception as e:
            print(f"标记初始化失败: {e}")
            return False
    
    def get_initialization_time(self) -> Optional[str]:
        """
        获取设备初始化时间
        
        Returns:
            初始化时间字符串，如果未初始化则返回None
        """
        if not os.path.exists(self.flag_path):
            return None
        
        try:
            with open(self.flag_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取时间戳
                for line in content.split('\n'):
                    if line.startswith('initialized_at:'):
                        return line.split(':', 1)[1].strip()
        except Exception as e:
            print(f"读取初始化时间失败: {e}")
        
        return None


class AccountSetupFlow:
    """
    账号设置流程模块
    功能：创建新账号 / 继承老账号
    支持语音引导配网/扫码配对等机制
    """
    
    def __init__(self, account_path="data/user_profile.json"):
        self.account_path = account_path
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.account_path), exist_ok=True)
    
    def account_setup_flow(self, use_voice_input: bool = False) -> Optional[str]:
        """
        启动初始化流程：提示创建或继承账号
        需后续接入语音或触摸输入方式
        
        Args:
            use_voice_input: 是否使用语音输入
            
        Returns:
            账号ID，如果设置失败则返回None
        """
        print("=" * 50)
        print("欢迎使用Luna智能导航助手")
        print("=" * 50)
        
        if use_voice_input:
            speak("请选择：说创建新账号或登录已有账号")
            print("等待语音输入...")
            
            # 使用Whisper识别
            whisper = get_whisper_recognizer(model_name="base")
            user_input, _ = whisper.recognize_from_microphone(duration=5)
            print(f"您说的是: {user_input}")
        else:
            print("请选择：")
            print("1) 创建新账号")
            print("2) 登录已有账号")
            user_input = input("请输入选项：")
        
        if user_input in ["1", "创建新账号"] or "创建" in user_input:
            # 创建新账号
            account_id = self._create_new_account()
            if account_id:
                print(f"✓ 账号创建成功：{account_id}")
                return account_id
        elif user_input in ["2", "登录已有账号"]:
            # 登录已有账号
            account_id = self._login_existing_account(use_voice_input)
            if account_id:
                print(f"✓ 账号登录成功：{account_id}")
                return account_id
        else:
            print("✗ 输入无效，请重试")
        
        return None
    
    def _create_new_account(self) -> Optional[str]:
        """创建新账号"""
        try:
            account_id = "user_" + str(int(time.time()))
            account_data = {
                "account_id": account_id,
                "created_at": datetime.now().isoformat(),
                "account_type": "new",
                "profile": {
                    "name": "",
                    "preferences": {}
                }
            }
            
            # 保存账号信息
            with open(self.account_path, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, indent=2, ensure_ascii=False)
            
            return account_id
        except Exception as e:
            print(f"创建账号失败: {e}")
            return None
    
    def _login_existing_account(self, use_voice_input: bool = False) -> Optional[str]:
        """登录已有账号"""
        if use_voice_input:
            speak("请说出您的账号ID")
            print("等待语音输入...")
            
            # 使用Whisper识别
            whisper = get_whisper_recognizer(model_name="base")
            account_id, _ = whisper.recognize_from_microphone(duration=5)
            print(f"您说的是: {account_id}")
        else:
            account_id = input("请输入原账号ID：")
        
        if not account_id:
            return None
        
        # 验证账号（这里可以接入后台验证）
        account_data = {
            "account_id": account_id,
            "logged_in_at": datetime.now().isoformat(),
            "account_type": "existing",
            "profile": {}
        }
        
        # 保存账号信息
        try:
            with open(self.account_path, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, indent=2, ensure_ascii=False)
            
            return account_id
        except Exception as e:
            print(f"登录账号失败: {e}")
            return None
    
    def _wait_for_voice_input(self) -> str:
        """等待语音输入（保留兼容接口）"""
        # 已经集成了Whisper，此方法保留为兼容接口
        whisper = get_whisper_recognizer(model_name="base")
        text, _ = whisper.recognize_from_microphone(duration=5)
        return text
    
    def load_account_info(self) -> Optional[dict]:
        """
        加载当前账号信息
        
        Returns:
            账号信息字典，如果未登录则返回None
        """
        if not os.path.exists(self.account_path):
            return None
        
        try:
            with open(self.account_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载账号信息失败: {e}")
            return None


# 集成函数
def run_first_boot_flow() -> Optional[str]:
    """
    运行首次开机完整流程
    
    Returns:
        账号ID，如果流程失败则返回None
    """
    boot_manager = FirstBootManager()
    account_setup = AccountSetupFlow()
    
    # 检查是否首次开机
    if boot_manager.first_boot_check():
        print("\n检测到首次开机，进入初始化流程...\n")
        
        # 运行账号设置流程
        account_id = account_setup.account_setup_flow(use_voice_input=False)
        
        if account_id:
            # 标记设备已初始化
            boot_manager.mark_device_initialized()
            print("\n✓ 设备初始化完成！")
            return account_id
        else:
            print("\n✗ 初始化失败，请重试")
            return None
    else:
        init_time = boot_manager.get_initialization_time()
        print(f"设备已在 {init_time} 完成初始化")
        
        # 加载已有账号
        account_info = account_setup.load_account_info()
        if account_info:
            return account_info.get("account_id")
    
    return None
