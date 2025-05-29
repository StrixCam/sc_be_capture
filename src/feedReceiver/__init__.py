from typing import Optional, Tuple
from picamera2 import Picamera2
import numpy as np
import time

from .. import config
from .feedReciever import camera_feed

def run_feed_recieved(return_processes: bool = False) -> Optional[Tuple[Picamera2, Picamera2]]:
    """
    Captures both camera feeds using Picamera2 directly.

    Args:
        return_processes (bool): If True, returns the Picamera2 objects.

    Returns:
        Optional[Tuple[Picamera2, Picamera2]]:
            Tuple of Picamera2 objects if return_processes is True, otherwise None.
    """
    cap0 = camera_feed(camera_name=config.CAMERA_0_NAME, camera_id=config.CAMERA_0_INDEX)
    cap1 = camera_feed(camera_name=config.CAMERA_1_NAME, camera_id=config.CAMERA_1_INDEX)

    if return_processes:
        return cap0, cap1

    try:
        print("🟢 Camera feeds running. Press Ctrl+C to stop.")
        while True:
            frame0 = cap0.capture_array()
            frame1 = cap1.capture_array()
            if frame0 is None or frame1 is None:
                raise RuntimeError("❌ One or both cameras failed to deliver frames.")
            time.sleep(1 / config.CAMERA_DEFAULT_FPS)
    except KeyboardInterrupt:
        print("🛑 Terminating camera feeds...")

    return None
