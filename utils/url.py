from urllib.parse import urlparse
import os


def extract_filename(url):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)  # 自动处理路径和文件名
    return filename


if __name__ == "__main__":
    url1 = "https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp"
    url2 = "https://img.zcool.cn/community/foo.png"

    print(extract_filename(url1))  # 01vttarjy7ow5sdayn6tah3731.jpg
    print(extract_filename(url2))  # foo.png
