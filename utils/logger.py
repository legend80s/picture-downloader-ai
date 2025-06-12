# import logging

# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     # level=logging.INFO,
#     # defaults={"details": ""},  # 为缺失的字段提供默认值
# )
import sys
from loguru import logger as log

log.remove()

log.add(sys.stdout, level="INFO")  # Log only messages with level "WARNING" or higher.

logger = log
