from typing import Generator

import cv2
import numpy as np
from numpy.typing import NDArray
from picamera2.picamera2 import Picamera2

from .. import config


def combine_camera_feeds(
    cam0: Picamera2,
    cam1: Picamera2
) -> Generator[NDArray[np.uint8], None, None]:
    """
    Continuously reads frames from two Picamera2 objects and horizontally stacks them.

    Args:
        cam0 (Picamera2): Left camera
        cam1 (Picamera2): Right camera

    Yields:
        NDArray[np.uint8]: Combined (horizontally stacked) frame
    """
    while True:
        try:
            frame0: NDArray[np.uint8] = cam0.capture_array(wait=True)
            frame1: NDArray[np.uint8] = cam1.capture_array(wait=True)

            if frame0 is None:
                raise RuntimeError("❌ Failed to read from Left Camera.")
            if frame1 is None:
                raise RuntimeError("❌ Failed to read from Right Camera.")

            combined = np.hstack((frame0,frame1,)).astype(np.uint8)
            resized = cv2.resize(combined,config.FEED_OUTPUT_RESOLUTION,interpolation=cv2.INTER_AREA)
            colored = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
            flipped = cv2.flip(colored, 1)
            yield flipped

        except Exception as e:
            raise RuntimeError(f"❌ Error combining camera feeds: {e}") from e
