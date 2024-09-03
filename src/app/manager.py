import asyncio
import json
import signal

import cv2 as cv

from camera_capture import VideoProcessor
from video_streamer import Streamer


class Manager:
    def __init__(self, config):
        self.config = config
        self.source = []
        for name, source in self.config['device'].items():
            obj_dict = {}
            capture_obj = cv.VideoCapture(source)
            obj_dict['capture_obj'] = capture_obj
            obj_dict['cam_name'] = name
            self.source.append(obj_dict)
        self.video_processor = None

    def get_loop_attributes(self, camera):
        source = {}
        for camera_object in self.source:
            if camera_object["cam_name"] == camera:
                source["cam_name"] = camera_object["cam_name"]
                source["capture_obj"] = camera_object["capture_obj"]
        cam_queue = asyncio.LifoQueue(maxsize=100)
        cap_stream_queue = asyncio.LifoQueue(maxsize=100)
        annotation_streaming_queue = asyncio.LifoQueue(maxsize=100)
        database_queue = asyncio.LifoQueue(maxsize=100)
        source['cam_queue'] = cam_queue
        source['cap_stream_queue'] = cap_stream_queue
        source['annotation_streaming_queue'] = annotation_streaming_queue
        source['database_queue'] = database_queue
        return source

    async def start(self, source):
        cam_queue = source['cam_queue']
        cap_stream_queue = source['cap_stream_queue']
        ann_queue = source['annotation_streaming_queue']
        task_loop = source['loop']
        video_processor = VideoProcessor(source, self.config)
        har_streamer = Streamer(source)
        cam_streamer = Streamer(source)
        capture_task = asyncio.create_task(video_processor.start_camera(), name="capture_task")
        cam_streaming_task = asyncio.create_task(
            cam_streamer.start_streaming(cap_stream_queue), name="cam_streaming_task"
        )
        annotation_task = asyncio.create_task(
            video_processor.start_annotation(),
            name="annotation_task",
        )
        try:
            annotation_streaming_task = asyncio.create_task(
                har_streamer.start_streaming(ann_queue), name="annotation_streaming_task"
            )
        except Exception as e:
            print(f"Error: {e}")
        tasks = [capture_task, cam_streaming_task, annotation_task, annotation_streaming_task]
        await asyncio.gather(
            *tasks,
            return_exceptions=True
            )

    async def run(self, source):
        await self.start(source)

    async def shutdown_(signal_, loop_):
        print(f"Received exit signal {signal_}.")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        print(f"Cancelling {len(tasks)} outstanding tasks")
        await asyncio.gather(*tasks, return_exceptions=True)
        loop_.stop()


async def main(task_object, sources):
    _loop = asyncio.get_event_loop()
    _loop.add_signal_handler(signal.SIGINT, _loop.stop)
    for source in sources:
        source['loop'] = _loop
    try:
        tasks = []
        for source in sources:
            task = asyncio.create_task(task_object.start(source))
            tasks.append(task)
        await asyncio.gather(*tasks)
    finally:
        print("Successfully shutdown service")
        for source in sources:
            source['loop'].stop()


if __name__ == "__main__":
    with open("src/config.json") as file:
        config = json.load(file)
    manager = Manager(config)
    source1 = manager.get_loop_attributes("camera_1")
    source2 = manager.get_loop_attributes("camera_2")
    source3 = manager.get_loop_attributes("camera_3")
    source4 = manager.get_loop_attributes("camera_4")
    sources = [source1, source2, source3, source4]
    asyncio.run(main(manager, sources))
