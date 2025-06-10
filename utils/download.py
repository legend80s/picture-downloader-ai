import asyncio
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup, Tag
from rich import print
from rich.progress import Progress, TaskID

from utils import ask_ai_for_image_name, extract_filename

from .logging_config import logging

logger = logging.getLogger(__name__)


class DownloadResult(NamedTuple):
    img_name: str
    img_url: str
    full_path: Path


async def download(
    img: Tag, index: int, save_dir: str, progress: Progress
) -> None | DownloadResult:
    img_url = img.get("data-src", img.get("src"))

    # progress.console.print(f"Working on job #{index + 1}...")

    if not img_url:
        logging.warning(f"🚫 #{index + 1} no src found", img)
        return

    img_url = str(img_url)
    img_name = await get_name(img, img_url, progress)

    logging.debug(f"{img_url, img_name}")

    full_path: Path = Path(save_dir) / img_name

    if Path.exists(full_path):
        logging.info(f"{full_path} already exists")
        img_name = gen_uniq_filename(img_name)

    full_path: Path = Path(save_dir) / img_name

    logging.debug(f"📥 {img_url} -> {full_path}")
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

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    html = r.text
    # print("HTML:", html)
    soup = BeautifulSoup(html, "html.parser")

    imgs = soup.css.select(selector)

    if len(imgs) == 0:
        logger.warning("No images found.")
        print(soup.getText(strip=True))

        return

    img_count = len(imgs)
    info = f"Found {img_count} images."
    print(f"{info:^160}")

    semaphore = asyncio.Semaphore(concurrency)

    async def worker(
        semaphore: asyncio.Semaphore,
        img: Tag,
        index: int,
        save_dir: str,
        task: TaskID,
        progress: Progress,
    ):
        async with semaphore:
            result = await download(img, index, save_dir, progress)

            logger.info(f"Downloaded {index}")
            progress.update(task, advance=1)
            return result

    with Progress() as progress:
        task1 = progress.add_task("⏳ Downloading...", total=img_count)
        tasks = [
            worker(semaphore, img, index, save_dir, task1, progress)
            for index, img in enumerate(imgs)
        ]

        logger.info(
            f"⏳ Executing {len(tasks)} tasks with concurrency {concurrency} 🤹..."
        )

        results = await asyncio.gather(*tasks)

        progress.update(task1, description="🎉 Downloaded")

        return results
