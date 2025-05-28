from typing import Generator

import numpy as np
from numpy.typing import NDArray

from .feedSender import send_combined_feed


def run_feed_sender(combined_frames: Generator[NDArray[np.uint8], None, None]) -> None:
    """
    Entry point for the feed sender. It takes the combined frame generator and sends it over TCP.
    """
    send_combined_feed(combined_frames)
