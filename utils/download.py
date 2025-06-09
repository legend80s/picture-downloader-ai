import asyncio
from datetime import datetime
from pathlib import Path
import random
from bs4 import BeautifulSoup, Tag
import requests
from utils import ask_ai_for_image_name, extract_filename, timing
from .logging_config import logging

logger = logging.getLogger(__name__)


async def download(img: Tag, index: int, save_dir: str) -> None:
    img_url = img.get("data-src", img.get("src"))

    if not img_url:
        logging.warning(f"🚫 #{index + 1} no src found", img)
        return

    img_url = str(img_url)
    img_name = await get_name(img, img_url)

    logging.debug(f"{img_url, img_name}")

    full_path: Path = Path(save_dir) / img_name

    if Path.exists(full_path):
        logging.info(f"{full_path} already exists")
        full_path = Path(save_dir) / gen_uniq_filename(img_name)

    logging.info(f"📥 {img_url} -> {full_path}")
    img_r = requests.get(img_url)

    with open(full_path, "wb") as f:
        f.write(img_r.content)

    logging.info(f"✅ Downloaded #{index + 1} {img_name}")


def gen_uniq_filename(filename: str) -> str:
    return gen_time() + "-" + filename


def gen_time() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


@timing()
async def get_name(img: Tag, img_url: str) -> str:
    img_url = str(img_url)
    img_name = await ask_ai_for_image_name(img) or extract_filename(img_url)

    # 发送频率过高，请稍后再试.
    # await asyncio.sleep(0.5)

    return img_name


async def start(
    url: str,
    selector: str,
    save_dir: str,
    concurrency: int = 1,
    verbose: bool = False,
):
    if verbose:
        print(
            f"🕷️ 将从页面 {url} 抓取符合 {selector} 的图片，保存到 {save_dir} 目录下，并发数为 {concurrency}"
        )

    if not url or not selector or not Path(save_dir).exists():
        logger.error(
            "❌ url, imgs selector, and save_dir are required!"
            + " "
            + str(
                {
                    "url": url,
                    "selector": selector,
                    "save_dir": save_dir,
                    "save_dir_exists?": Path(save_dir).exists(),
                }
            )
        )
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
    logger.info(f"found {img_count} images.")

    semaphore = asyncio.Semaphore(concurrency)

    async def worker(semaphore: asyncio.Semaphore, img: Tag, index: int, save_dir: str):
        async with semaphore:
            await download(img, index, save_dir)

    tasks = [worker(semaphore, img, index, save_dir) for index, img in enumerate(imgs)]

    logger.info(f"⏳ Executing {len(tasks)} tasks with concurrency {concurrency} 🤹...")

    await asyncio.gather(*tasks)

    logger.info("🎉 All Done.")
