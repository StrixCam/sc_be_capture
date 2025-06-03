from typing import Generator
import numpy as np
from numpy.typing import NDArray

from .feed-sender import send_combined_feed


def run_feed_sender(combined_frames: Generator[NDArray[np.uint8], None, None]) -> None:
    """
    Entry point for the feed sender. Sends combined frames over TCP using a raw TCP socket.

    Args:
        combined_frames: Generator yielding BGR frames (e.g., horizontally stacked camera feeds).
    """
    send_combined_feed(combined_frames)
