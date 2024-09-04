import asyncio
import json

from camera_capture.model import HARModel
from camera_capture.video_capture import Capture


class VideoProcessor:
    def __init__(self, source, config):
        self.capture = source["capture_obj"]
        self.cam_name = source["cam_name"]
        self.cam_queue = source["cam_queue"]
        self.ann_queue = source["annotation_streaming_queue"]
        self.cap_stream_queue = source["cap_stream_queue"]
        self.config = config
        self.camera_capture = Capture(source)
        self.asyncio_sleep = 0.01
        self.har_model = HARModel()

    # Producer
    async def start_camera(self) -> None:
        while True:
            frame = await asyncio.create_task(self.camera_capture.start_capture(self.capture), name=self.cam_name)
            await self.cam_queue.put([self.cam_name, frame, True])
            await self.cap_stream_queue.put([self.cam_name, frame, True])
            await asyncio.sleep(self.asyncio_sleep)

    # Primary Consumer
    async def start_annotation(self) -> None:
        while True:
            if self.cam_queue.qsize():
                try:
                    print("Processing frame")
                    to_har_model = asyncio.create_task(
                        self.har_model.process_frame(cam_queue=self.cam_queue, ann_queue=self.ann_queue),
                        name=f"{self.cam_name}_HAR",
                    )
                    await to_har_model
                    await asyncio.sleep(self.asyncio_sleep)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                await asyncio.sleep(self.asyncio_sleep)

    # Third Consumer
    async def to_database(self, database_queue):
        frame = await database_queue.get()
        if frame[-1] is not None:
            return frame
        return


if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)
    video_processor = VideoProcessor(config["device"], "testSite", "A1B2R32", config)
