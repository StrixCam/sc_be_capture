"""
This module provides the entry point for the feed sender, which sends combined frames over TCP.
"""

from typing import Generator
import numpy as np
from numpy.typing import NDArray
from picamera2.picamera2 import Picamera2

from .feed_combiner import combine_camera_feeds


def run_feed_combiner(
    cam0: Picamera2,
    cam1: Picamera2
) -> Generator[NDArray[np.uint8], None, None]:
    """
    Initializes feed combiner logic with two Picamera2 objects.

    Args:
        cam0 (Picamera2): Left camera
        cam1 (Picamera2): Right camera

    Returns:
        Generator yielding combined frames as NDArray[np.uint8]
    """
    return combine_camera_feeds(cam0, cam1)
