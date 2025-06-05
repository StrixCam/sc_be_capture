from collections.abc import Generator

import cv2
import numpy as np
from numpy.typing import NDArray
from picamera2 import Picamera2

from config import envs


def run_feed_combiner(cam0: Picamera2, cam1: Picamera2) -> Generator[NDArray[np.uint8], None, None]:
	cv2.startWindowThread()
	while True:
		frame0: NDArray[np.uint8] = cam0.capture_array(wait=True)
		frame1: NDArray[np.uint8] = cam1.capture_array(wait=True)

		min_height: int = min(frame0.shape[0], frame1.shape[0])
		frame0 = cv2.resize(frame0, (frame0.shape[1], min_height))
		frame1 = cv2.resize(frame1, (frame1.shape[1], min_height))

		combined: NDArray[np.uint8] = np.hstack((frame0, frame1)).astype(np.uint8)
		resized: NDArray[np.uint8] = cv2.resize(
			combined, envs.FEED_OUTPUT_RESOLUTION, interpolation=cv2.INTER_AREA
		)
		colored: NDArray[np.uint8] = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
		flipped: NDArray[np.uint8] = cv2.flip(colored, 1)
		yield flipped
