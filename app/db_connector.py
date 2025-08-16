
import functools
import asyncio
import random
import logging
from tortoise import Tortoise
from tortoise.exceptions import OperationalError
from settings import TORTOISE_ORM
from typing import Callable, Any, Optional, Union

logger = logging.getLogger("db")

def tortoise_tx(
    retries: int = 3,
    base_delay: float = 0.1,
    autoreconnect: bool = True,
    keep_connection: bool = True
) -> Callable:
    """
    增强版数据库事务装饰器，整合了重试和连接管理功能
    
    参数:
        retries: 重试次数 (默认3次)
        base_delay: 基础延迟时间(秒) (默认0.1秒)
        autoreconnect: 是否自动重新连接 (默认True)
        keep_connection: 是否保持长连接 (默认True)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 确保数据库已初始化
            await _ensure_db_initialized(keep_connection)
            
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    last_exception = e
                    if attempt == retries:
                        logger.error(f"Operation failed after {retries} retries: {str(e)}")
                        break
                    
                    # 指数退避 + 随机抖动
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    logger.warning(
                        f"Database operation failed (attempt {attempt + 1}/{retries}), "
                        f"retrying in {delay:.2f}s... Error: {str(e)}"
                    )
                    await asyncio.sleep(delay)
                    
                    # 自动重新连接逻辑
                    if autoreconnect and "Lost connection" in str(e):
                        await _reconnect_db()
                except Exception as e:
                    last_exception = e
                    logger.error(f"Unexpected error in database operation: {str(e)}")
                    raise
            
            if last_exception:
                raise last_exception
            
            raise RuntimeError("Unexpected state in tortoise_tx decorator")
        return wrapper
    return decorator

# 全局状态和管理函数
_init_lock = asyncio.Lock()
_initialized = False
_keep_alive_task: Optional[asyncio.Task] = None

async def _ensure_db_initialized(keep_alive: bool = True) -> None:
    """确保数据库连接已初始化"""
    global _initialized, _keep_alive_task
    async with _init_lock:
        if not _initialized:
            try:
                await Tortoise.init(config=TORTOISE_ORM)
                _initialized = True
                if keep_alive:
                    _keep_alive_task = asyncio.create_task(_keep_alive_job())
                logger.info("Database connection initialized")
            except Exception as e:
                logger.error(f"DB initialization failed: {str(e)}")
                raise

async def _reconnect_db() -> None:
    """重新建立数据库连接"""
    global _initialized
    try:
        await Tortoise.close_connections()
        _initialized = False
        await _ensure_db_initialized()
        logger.info("Database reconnected successfully")
    except Exception as e:
        logger.error(f"Database reconnection failed: {str(e)}")
        raise

async def _keep_alive_job() -> None:
    """保持数据库连接活跃的后台任务"""
    while True:
        try:
            await asyncio.sleep(300)  # 每5分钟心跳一次
            conn = Tortoise.get_connection("default")
            await conn.execute_query("SELECT 1")
            logger.debug("Database keep-alive ping")
        except OperationalError as e:
            logger.warning(f"Keep-alive failed: {str(e)}")
            await _reconnect_db()
        except Exception as e:
            logger.error(f"Unexpected keep-alive error: {str(e)}")
            await asyncio.sleep(60)

async def close_db_connections() -> None:
    """关闭所有数据库连接"""
    global _initialized, _keep_alive_task
    if _initialized:
        if _keep_alive_task and not _keep_alive_task.done():
            _keep_alive_task.cancel()
            try:
                await _keep_alive_task
            except asyncio.CancelledError:
                logger.debug("Keep-alive task cancelled")
        
        await Tortoise.close_connections()
        _initialized = False
        logger.info("All database connections closed")