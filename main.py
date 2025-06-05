import asyncio
import functools
import logging
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

from utils import ask_ai_for_image_name

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # defaults={"details": ""},  # 为缺失的字段提供默认值
)


async def main():
    # print((" Hello from image-downloader-ai-namer! ").center(100, "="))
    print(f"{' Hello from image-downloader-ai-namer! ':=^100}")

    await init(
        url="https://www.zcool.com.cn/work/ZNjIzODY0Njg=.html",
        selector="#newContent img",
        save_dir=r"E:\download-2024-5-8\配图\temp",
    )


def timing(precision=2, show_func_name=False, label=""):
    """
    装饰器，用于计算函数的执行时间。

    ## Features
    - 同步和异步函数均可使用。

    :param func: 要装饰的函数
    :param precision: 小数点后精度
    :param show_func_name: 是否显示函数名
    :param label: 自定义标签
    """

    def decorator(func):
        time_label = label or ((func.__name__ if show_func_name else "") + "耗时: ")

        def print_time(start_time, end_time):
            print(f"{time_label}{end_time - start_time:.{precision}f} 秒")

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            print_time(start_time, end_time)

            return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()

            print_time(start_time, end_time)
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


@timing(label="下载耗时 ")
async def init(url: str, selector: str, save_dir: str):
    if not url or not selector or not Path(save_dir).exists():
        logging.error(
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
        logging.warning("No images found.")
        print(soup.getText(strip=True))

        return

    logging.info(f"found {len(imgs)} images.")

    tasks = [
        asyncio.create_task(download(img, index, save_dir))
        for index, img in enumerate(imgs)
    ]

    logging.info(f"⏳ Executing {len(tasks)} tasks concurrently 🤹...")

    await asyncio.gather(*tasks)

    logging.info("🥳 Done.")


async def download(img: Tag, index: int, save_dir: str) -> None:
    img_url = img.get("data-src", img.get("src"))

    if not img_url:
        logging.warning(f"🚫 #{index + 1} no src found", img)
        return

    img_url = str(img_url)
    img_name = await ask_ai_for_image_name(str(img))
    logging.debug(f"{img_url, img_name}")

    full_path: Path = Path(save_dir) / img_name

    if not Path.exists(full_path):
        img_r = requests.get(img_url)
        with open(full_path, "wb") as f:
            f.write(img_r.content)
        logging.info(f"✅ Downloaded #{index + 1} {img_name}")
    else:
        logging.warning("f❌ {full_path} already exists")


if __name__ == "__main__":
    asyncio.run(main())
