from picamera2 import Picamera2
from config import envs
from feed_reciever import feed_recieved

def run_feed_recieved() -> tuple[Picamera2, Picamera2]:
    cap0: Picamera2 = feed_recieved(
        camera_name=envs.CAMERA_0_NAME, camera_id=envs.CAMERA_0_INDEX
    )
    cap1: Picamera2 = feed_recieved(
        camera_name=envs.CAMERA_1_NAME, camera_id=envs.CAMERA_1_INDEX
    )

    return cap0, cap1
