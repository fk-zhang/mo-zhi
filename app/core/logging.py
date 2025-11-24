from loguru import logger
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 从环境变量获取日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_PATH = os.getenv("LOG_PATH", "./logs/mo-zhi.log")

# 确保日志目录存在
log_dir = Path(LOG_PATH).parent
log_dir.mkdir(parents=True, exist_ok=True)

# 配置 loguru 日志输出到控制台和文件，支持分割、保留、压缩
logger.remove()  # 移除默认 handler

# 文件日志：输出到文件，支持轮转、压缩
logger.add(
    LOG_PATH,
    rotation=os.getenv("LOG_ROTATION", "10 MB"),      # 单文件最大 10MB 自动分割
    retention=os.getenv("LOG_RETENTION", "10 days"),  # 日志保留 10 天
    compression=os.getenv("LOG_COMPRESSION", "zip"),  # 压缩历史日志
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8",
    enqueue=True,           # 多线程/多进程安全
    backtrace=True,         # 记录异常堆栈
    diagnose=True           # 显示异常变量值
)

# 控制台日志：输出到标准输出，支持颜色
# 根据 DEBUG 环境变量决定是否显示调试信息
console_level = "DEBUG" if os.getenv("DEBUG", "false").lower() in ("true", "1", "yes") else LOG_LEVEL
logger.add(
    sink=lambda msg: print(msg, end=""),
    level=console_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
    backtrace=True,
    diagnose=True
)

# ========== 日志桥接：标准 logging 日志全部转发到 loguru ==========
class InterceptHandler(logging.Handler):
    """
    拦截标准 logging 日志，转发到 loguru
    
    这个处理器会将所有标准 logging 的日志记录转发到 loguru，
    确保统一的日志格式和输出。
    """
    def emit(self, record):
        # 获取对应的 loguru 级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            # 如果找不到对应的级别名称，使用数字级别映射
            level_map = {
                50: "CRITICAL",
                40: "ERROR",
                30: "WARNING",
                20: "INFO",
                10: "DEBUG",
                0: "NOTSET"
            }
            level = level_map.get(record.levelno, "INFO")
        
        # 使用 depth=6 来跳过 logging 框架的调用栈，直接定位到实际调用者
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

# 替换标准 logging 的 root handler
logging.root.handlers = [InterceptHandler()]
logging.root.setLevel(LOG_LEVEL)

# 让第三方库日志也走 loguru
# 包括 uvicorn、fastapi、fastmcp、zabbix_utils 等
third_party_loggers = (
    "uvicorn", "uvicorn.error", "uvicorn.access",
    "fastapi", "fastmcp",
    "zabbix_utils", "requests", "urllib3",
    "sqlalchemy", "httpx"
)
for name in third_party_loggers:
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True

# ========== 获取 loguru logger 的统一接口 ==========
def get_logger(name: str = None):
    """
    获取 loguru logger（兼容原有接口，name 参数可选）
    
    Args:
        name: 可选，日志记录器名称，用于标识不同的模块
        
    Returns:
        Logger: loguru logger 实例
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
    """
    if name:
        return logger.bind(name=name)
    return logger


# 导出 logger 以供直接使用
__all__ = ["logger", "get_logger"]