import asyncio
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import httpx
import requests
from bs4 import BeautifulSoup, Tag
from rich import print
from rich.progress import Progress, TaskID

from utils import ask_ai_for_image_name, extract_filename

# from .logging_config import logging
from .url import get_full_url
from .logger import logger

# logger = logger.getLogger(__name__)


class DownloadResult(NamedTuple):
    img_name: str
    img_url: str
    full_path: Path


async def download(
    img: Tag, index: int, save_dir: str, progress: Progress, url: str
) -> None | DownloadResult:
    img_url = img.get("data-src", img.get("src"))

    # progress.console.print(f"Working on job #{index + 1}...")

    if not img_url:
        logger.warning(f"🚫 #{index + 1} no src found", img)
        return

    img_url = str(img_url)
    img_name = await get_name(img, img_url, progress)

    logger.debug(f"{img_url, img_name}")

    full_path: Path = Path(save_dir) / img_name

    if Path.exists(full_path):
        logger.info(f"{full_path} already exists")
        img_name = gen_uniq_filename(img_name)

    full_path: Path = Path(save_dir) / img_name

    logger.debug(f"📥 {img_url} -> {full_path}")

    img_url = get_full_url(url, img_url)

    img_r = requests.get(img_url)

    with open(full_path, "wb") as f:
        f.write(img_r.content)

    return DownloadResult(img_name, img_url, full_path)


def gen_uniq_filename(filename: str) -> str:
    stem = Path(filename).stem
    suffix = Path(filename).suffix

    return stem + "-" + gen_time() + suffix


def gen_time() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


# @timing()
async def get_name(img: Tag, img_url: str, progress: Progress) -> str:
    img_url = str(img_url)
    filename = extract_filename(img_url)
    img_name = await ask_ai_for_image_name(img, filename, progress) or filename

    # 发送频率过高，请稍后再试.
    # await asyncio.sleep(0.5)

    return img_name


def sleep_gap_factory(*, gap: float, iters: int = 100_0000):
    sleep_gaps = (round(x * gap, 3) for x in range(0, iters))

    async def sleep():
        gap = next(sleep_gaps)
        # print("sleep", gap)
        await asyncio.sleep(gap)

    return sleep


sleep_gap = sleep_gap_factory(gap=0.3)


async def crawl_html(url: str) -> str:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        html = r.text

    # print("HTML:", html)

    return html


async def start(
    url: str,
    selector: str,
    save_dir: str,
    concurrency: int = 1,
) -> list[DownloadResult | None] | None:
    if not url or not selector or not Path(save_dir).exists():
        details = {
            "url": url,
            "selector": selector,
            "save_dir": save_dir,
            "save_dir_exists?": Path(save_dir).exists(),
        }
        logger.error(f"❌ url, imgs selector, and save_dir are required! {details}")
        return

    html = await crawl_html(url)
    soup = BeautifulSoup(html, "html.parser")

    imgs = soup.css.select(selector)

    if len(imgs) == 0:
        logger.warning("No images found.")
        print("Web Page text:", soup.getText(strip=True), sep="\n")

        return

    img_count = len(imgs)
    info = f"Found {img_count} images."
    print(f"{info:^160}\n")

    semaphore = asyncio.Semaphore(concurrency)

    async def worker(
        semaphore: asyncio.Semaphore,
        img: Tag,
        index: int,
        save_dir: str,
        task: TaskID,
        progress: Progress,
        url: str,
    ):
        async with semaphore:
            # start_time = time.perf_counter()
            await sleep_gap()
            # end_time = time.perf_counter()

            # print(f"{(end_time - start_time):.2f} s")

            result = await download(img, index, save_dir, progress, url)

            logger.info(f"Downloaded {index}")
            progress.update(task, advance=1)
            return result

    with Progress() as progress:
        task1 = progress.add_task("⏳ Downloading...", total=img_count)
        tasks = [
            worker(semaphore, img, index, save_dir, task1, progress, url)
            for index, img in enumerate(imgs)
        ]

        print(f"⏳ Executing {len(tasks)} tasks with concurrency {concurrency} 🤹...")

        results = await asyncio.gather(*tasks)

        progress.update(task1, description="🎉 Downloaded")

        return results


if __name__ == "__main__":
    # print(random.uniform(0.0, 1.1))
    # numbers = [round(x * 0.1, 1) for x in range(0, 101)]
    # print(numbers)
    # print((float("inf")))
    print(int(float("inf")))
    # sleep_gap = sleep_gap_factory(0.05)

    # for _ in range(10):
    #     sleep_gap()
