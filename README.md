# picture-downloader-ai

Use AI as 🖼️ picture namer.

## Usage

copy .env.example to .env and fill it with your own values.

```bash
py main.py # uv run main.py
```

## 应用 Features

- [x] 自动从 URL 抓取符合 css 选择器的图片下载到本地
- [x] 使用 kimi 智能命名图片（优先从 alt 获取，否则“看图”获取）

## 技术 Stack

- requests
- beautifulsoup4
- httpx
- asyncio
- pydantic
- python-settings
- pytest
- [ ] loguru
