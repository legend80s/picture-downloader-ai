import asyncio
import functools
import time


def timing(precision=2, show_func_name=True, label=""):
    """
    装饰器，用于计算函数的执行时间。

    ## Features
    - 同步和异步函数均可使用。

    :param func: 要装饰的函数
    :param precision: 小数点后精度
    :param show_func_name: 是否显示函数名
    :param label: 自定义标签
    """

    def decorator(func):
        time_label = label or (
            (func.__name__ + " " if show_func_name else "") + "耗时: "
        )

        def print_time(start_time, end_time):
            print(f"{time_label}{end_time - start_time:.{precision}f} 秒")

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
