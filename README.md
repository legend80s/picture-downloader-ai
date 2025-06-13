# picture-downloader-ai

The Selling point: Use AI as 🖼️ picture namer.

痛点：很多图片下载后名字是随机字符串尤其是中文网站，需要耗费精力命名，本工具利用 AI 命名图片。

## Usage

1. copy .env.example to .env and fill it with your own values.

2. 运行

```bash
# py main.py
uv run main.py --output-dir='E:\download-2024-5-8\配图\temp\ai' --url='https://www.python-httpx.org/' --selector='.md-content img'

# 更多用法
uv run main.py --help
```

> [!NOTE]
> 因为默认使用 Kimi AI 智能命名图片，会显著增加时间，如果不需要可设置 `--not-ai-naming`，而且并发度不能太大（默认 `--concurrency=1`），否则会触发 Kimi 的 rate limiting 机制。
>
> 故英文网站或不需要智能命名，可设置 `--not-ai-naming` 并设置更大的并发度。

## 性能

图片 6 张并发度 1，耗时 6.9s，并发度 5 耗时仅 2.77s。

## 应用 Features

- [x] 自动从 URL 抓取符合 css 选择器的图片下载到本地。
- [x] 使用 Kimi 智能命名图片（优先从 alt 获取，否则“看图”获取）。
- [ ] 性能优化。两处并行：1. 图片之间 2. AI 命名图片和图片下载并行，下载完毕后再命名。

## 技术 Features

- 使用 `httpx` 替代 `requests`，支持异步下载。
- 使用 `pydantic` 替代 `dataclass`，支持数据校验。
- 敏感信息使用环境变量文件 .env 存储
- 使用 `pydantic-settings` 获取环境变量。
- 使用 `pytest` 替代 `unittest`，支持单元测试。
- 使用 `loguru` 替代 `logging`，支持日志记录。
- 使用 `rich` 替代 `print`，支持彩色输出。
- 使用 `typer` 替代 `argparse`，支持命令行参数配置。
- 使用最新的 “=: 海象赋值操作符” walrus operator 简化代码。
- 使用 dataclass 避免繁琐的 `__init__` 函数。
- 使用 dataclass 存储命令行参数，解决参数需要在多个函数中传递的问题。

## 技术 Stack

运行时

- requests
- beautifulsoup4
- httpx
- asyncio
- pydantic
- python-settings
- pytest
- loguru
- [ ] argparse
- [x] rich
- [x] typer
- [ ] click
- [ ] fire

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
- [x] 增加命令行参数，变成 CLI APP
- [x] 增加 .env 配置文件
- [ ] 判断如果已经是单词则不使用 AI 命名
- [ ] 单个图片下载失败后续图片不受影响
- [ ] 增加 e2e 测试
- [ ] 优化进度条
- [ ] count：下载的图片数量。默认全部
