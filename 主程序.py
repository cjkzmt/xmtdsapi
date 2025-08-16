import os
import threading
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import psutil
import GPUtil
import time
import logging
from typing import Optional
from src.task.task import fetch_new_tasks, worker
from src.utils.Ffmpeg import *

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class TaskItem(BaseModel):
    taskname: str
    ScriptId: int
# Global variables
SuccessTask: List[TaskItem] = []  # Successful tasks
FailureTask: List[TaskItem] = []  # Failed tasks
PendingTask: list[TaskItem] = []#待处理任务
ProgressingTask: list[TaskItem] = []#正在处理的任务

# Resource constraints per task
TASK_MEM_PERCENT = 0.01  # 1% memory per task
TASK_GPU_MEMORY_MB = 10  # 10MB GPU memory per task

# Thread control
SHUTDOWN = threading.Event()
executor: Optional[ThreadPoolExecutor] = None
NO_MORE_TASKS = threading.Event()  # Flag to indicate no more tasks available

class TaskResourceMetrics(BaseModel):
    cpu_usage: float
    mem_usage: float
    gpu_memory_used: float

def get_system_resources() -> TaskResourceMetrics:
    """Get current system resource usage"""
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    
    try:
        gpus = GPUtil.getGPUs()
        gpu_memory_used = sum(gpu.memoryUsed for gpu in gpus) if gpus else 0
    except Exception as e:
        logger.warning(f"Could not get GPU info: {e}")
        gpu_memory_used = 0
    
    return TaskResourceMetrics(
        cpu_usage=cpu_usage,
        mem_usage=mem_usage,
        gpu_memory_used=gpu_memory_used
    )

def calculate_optimal_task_count() -> int:
    """Calculate the optimal number of tasks based on system resources"""
    resources = get_system_resources()
    
    # CPU constraints
    max_task_num = max(1, os.cpu_count() - 1)
    min_task_num = max(1, os.cpu_count() // 2)
    
    # Memory constraints
    available_mem = 100 - resources.mem_usage
    mem_constrained_tasks = int(available_mem / (TASK_MEM_PERCENT * 100))
    
    # GPU constraints (if available)
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            available_gpu_mem = sum(gpu.memoryFree for gpu in gpus)
            gpu_constrained_tasks = int(available_gpu_mem / TASK_GPU_MEMORY_MB)
            max_task_num = min(max_task_num, gpu_constrained_tasks)
    except Exception as e:
        logger.warning(f"GPU constraint calculation skipped: {e}")
    
    # Final task count
    task_num = min(max_task_num, mem_constrained_tasks)
    task_num = max(min_task_num, task_num)
    
  
    return task_num,resources.cpu_usage,resources.mem_usage,resources.gpu_memory_used,mem_constrained_tasks
def task_callback(future):
    """Callback for completed tasks"""
    result,task_id  = future.result()
    if result:
        SuccessTask.append(task_id)
    else:
        FailureTask.append(task_id)
    ProgressingTask.remove(task_id)
    
    #logger.info(f"任务 {task_id} {'succeeded' if result else 'failed'}")
    
    # Check if we should shutdown after completing all tasks
    if NO_MORE_TASKS.is_set() and not PendingTask and not ProgressingTask:
        SHUTDOWN.set()
        logger.info(f"所有任务成功: {len(SuccessTask)},失败:{len(FailureTask)}已完成，准备关闭")
    # logger.info(
    #         f"任务状态 - \n成功: {len(SuccessTask)}, "
    #         f"\n失败:{len(FailureTask)} 个：{FailureTask}, "
    #         f"\n进行中:{len(ProgressingTask)}个：{ProgressingTask}, "
    #         f"\n等待中: {len(PendingTask)}"
    #         )

def main():
    global executor, PendingTask, ProgressingTask
    
    
    executor = ThreadPoolExecutor(max_workers=os.cpu_count())
    
    try:
        while not SHUTDOWN.is_set():
            max_tasks,cpu_usage,mem_usage,gpu_memory_used,mem_constrained_tasks = calculate_optimal_task_count()
            
            # Log current task status
            
            
            # Fetch new tasks if needed and we haven't been told to stop
            if not NO_MORE_TASKS.is_set() and len(PendingTask) + len(ProgressingTask) < max_tasks:
                tasks_needed = max_tasks - (len(PendingTask) + len(ProgressingTask))
                logger.info(
                    f"系统状态 - CPU: {cpu_usage}%, "
                    f"内存: {mem_usage}%, "
                    f"显存: {gpu_memory_used}MB. "
                    f"可执行任务数: {max_tasks} (可用线程: {os.cpu_count()}, "
                    f"可用内存: {mem_constrained_tasks})"
                    f"正在获取 {tasks_needed} 个新任务（容量充足）"
                )
                
                new_tasks = fetch_new_tasks(tasks_needed)
                print(f"需要{tasks_needed}个，获得 {len(new_tasks)} 新任务已加入待处理队列")
                if new_tasks:
                    PendingTask.extend(new_tasks)
                    # logger.info(f"添加 {len(new_tasks)} 新任务已加入待处理队列")
                else:
                    logger.info("没有更多新任务，将完成当前任务后退出")
                    NO_MORE_TASKS.set()

            # Process pending tasks if resources available
            
            while PendingTask and len(ProgressingTask) < max_tasks:
                task_id = PendingTask.pop(0)
                if task_id['taskname'] == 'Video':
                    video_running = any(t['taskname'] == 'Video' for t in ProgressingTask)
                    if video_running:
                        PendingTask.insert(0, task_id)
                        continue
                ProgressingTask.append(task_id)
                future = executor.submit(worker, task_id)
                future.add_done_callback(task_callback)
                # logger.info(f"启动任务 {task_id}")
            
            # Sleep if no tasks are being processed
            if not ProgressingTask:
                if NO_MORE_TASKS.is_set():
                    logger.info("没有更多任务需要处理，准备关闭")
                    SHUTDOWN.set()
                else:
                    logger.info("暂无任务待处理，等待中……")
                    time.sleep(5)
            else:
                time.sleep(1)
                
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        SHUTDOWN.set()
    finally:
        if executor:
            executor.shutdown(wait=True)
        logger.info("任务处理器已完全关闭")

if __name__ == '__main__':
    GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
    if not GPU_SUPPORTED: print("注意：将使用CPU模式运行...")
    try:
        main()
    except KeyboardInterrupt:
        SHUTDOWN.set()
        logger.info('Received Ctrl-C, shutting down gracefully...')
        if executor:
            executor.shutdown(wait=True)