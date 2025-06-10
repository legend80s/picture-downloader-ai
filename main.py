import asyncio
from typing import TypedDict

from rich import print
from rich.console import Console

from utils import start as start_download
from utils import timing
from utils.logging_config import logging

logger = logging.getLogger(__name__)


class Config(TypedDict):
    url: str
    selector: str
    save_dir: str
    concurrency: int
    verbose: bool


config: Config = {
    "url": "https://www.zcool.com.cn/work/ZNjIzODY0Njg=.html",
    "selector": "#newContent img",
    "save_dir": r"E:\download-2024-5-8\配图\temp\ai",
    "concurrency": 1,
    "verbose": True,
}

console = Console()


@timing(label="总耗时 ")
async def main():
    print(f"{' Hello from image-downloader-ai-namer! ':=^160}")

    verbose = config["verbose"]
    url = config["url"]
    selector = config["selector"]
    save_dir = config["save_dir"]
    concurrency = config["concurrency"]

    if verbose:
        print(
            f"🔍 将从页面 {url!r} 抓取符合 {selector!r} 的图片，保存到 {save_dir!r} 目录下，并发数为 {concurrency}"
        )

    result = await start_download(
        url=url,
        selector=selector,
        save_dir=save_dir,
        concurrency=concurrency,
    )

    if result is not None:
        list = [item.img_name for item in result if item is not None]

        print(f"Picture list ({len(list)}):", list)

    logger.info("🎉 All Done.")


if __name__ == "__main__":
    asyncio.run(main())
    # info = f"Found {7} images."
    # print(f"{info:^160}")
