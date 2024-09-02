import time


def run_inference(frame):
    camera_name = frame[0]
    current_frame = frame[1]
    frame_status = frame[-1]
    if frame_status:
        time.sleep(0.5)
        print(f"Processing frame from {camera_name}")
        return [camera_name, current_frame, frame_status]
    return frame
