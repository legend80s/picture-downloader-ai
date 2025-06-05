import asyncio
import functools
import time
# from inspect import iscoroutinefunction


def timeit(precision=2):
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"[同步] {func.__name__} 耗时: {end - start:.{precision}f} 秒")
            return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            print(f"[异步] {func.__name__} 耗时: {end - start:.{precision}f} 秒")
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


# 测试同步函数
@timeit()
def sync_func():
    time.sleep(0.3)
    return sum(range(10))


# 测试异步函数
@timeit()
async def async_func():
    await asyncio.sleep(0.3)
    return sum(range(10))


if __name__ == "__main__":
    # 运行测试
    r1 = sync_func()  # 输出: [同步] sync_func 耗时: 0.300128 秒
    r2 = asyncio.run(async_func())  # 输出: [异步] async_func 耗时: 0.300215 秒

    print({"r1": r1, "r2": r2})
