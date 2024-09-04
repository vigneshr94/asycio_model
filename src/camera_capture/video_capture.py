import json
import pathlib

import cv2 as cv


class Capture:
    def __init__(self, sources: dict) -> None:
        self.cap = sources["capture_obj"]
        self.cam_name = sources["cam_name"]

    async def start_capture(self, capture_obj: cv.VideoCapture):
        capture_obj.grab()
        ret, frame = capture_obj.retrieve()
        if not ret:
            print(f"Cannot open {self.cam_name}. Exiting......")
            return
        return frame

    async def show_capture(self, _queue) -> None:
        frame = await _queue.get()
        cv.imshow(frame[0], frame[1])


if __name__ == "__main__":
    config_file = "config.json"

    with open(f"../{config_file}") as file:
        config = json.load(file)

    CAM_DEVICE = config["device"]
    WIN_TITLE = pathlib.Path(__file__).stem
    QUIT_KEY = ord(config["quit_key"])
    capture = Capture(CAM_DEVICE)
    win_title = WIN_TITLE
    quit_key = QUIT_KEY

    for ret, frame in capture.start_capture():
        cv.imshow(win_title, frame)
        key = cv.waitKey(1) & 0xFF
        if key == quit_key:
            break
            capture.stop_capture()
