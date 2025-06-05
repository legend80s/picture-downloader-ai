import random
import time


async def ask_ai_for_image_name(img: str) -> str:
    return f"test-{time.time()}-{random.randint(1, 1000)}.jpg"
