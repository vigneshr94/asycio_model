import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(2, "world"))
    print(f"{time.strftime('%X')}")

    await task1
    await task2

    print(f"{time.strftime('%X')}")


asyncio.run(main())
