from .url import extract_filename


def test_extract_filename():
    url1 = "https://img.zcool.cn/community/01vttarjy7ow5sdayn6tah3731.jpg?imageMogr2/auto-orient/thumbnail/1280x%3e/sharpen/0.5/quality/100/format/webp"
    url2 = "https://img.zcool.cn/community/foo.png"

    assert extract_filename(url1) == "01vttarjy7ow5sdayn6tah3731.jpg"
    assert extract_filename(url2) == "foo.png"
