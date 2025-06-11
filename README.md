# picture-downloader-ai

The Selling point: Use AI as 🖼️ picture namer.

痛点：很多图片下载后名字是随机字符串尤其是中文网站，需要耗费精力命名，本工具利用 AI 命名图片。

## Usage

1. copy .env.example to .env and fill it with your own values.

2. 运行

```bash
# py main.py
uv run main.py --output-dir='E:\download-2024-5-8\配图\temp\ai' --url='https://www.python-httpx.org/' --selector='.md-content img'
```

因为默认使用 Kimi AI 智能命名图片。会增加一些时间，如果不需要可以设置 `--not-use-ai-naming`，而且并发度不能太大（默认 `--concurrency=1`），否则会触发 Kimi 的 rate limit 机制。

## 应用 Features

- [x] 自动从 URL 抓取符合 css 选择器的图片下载到本地。
- [x] 使用 Kimi 智能命名图片（优先从 alt 获取，否则“看图”获取）。
- [ ] 性能优化。两处并行：1. 图片之间 2. AI 命名图片和图片下载并行，下载完毕后再命名。

## 技术 Stack

运行时

- requests
- beautifulsoup4
- httpx
- asyncio
- pydantic
- python-settings
- pytest
- [ ] loguru
- [ ] argparse
- [x] rich

开发时

- [x] uv
- [x] ruff
- [ ] mypy

## TODO

- [x] 优化下载逻辑
- [x] 优化命名逻辑
- [x] 优化并发逻辑。通过 asyncio.gather 结合 asyncio.Semaphore 实现并发控制。
- [ ] 优化性能。AI 命名图片和图片下载并行，下载完毕后再命名。
- [x] 优化日志 logging -> 使用 loguru
- [x] 优化错误处理
- [x] 优化 UI
- [x] 增加测试
- [x] 优化文档
- [ ] ~~能抓取 SPA（Single Page Application） 单页应用网站。不支持 SPA 否则要引入 Selenium，就和这个工具的初衷背道而驰了。~~
- [x] 增加命令行参数
- [x] 增加 .env 配置文件
- [ ] 判断如果已经是单词则不使用 AI 命名
