import asyncio
import functools
import time
from typing import Any, Callable


def timing(
    precision: int = 2,
    show_func_name: bool = True,
    customizeLabel: None | Callable[[float], str] = None,
):
    """
    装饰器，用于计算函数的执行时间。

    ## Features
    - 同步和异步函数均可使用。

    :param func: 要装饰的函数
    :param precision: 小数点后精度
    :param show_func_name: 是否显示函数名
    :param label: 自定义标签
    """

    def decorator(func: Callable[..., Any]):
        def print_time(start_time, end_time):
            time = end_time - start_time
            tips = ""

            if customizeLabel is not None:
                tips = customizeLabel(time)
            else:
                time_label = (func.__name__ + " " if show_func_name else "") + "耗时: "

                tips = f"{time_label}{time:.{precision}f} 秒"

            print(tips)

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
