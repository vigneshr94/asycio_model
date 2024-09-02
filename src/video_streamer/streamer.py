import asyncio

import cv2 as cv


class Streamer:
    def __init__(self, source):
        self.asyncio_sleep = 0.01

    async def start_streaming(self, streaming_queue):
        while True:
            if streaming_queue.qsize():
                try:
                    frame = await streaming_queue.get()
                    print(frame[0])
                    cv.imshow(frame[0], frame[1])
                    if cv.waitKey(1) == 27:
                        break
                except Exception as e:
                    print(f"Error: {e}")
            else:
                await asyncio.sleep(self.asyncio_sleep)
