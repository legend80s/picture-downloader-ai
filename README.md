# picture-downloader-ai

The Selling point: Use AI as 🖼️ picture namer.

痛点：很多图片下载后名字是随机字符串尤其是中文网站，需要耗费精力命名，本工具利用 AI 命名图片。

## Usage

1. copy .env.example to .env and fill it with your own values.

2. 运行

```bash
# uv run main.py
py main.py --url='https://juejin.cn/' --selector='.content-wrapper img' --output-dir='E:\download-2024-5-8\配图\temp\ai' 
```

因为默认使用 Kimi AI 智能命名图片。会增加一些时间，如果不需要可以设置 `--not-use-ai-naming`，而且并发度不能太大（默认 `--concurrency=1`），否则会触发 Kimi 的 rate limit 机制。

## 应用 Features

- [x] 自动从 URL 抓取符合 css 选择器的图片下载到本地
- [x] 使用 Kimi 智能命名图片（优先从 alt 获取，否则“看图”获取）

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

- [ ] 优化下载逻辑
- [ ] 优化命名逻辑
- [ ] 优化并发逻辑
- [ ] 优化日志
- [ ] 优化错误处理
- [ ] 优化 UI
- [ ] 优化测试
- [ ] 优化文档
