#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 记忆收集器
汇总每日缓存目录用于打包上传
"""

import json
import logging
import tarfile
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class MemoryCollector:
    """记忆收集器"""
    
    def __init__(self,
                 local_memory_dir: str = "memory_store/local_memory",
                 uploaded_flags_dir: str = "memory_store/uploaded_flags"):
        """初始化收集器
        
        Args:
            local_memory_dir: 本地记忆目录
            uploaded_flags_dir: 已上传标记目录
        """
        self.local_memory_dir = Path(local_memory_dir)
        self.uploaded_flags_dir = Path(uploaded_flags_dir)
        self.uploaded_flags_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("📦 记忆收集器初始化完成")
    
    def collect_pending_memories(self, date: Optional[str] = None) -> List[Dict]:
        """收集待上传的记忆
        
        Args:
            date: 指定日期（默认为昨天，T+1机制）
            
        Returns:
            待上传的记忆列表
        """
        # T+1机制：默认收集昨天的数据
        if not date:
            yesterday = datetime.now() - timedelta(days=1)
            date = yesterday.strftime("%Y-%m-%d")
        
        # 获取所有未上传的记忆文件
        pending_files = []
        
        for memory_file in self.local_memory_dir.glob("*_memory.json"):
            # 检查是否已上传
            if self._is_uploaded(memory_file):
                continue
            
            # 检查日期匹配
            if date in memory_file.name:
                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        memory_data = json.load(f)
                    
                    pending_files.append({
                        "file": memory_file,
                        "data": memory_data,
                        "size": memory_file.stat().st_size
                    })
                except Exception as e:
                    logger.error(f"❌ 读取记忆文件失败 {memory_file}: {e}")
        
        logger.info(f"📋 收集到 {len(pending_files)} 个待上传记忆")
        return pending_files
    
    def _is_uploaded(self, memory_file: Path) -> bool:
        """检查记忆文件是否已上传
        
        Args:
            memory_file: 记忆文件路径
            
        Returns:
            是否已上传
        """
        # 生成标记文件名
        flag_filename = memory_file.stem.replace("_memory", "") + ".uploaded"
        flag_file = self.uploaded_flags_dir / flag_filename
        
        return flag_file.exists()
    
    def mark_as_uploaded(self, memory_file: Path):
        """标记记忆文件为已上传
        
        Args:
            memory_file: 记忆文件路径
        """
        # 生成标记文件
        flag_filename = memory_file.stem.replace("_memory", "") + ".uploaded"
        flag_file = self.uploaded_flags_dir / flag_filename
        
        with open(flag_file, 'w') as f:
            f.write(datetime.now().isoformat())
        
        logger.info(f"✅ 已标记为已上传：{memory_file.name}")
    
    def create_upload_package(self, memories: List[Dict], compress: bool = True) -> Path:
        """创建上传数据包
        
        Args:
            memories: 记忆列表
            compress: 是否压缩
            
        Returns:
            数据包文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_dir = Path("memory_store/packages")
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # 组合所有记忆数据
        package_data = {
            "timestamp": timestamp,
            "uploaded_at": datetime.now().isoformat(),
            "memories": [m["data"] for m in memories],
            "metadata": {
                "total_files": len(memories),
                "total_size_bytes": sum(m["size"] for m in memories)
            }
        }
        
        # 保存为JSON
        json_file = package_dir / f"memory_package_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, ensure_ascii=False, indent=2)
        
        if compress:
            # 压缩文件
            gz_file = package_dir / f"memory_package_{timestamp}.json.gz"
            with open(json_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            # 删除未压缩文件
            json_file.unlink()
            
            logger.info(f"✅ 数据包已创建（压缩）：{gz_file.name}")
            return gz_file
        else:
            logger.info(f"✅ 数据包已创建：{json_file.name}")
            return json_file
    
    def get_statistics(self) -> Dict:
        """获取统计信息
        
        Returns:
            统计信息字典
        """
        total_files = len(list(self.local_memory_dir.glob("*_memory.json")))
        uploaded_files = sum(1 for f in self.local_memory_dir.glob("*_memory.json") 
                           if self._is_uploaded(f))
        pending_files = total_files - uploaded_files
        
        total_size = sum(f.stat().st_size for f in self.local_memory_dir.glob("*_memory.json"))
        
        return {
            "total_files": total_files,
            "uploaded_files": uploaded_files,
            "pending_files": pending_files,
            "total_size_kb": round(total_size / 1024, 2),
            "uploaded_flags_count": len(list(self.uploaded_flags_dir.glob("*.uploaded")))
        }


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化收集器
    collector = MemoryCollector()
    
    # 显示统计
    print("=" * 60)
    print("📊 记忆统计")
    print("=" * 60)
    stats = collector.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 收集待上传记忆
    print("\n📋 收集待上传记忆")
    print("=" * 60)
    pending = collector.collect_pending_memories()
    print(f"待上传文件数：{len(pending)}")
    
    if pending:
        # 创建上传包
        print("\n📦 创建上传包")
        print("=" * 60)
        package = collector.create_upload_package(pending, compress=True)
        print(f"数据包：{package}")
        
        # 标记为已上传（测试）
        # collector.mark_as_uploaded(pending[0]["file"])


