from urllib.parse import urlparse
import os


def extract_filename(url):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)  # 自动处理路径和文件名
    return filename
