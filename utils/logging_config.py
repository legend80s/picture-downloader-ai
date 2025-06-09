import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # defaults={"details": ""},  # 为缺失的字段提供默认值
)
