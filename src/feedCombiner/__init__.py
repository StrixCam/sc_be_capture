from .feedCombiner import combine_camera_feeds
import subprocess
from typing import Generator
from numpy.typing import NDArray
import numpy as np

def run_feed_combiner(
    process_0: subprocess.Popen[bytes],
    process_1: subprocess.Popen[bytes]
) -> Generator[NDArray[np.uint8], None, None]:
    return combine_camera_feeds(process_0, process_1)