# import argparse
import asyncio
import sys
from typing import TypedDict

import httpx
import requests
import typer
from loguru import logger
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from utils import timing, CLIArgs, get_args, set_args, start as start_download

# from utils.logging_config import logging

# logger = logging.getLogger(__name__)


class Config(TypedDict):
    url: str
    selector: str
    save_dir: str
    concurrency: int
    verbose: bool


console = Console()

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "-u", "--url", type=str, required=True, help="想要下载图片的网站链接"
# )
# parser.add_argument("-s", "--selector", type=str, required=True, help="图片 CSS 选择器")
# parser.add_argument("-o", "--output-dir", type=Path, required=True, help="图片保存目录")
# parser.add_argument(
#     "-c", "--concurrency", type=int, required=False, default=1, help="并发数量"
# )
# parser.add_argument(
#     "--use-ai-naming",
#     action="store_true",
#     # required=False,
#     # default=True,
#     help="是否使用 AI 命名",
# )
# parser.add_argument("-v", "--verbose", action="store_true")

# args = parser.parse_args()


@timing(customizeLabel=lambda time: f"⏱️ 总耗时：{time:.2f} 秒\n")
async def init():
    """
    Downloads pictures from a website using a CSS selector and generates names for them using AI.

    :param url: The URL of the website to download pictures from.
    :param selector: The CSS selector to use to find pictures on the website.
    :param output_dir: The directory to save the downloaded pictures to.
    :param verbose: Whether to print verbose output.
    :param concurrency: The number of concurrent downloads to use.
    """

    print(f"\n{'[purple] Hello from picture-downloader-ai-namer [/purple]':-^160}\n")

    args = get_args()

    verbose = args.verbose
    url = args.url
    selector = args.selector
    output_dir = args.output_dir
    concurrency = args.concurrency

    if verbose:
        print(
            f"🔍 将从页面 {url!r} 抓取符合 {selector!r} 的图片，保存到 {output_dir!r} 目录下，并发数为 {concurrency}"
        )

    result = await start_download()

    if result is None:
        # logger.error("🤔 没有找到任何图片")
        return

    list = [item.img_name for item in result if item is not None]

    print(f"\nPicture list ({len(list)}):")
    for name in list:
        print(f"[green]- {name}[/green]")
    print()

    logger.success("🎉 All Done.")


def main(
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-u",
            help="The URL of the website to download pictures from.",
        ),
    ],
    selector: Annotated[
        str,
        typer.Option(
            "--selector",
            "-s",
            help="The CSS selector to use to find pictures on the website.",
        ),
    ],
    output_dir: Annotated[
        str,
        typer.Option(
            "--output-dir",
            "-o",
            help="The directory to save the downloaded pictures to.",
        ),
    ],
    verbose: Annotated[
        bool, typer.Option(help="Whether to print verbose output.")
    ] = False,
    concurrency: Annotated[
        int,
        typer.Option(
            "--concurrency",
            "-c",
            help="The number of concurrent downloads to perform.",
            min=1,
            max=100,
        ),
    ] = 1,
    ai_naming: Annotated[
        bool,
        typer.Option(
            help="Whether to use AI to name the pictures. AI is slow if `--no-ai-naming` set the downloading will be faster and you can set higher concurrency"
        ),
    ] = True,
    count: Annotated[
        int | None,
        typer.Option(
            "--count",
            help="The number of pictures to download.",
            min=1,
            max=100,
        ),
    ] = None,
):
    args = CLIArgs(
        url=url,
        selector=selector,
        output_dir=output_dir,
        verbose=verbose,
        concurrency=concurrency,
        count=count,
        ai_naming=ai_naming,
    )
    set_args(args)

    if verbose:
        print(
            {
                "url": url,
                "selector": selector,
                "output_dir": output_dir,
                "verbose": verbose,
                "concurrency": concurrency,
                "ai_naming": ai_naming,
            }
        )

    coroutine = init()

    try:
        asyncio.run(coroutine)
    except httpx.ConnectError as httpConnectError:
        logger.error(f"{httpConnectError.request} failed: {httpConnectError}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as connectionError:
        logger.error(
            f"{f'{connectionError.request.method} {connectionError.request.url}' if connectionError.request else connectionError.request} failed: {connectionError}"
        )
        sys.exit(1)
    except httpx.ReadTimeout as ReadTimeoutError:
        logger.error(f"{ReadTimeoutError.request} timeout: {ReadTimeoutError}")
        sys.exit(1)
    except Exception as exception:
        logger.error(f"An error occurred: {exception}")
        sys.exit(1)


if __name__ == "__main__":
    # print(f"\n{'[purple] Hello from picture-downloader-ai-namer [/purple]':-^160}\n")

    # print(args)

    typer.run(main)

    # from rich import print

    # data = {
    #     "name": "Alice",
    #     "age": 30,
    #     "address": {"street": "123 Main St", "city": "Wonderland"},
    #     "hobbies": ["reading", "traveling", "coding"],
    # }

    # print(data, sep="\n")

# try:
#     asyncio.run(main())
# except httpx.ConnectError as e:
#     logger.error(f"{e.request} failed: {e}")
#     sys.exit(1)
# except requests.exceptions.ConnectionError as e:
#     logger.error(
#         f"{f'{e.request.method} {e.request.url}' if e.request else e.request} failed: {e}"
#     )
#     sys.exit(1)
# except httpx.ReadTimeout as e:
#     logger.error(f"{e.request} timeout: {e}")
#     sys.exit(1)

# info = f"Found {7} pictures."
# print(f"{info:^160}")
