import asyncio
from typing import TypedDict

from utils import start as start_download, timing
from utils.logging_config import logging

logger = logging.getLogger(__name__)


class Config(TypedDict):
    url: str
    selector: str
    save_dir: str
    concurrency: int


config: Config = {
    "url": "https://www.zcool.com.cn/work/ZNjIzODY0Njg=.html",
    "selector": "#newContent img",
    "save_dir": r"E:\download-2024-5-8\配图\temp\ai",
    "concurrency": 1,
    # "verbose": True,
}


@timing(label="总耗时 ")
async def main():
    print(f"{' Hello from image-downloader-ai-namer! ':=^100}")

    await start_download(**config)


if __name__ == "__main__":
    asyncio.run(main())
