from datetime import datetime

import cv2 as cv


def run_inference(frame):
    camera_name = frame[0]
    current_frame = frame[1]
    frame_status = frame[-1]
    if frame_status:
        print(f"Processing frame from {camera_name}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        position = (10, current_frame.shape[0] - 10)
        cv.putText(
            current_frame,
            timestamp,
            position,
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv.LINE_AA,
        )
        return [camera_name, current_frame, frame_status]
    return frame
