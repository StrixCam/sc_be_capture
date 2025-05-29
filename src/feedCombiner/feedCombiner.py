import numpy as np
from typing import Generator
from numpy.typing import NDArray
from picamera2 import Picamera2


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
            frame0 = cam0.capture_array()
            frame1 = cam1.capture_array()

            if frame0 is None:
                raise RuntimeError("❌ Failed to read from Left Camera.")
            if frame1 is None:
                raise RuntimeError("❌ Failed to read from Right Camera.")

            combined = np.hstack((frame0,frame1,)).astype(np.uint8)
            yield combined

        except Exception as e:
            raise RuntimeError(f"❌ Error combining camera feeds: {e}") from e
