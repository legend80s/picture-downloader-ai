import argparse
import asyncio
from pathlib import Path
import sys
from typing import TypedDict

import httpx
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


console = Console()

parser = argparse.ArgumentParser()
parser.add_argument(
    "-u", "--url", type=str, required=True, help="想要下载图片的网站链接"
)
parser.add_argument("-s", "--selector", type=str, required=True, help="图片 CSS 选择器")
parser.add_argument("-o", "--output-dir", type=Path, required=True, help="图片保存目录")
parser.add_argument(
    "-c", "--concurrency", type=int, required=False, default=1, help="并发数量"
)
parser.add_argument(
    "--not-use-ai-naming",
    action="store_true",
    # required=False,
    # default=True,
    help="是否使用 AI 命名",
)
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()


@timing(label="总耗时 ")
async def main():
    print(f"{' Hello from image-downloader-ai-namer! ':=^160}")

    verbose = args.verbose
    url = args.url
    selector = args.selector
    save_dir = args.output_dir
    concurrency = args.concurrency

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
    try:
        asyncio.run(main())
    except httpx.ConnectError as e:
        logger.error(f"{e}. {e.request}")
        sys.exit(1)

    # info = f"Found {7} images."
    # print(f"{info:^160}")

    # print(args)
