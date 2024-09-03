import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from har_model import run_inference


class HARModel:
    def __init__(self):
        self.frame = None
        self.annotated_frame = None
        self.asyncio_sleep = 0.01

    async def process_frame(self, cam_queue, ann_queue):
        cam_loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as process_pool:
            frame = await cam_queue.get()
            inference_block = partial(run_inference, frame)
            try:
                frame = await cam_loop.run_in_executor(process_pool, inference_block)
            except Exception as e:
                print(f"Error: {e}")
            frame[-1] = True
            frame[0] = f"annotated_{frame[0]}"
            ann_queue.put_nowait(frame)
            print("From annotation model ->", ann_queue.qsize())
            # await asyncio.sleep(self.asyncio_sleep)
