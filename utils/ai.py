import json
import textwrap
from http import HTTPMethod
from typing import TypedDict

import bs4
import httpx

from utils.env_settings import get_settings
from utils.logging_config import logging

logger = logging.getLogger(__name__)

settings = get_settings()


class Img(TypedDict):
    alt: str
    src: str
    data_src: str


async def ask_ai_for_image_name(img: bs4.Tag | Img) -> str | None:
    """
    生成图片文件名，如果src本身名称已经具备描述性，则直接使用，否则根据alt生成摘要当做图片文件名，否则请看图取名字。

    :param img: Tag 对象
    :return: 图片文件名

    .. code-block:: python
        img = bs4.BeautifulSoup(<img data-src="https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp" src="https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp" alt="远方有虫鸣鸟叫，我的鸭子、我的小狗。我的你都在身边。" data-expand="2048" class="photoImage lazyloaded" style="white-space:pre-wrap" draggable="false">).css.select_one("img")
        name = ask_ai_for_image_name(img) # => "duck-puppy-me-aside.jpg"
    """

    chat_id = settings.chat_id
    authorization = settings.authorization

    question = textwrap.dedent(f"""
    生成图片文件名，如果src本身名称已经具备描述性，则直接使用，否则根据alt生成摘要当做图片文件名，否则请看图取名字。文件名必须是英文，优先人/动物/物品名称、时间季节、地点等区别于其他图片的标识性独特的词语，比如`alt=塔莎的照片里……花园里种植的是滨菊、牡丹、虞美人`则需要出现“塔莎”、“滨菊、牡丹、虞美人”。文件名不必简短，需要充分描述图片内容，但是不多于12个词，克制使用介词连词等虚词比如with and or，单词小写且用`-`隔开，后缀请从 src 推断。只需输出文件名无需解释。

    ```html
    {img}
    ```
    """).strip()

    name: str = ""

    # logger.info(f"{question=!r}")

    token_stream = read_sse_stream(
        url=f"https://kimi.moonshot.cn/api/chat/{chat_id}/completion/stream",
        method=HTTPMethod.POST,
        headers={
            #           accept: 'application/json, text/plain, */*',
            #           'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            "authorization": authorization,
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            #           priority: 'u=1, i',
            #           'r-timezone': 'Asia/Shanghai',
            #           'sec-ch-ua':
            #           '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            #           'sec-ch-ua-mobile': '?0',
            #           'sec-ch-ua-platform': '"Windows"',
            #           'sec-fetch-dest': 'empty',
            #           'sec-fetch-mode': 'cors',
            #           'sec-fetch-site': 'same-origin',
            # 'x-language': 'zh-CN',
            # 'x-msh-device-id': '7385109661751553547',
            # 'x-msh-platform': 'web',
            # 'x-msh-session-id': '1730303647696008250',
            # 'x-traffic-id': 'cpgib5e768j5a4md3f40',
        },
        # referrer: 'https://kimi.moonshot.cn/chat/cvv094v37oqbghbb8vh0',
        # referrerPolicy: 'strict-origin-when-cross-origin',
        data={
            "kimiplus_id": "kimi",
            "extend": {
                "sidebar": True,
            },
            "model": "kimi",
            "stream": False,
            # 是否联网搜索
            "use_search": False,
            "messages": [
                {
                    "role": "user",
                    "content": question,
                },
            ],
            "refs": [],
            "history": [],
            "scene_labels": [],
        },
        # mode: 'cors',
        # credentials: 'include',
    )

    try:
        async for token in token_stream:
            name += token
    except EnhancedHTTPError as error:
        logger.error(f"🚫 {img=}")

        status_code = error.original_error.response.status_code
        url = error.original_error.request.url
        logger.error(
            f"🚫 Bad Request {status_code} {error.response_text} while requesting {url!r}."
        )

        return None
        # raise error

    except httpx.RequestError as error:
        logger.error(f"❌ {img=}")
        logger.error(
            f"❌ Network error while fetch name from AI: {error.request.url!r}"
        )
        return None

    return name


class EnhancedHTTPError(Exception):
    def __init__(
        self, original_error: httpx.HTTPStatusError, response_bytes: bytes
    ) -> None:
        self.original_error = original_error
        self.response_text = response_bytes.decode("utf-8")
        super().__init__(original_error)


async def read_sse_stream(
    url: str,
    method: HTTPMethod,
    headers: dict | None = None,
    data: dict | None = None,
):
    async with httpx.AsyncClient() as client:
        async with client.stream(method, url, headers=headers, json=data) as response:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                raise EnhancedHTTPError(error, await error.response.aread())

            async for line in response.aiter_lines():
                logger.debug(f"{line=}")
                if line.startswith("data:"):
                    data = json.loads(line[6:])
                    if not data:
                        continue

                    if data["event"] == "cmpl":
                        yield data["text"]
                    if "error" in data:
                        raise Exception(data["error"]["message"])


if __name__ == "__main__":
    print(get_settings())

    async def main():
        # img_tag = bs4.BeautifulSoup(
        #     '<img data-src="https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp" src="https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp" alt="远方有虫鸣鸟叫，我的鸭子、我的小狗。我的你都在身边。" data-expand="2048" class="photoImage lazyloaded" style="white-space:pre-wrap" draggable="false">',
        #     "html.parser",
        # ).css.select_one("img")

        # assert img_tag is not None, "No img tag found in the HTML."

        # name = await ask_ai_for_image_name(img_tag)

        # print(f"{name=}")
        question = textwrap.dedent(f"""
    生成图片文件名，如果src本身名称已经具备描述性，则直接使用，否则根据alt生成摘要当做图片文件名，否则请看图取名字。文件名必须是英文，优先人/动物/物品名称、时间季节、地点等区别于其他图片的标识性独特的词语，比如`alt=塔莎的照片里……花园里种植的是滨菊、牡丹、虞美人`则需要出现“塔莎”、“滨菊、牡丹、虞美人”。文件名不必简短，需要充分描述图片内容，但是不多于12个词，克制使用介词连词等虚词比如with and or，单词小写且用`-`隔开，后缀请从 src 推断。只需输出文件名无需解释。

    ```html
    {"是否第三方第三方斯蒂芬是打发"}
    ```
    """).strip()
        print(question)

    # asyncio.run(main())
