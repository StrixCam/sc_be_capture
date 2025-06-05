from collections.abc import Generator

import numpy as np
from numpy.typing import NDArray
from picamera2 import Picamera2

from feed_combiner import run_feed_combiner
from feed_reciever import run_feed_recieved
from feed_sender import run_feed_sender

Picamera2.set_logging(level=Picamera2.ERROR)

def main() -> None:
	camera_feeds: tuple[Picamera2, Picamera2] = run_feed_recieved()
	camera0, camera1 = camera_feeds

	combined_frames: Generator[NDArray[np.uint8], None, None] = run_feed_combiner(camera0, camera1)
	
	run_feed_sender(combined_frames)


if __name__ == '__main__':
	main()
