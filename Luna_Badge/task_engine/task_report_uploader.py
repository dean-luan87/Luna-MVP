#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 执行记录上传模块
将任务运行数据上传至云端后台
"""

import logging
import json
import time
import os
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class TaskReportUploader:
    """任务报告上传器"""
    
    def __init__(self, api_url: str = "https://api.luna.ai/task/report", 
                 max_retries: int = 3, retry_delay: int = 5):
        """
        初始化任务报告上传器
        
        Args:
            api_url: API上传地址
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.api_url = api_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.local_storage = "data/task_reports_pending.json"
        self.logger = logging.getLogger("TaskReportUploader")
        
        # 确保本地存储目录存在
        os.makedirs(os.path.dirname(self.local_storage), exist_ok=True)
    
    def upload_task_report(self, report_data: Dict[str, Any]) -> bool:
        """
        上传任务报告
        
        Args:
            report_data: 报告数据字典，包含以下字段：
                - task_id: 任务ID
                - user_id: 用户ID
                - graph_name: 图谱名称
                - execution_path: 执行链路
                - failed_nodes: 失败节点列表
                - corrections: 修正行为列表
                - duration: 执行时长（秒）
                - status: 最终状态
        
        Returns:
            bool: 是否上传成功
        """
        try:
            # 添加时间戳
            report_data["uploaded_at"] = time.time()
            report_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # 尝试上传
            success = self._do_upload(report_data)
            
            if success:
                self.logger.info(f"✅ 任务报告上传成功: {report_data.get('task_id')}")
                # 上传成功后从待上传列表中移除
                self._remove_from_pending(report_data.get('task_id'))
                return True
            else:
                # 上传失败，保存到本地
                self._save_to_local(report_data)
                self.logger.warning(f"⚠️ 任务报告上传失败，已保存到本地: {report_data.get('task_id')}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ 上传任务报告失败: {e}")
            # 保存到本地作为备份
            self._save_to_local(report_data)
            return False
    
    def _do_upload(self, report_data: Dict[str, Any]) -> bool:
        """执行实际上传"""
        try:
            import requests
            
            # 重试机制
            for attempt in range(self.max_retries):
                try:
                    response = requests.post(
                        self.api_url,
                        json=report_data,
                        timeout=10,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        return True
                    else:
                        self.logger.warning(f"⚠️ 上传失败，状态码: {response.status_code}, 尝试 {attempt + 1}/{self.max_retries}")
                        
                except requests.exceptions.RequestException as e:
                    self.logger.warning(f"⚠️ 上传请求异常: {e}, 尝试 {attempt + 1}/{self.max_retries}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            
            return False
            
        except ImportError:
            self.logger.warning("⚠️ requests库未安装，跳过上传（开发模式）")
            # 开发模式下模拟成功
            return True
        except Exception as e:
            self.logger.error(f"❌ 上传过程异常: {e}")
            return False
    
    def _save_to_local(self, report_data: Dict[str, Any]):
        """保存到本地待上传列表"""
        try:
            pending_reports = self._load_pending_reports()
            
            # 避免重复
            task_id = report_data.get('task_id')
            if task_id:
                pending_reports = [r for r in pending_reports if r.get('task_id') != task_id]
            
            pending_reports.append(report_data)
            
            with open(self.local_storage, 'w', encoding='utf-8') as f:
                json.dump(pending_reports, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"💾 报告已保存到本地: {task_id}")
            
        except Exception as e:
            self.logger.error(f"❌ 保存到本地失败: {e}")
    
    def _load_pending_reports(self) -> List[Dict[str, Any]]:
        """加载待上传报告列表"""
        try:
            if os.path.exists(self.local_storage):
                with open(self.local_storage, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"❌ 加载待上传报告失败: {e}")
            return []
    
    def _remove_from_pending(self, task_id: str):
        """从待上传列表中移除"""
        try:
            pending_reports = self._load_pending_reports()
            pending_reports = [r for r in pending_reports if r.get('task_id') != task_id]
            
            with open(self.local_storage, 'w', encoding='utf-8') as f:
                json.dump(pending_reports, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"🗑️ 已从待上传列表移除: {task_id}")
            
        except Exception as e:
            self.logger.error(f"❌ 移除待上传报告失败: {e}")
    
    def retry_pending_uploads(self) -> int:
        """
        重试上传待上传的报告
        
        Returns:
            int: 成功上传的数量
        """
        pending_reports = self._load_pending_reports()
        success_count = 0
        
        if not pending_reports:
            return 0
        
        self.logger.info(f"🔄 开始重试上传 {len(pending_reports)} 个待上传报告")
        
        for report in pending_reports[:]:  # 复制列表避免修改问题
            if self._do_upload(report):
                success_count += 1
                self._remove_from_pending(report.get('task_id'))
        
        self.logger.info(f"✅ 重试上传完成: {success_count}/{len(pending_reports)} 成功")
        return success_count
    
    def get_pending_count(self) -> int:
        """获取待上传报告数量"""
        return len(self._load_pending_reports())


# 全局上传器实例
_global_uploader: Optional[TaskReportUploader] = None

def get_report_uploader() -> TaskReportUploader:
    """获取全局任务报告上传器实例"""
    global _global_uploader
    if _global_uploader is None:
        _global_uploader = TaskReportUploader()
    return _global_uploader


if __name__ == "__main__":
    # 测试报告上传器
    print("📤 TaskReportUploader测试")
    print("=" * 60)
    
    uploader = get_report_uploader()
    
    # 测试报告数据
    test_report = {
        "task_id": "test_task_001",
        "user_id": "test_user",
        "graph_name": "hospital_visit",
        "execution_path": ["plan_route", "confirm_departure", "execute_navigation"],
        "failed_nodes": [],
        "corrections": [],
        "duration": 1800,
        "status": "completed"
    }
    
    print("\n1. 测试上传报告...")
    success = uploader.upload_task_report(test_report)
    print(f"   上传结果: {'成功' if success else '失败（已保存到本地）'}")
    
    print("\n2. 检查待上传报告...")
    pending_count = uploader.get_pending_count()
    print(f"   待上传数量: {pending_count}")
    
    if pending_count > 0:
        print("\n3. 重试上传...")
        retry_count = uploader.retry_pending_uploads()
        print(f"   成功上传: {retry_count}")
    
    print("\n🎉 TaskReportUploader测试完成！")

