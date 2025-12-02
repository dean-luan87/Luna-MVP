# core/task/task_engine.py

from typing import Optional, List


class TaskContext:
    """
    任务上下文：管理单个任务的状态和任务链
    """
    
    def __init__(self, task_id, task_type, chain):
        self.task_id = task_id
        self.task_type = task_type  # MAIN / INSERT / SWITCH / FORCE
        self.chain = chain
        self.state = "IDLE"  # IDLE / RUNNING / PAUSED / COMPLETED / CANCELLED
    
    def start(self):
        self.state = "RUNNING"
        if self.chain:
            self.chain.start()
    
    def pause(self):
        self.state = "PAUSED"
        if self.chain:
            self.chain.pause()
    
    def resume(self):
        self.state = "RUNNING"
        if self.chain:
            self.chain.resume()
    
    def cancel(self):
        self.state = "CANCELLED"
        if self.chain:
            self.chain.cancel()
    
    def complete(self):
        self.state = "COMPLETED"
        if self.chain:
            self.chain.complete()
    
    def is_finished(self):
        return self.state in ("COMPLETED", "CANCELLED")
    
    def __repr__(self):
        return f"TaskContext(id={self.task_id}, type={self.task_type}, state={self.state})"


class TaskEngine:
    """
    任务引擎：管理任务链的状态机（FSM）
    
    核心功能：
    - 主任务管理
    - 插入任务管理（栈结构）
    - 切换任务管理
    - 强制任务管理
    """
    
    def __init__(self, tts=None, map_manager=None):
        self.main_task: Optional[TaskContext] = None
        self.current_task: Optional[TaskContext] = None
        self.stack: List[TaskContext] = []
        self.forced_task: Optional[TaskContext] = None
        self.tts = tts
        self.map_manager = map_manager  # 用于缓存恢复
    
    # ---------- 主任务 ---------- #
    
    def start_main(self, task_id, chain):
        """
        启动主任务
        """
        ctx = TaskContext(task_id, "MAIN", chain)
        self.main_task = ctx
        self.current_task = ctx
        ctx.start()
        print(f"[TaskEngine] Start main task: {task_id}")
    
    # ---------- 插入任务（INSERT） ---------- #
    
    def insert_task(self, task_id, chain):
        """
        插入任务：暂停当前任务，执行插入任务，完成后恢复
        """
        if self.current_task:
            # 暂停当前任务并压栈
            self.current_task.pause()
            self.stack.append(self.current_task)
            print(f"[TaskEngine] Pause current task and push to stack: {self.current_task.task_id}")
        
        ctx = TaskContext(task_id, "INSERT", chain)
        self.current_task = ctx
        ctx.start()
        print(f"[TaskEngine] Insert task started: {task_id}")
    
    # ---------- 切换任务（SWITCH） ---------- #
    
    def switch_to(self, task_id, chain):
        """
        切换任务：放弃当前主线与插入栈，启动新的主任务
        """
        # 放弃当前主线与插入栈
        if self.main_task:
            self.main_task.cancel()
            print(f"[TaskEngine] Cancel main task: {self.main_task.task_id}")
        
        for ctx in self.stack:
            ctx.cancel()
            print(f"[TaskEngine] Cancel stacked task: {ctx.task_id}")
        
        self.stack.clear()
        
        # 启动新的主任务
        ctx = TaskContext(task_id, "MAIN", chain)
        self.main_task = ctx
        self.current_task = ctx
        ctx.start()
        print(f"[TaskEngine] Switch to new main task: {task_id}")
    
    # ---------- 强制任务（FORCE） ---------- #
    
    def force_start(self, task_id, chain):
        """
        强制任务：暂停当前任务（但不清栈），执行强制任务
        """
        # 若已有强制任务在执行，则忽略
        if self.forced_task:
            print(f"[TaskEngine] Force task already running: {self.forced_task.task_id}")
            return
        
        # 暂停当前任务（但不清栈）
        if self.current_task:
            self.current_task.pause()
            print(f"[TaskEngine] Pause current task for force task: {self.current_task.task_id}")
        
        ctx = TaskContext(task_id, "FORCE", chain)
        self.forced_task = ctx
        self.current_task = ctx
        ctx.start()
        print(f"[TaskEngine] Force task started: {task_id}")
    
    def end_force_task(self):
        """
        结束强制任务：恢复之前暂停的任务
        """
        if not self.forced_task:
            return
        
        self.forced_task.complete()
        print(f"[TaskEngine] Force task completed: {self.forced_task.task_id}")
        self.forced_task = None
        
        # 结束后不直接恢复，交给上层（或用户）决定
        # 这里只提供一个简单方案：自动恢复
        if self.stack:
            # 如果之前是插入链路中的某一层
            self.current_task = self.stack[-1]
            self.current_task.resume()
            print(f"[TaskEngine] Resume stacked task: {self.current_task.task_id}")
        elif self.main_task and self.main_task.state == "PAUSED":
            self.current_task = self.main_task
            self.current_task.resume()
            print(f"[TaskEngine] Resume main task: {self.main_task.task_id}")
    
    # ---------- 任务结束回调 ---------- #
    
    def on_task_completed(self, task_ctx: TaskContext):
        """
        任务完成回调：根据任务类型处理恢复逻辑
        """
        task_ctx.complete()
        print(f"[TaskEngine] Task completed: {task_ctx.task_id} (type={task_ctx.task_type})")
        
        if task_ctx.task_type == "INSERT":
            # 插入任务结束，恢复上一个任务
            if self.stack:
                prev = self.stack.pop()
                self.current_task = prev
                prev.resume()
                print(f"[TaskEngine] Resume previous task: {prev.task_id}")
            else:
                self.current_task = self.main_task
                if self.main_task:
                    self.main_task.resume()
                    print(f"[TaskEngine] Resume main task: {self.main_task.task_id}")
        
        elif task_ctx.task_type in ("MAIN", "SWITCH"):
            # 主任务结束 → 当前无任务
            self.current_task = None
            print(f"[TaskEngine] Main task completed, no current task")
        
        elif task_ctx.task_type == "FORCE":
            self.end_force_task()
    
    # ---------- 状态查询 ---------- #
    
    def get_status(self):
        """
        获取当前任务引擎状态（用于调试）
        """
        return {
            "main_task": str(self.main_task) if self.main_task else None,
            "current_task": str(self.current_task) if self.current_task else None,
            "stack_size": len(self.stack),
            "stacked_tasks": [str(ctx) for ctx in self.stack],
            "forced_task": str(self.forced_task) if self.forced_task else None,
        }
    
    # ---------- 任务恢复 ---------- #
    
    def try_restore(self, cache: dict):
        """
        从缓存恢复任务状态
        
        参数：
        - cache: 从 TaskCacheManager.load() 获取的缓存数据
        """
        if not cache:
            return False
        
        try:
            # 恢复主任务
            if cache.get("main_task"):
                ctx = self._restore_ctx(cache["main_task"])
                if ctx:
                    self.main_task = ctx
            
            # 恢复 current_task
            if cache.get("current_task"):
                ctx = self._restore_ctx(cache["current_task"])
                if ctx:
                    self.current_task = ctx
            
            # 恢复 stack
            self.stack = []
            for item in cache.get("stack", []):
                ctx = self._restore_ctx(item)
                if ctx:
                    self.stack.append(ctx)
            
            # 恢复 forced_task
            if cache.get("forced_task"):
                ctx = self._restore_ctx(cache["forced_task"])
                if ctx:
                    self.forced_task = ctx
            
            # 恢复地图
            if self.map_manager and "map_scene_id" in cache:
                self.map_manager.scene_id = cache["map_scene_id"]
            
            if self.map_manager and "map_last_node_index" in cache:
                # 截取到指定索引
                last_index = cache["map_last_node_index"]
                if last_index < len(self.map_manager.current_map):
                    self.map_manager.current_map = self.map_manager.current_map[:last_index]
            
            # 对用户播报
            if self.tts:
                self.tts.speak("检测到中断，我已恢复刚才的任务。")
            
            # 恢复当前任务
            if self.current_task:
                self.current_task.resume()
            
            print(f"[TaskEngine] Restored from cache (timestamp: {cache.get('timestamp')})")
            return True
            
        except Exception as e:
            print(f"[TaskEngine] Failed to restore: {e}")
            return False
    
    def _restore_ctx(self, ctx_dict: dict):
        """
        从字典恢复 TaskContext（占位实现）
        
        注意：实际实现需要根据任务链类型创建对应的 TaskChain 对象
        """
        if not ctx_dict:
            return None
        
        # 这里需要根据 task_id 创建对应的 TaskChain
        # 当前为占位实现
        from core.task.task_chain import TaskChain
        
        task_id = ctx_dict.get("task_id", "unknown")
        task_type = ctx_dict.get("task_type", "MAIN")
        state = ctx_dict.get("state", "IDLE")
        
        # 创建任务链（占位）
        chain = TaskChain(task_id)
        if hasattr(chain, 'current_node'):
            chain.current_node = ctx_dict.get("node_index", 0)
        
        ctx = TaskContext(task_id, task_type, chain)
        ctx.state = state  # 直接设置状态
        
        return ctx

