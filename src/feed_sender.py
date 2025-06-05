import sys
import time
from collections.abc import Generator

import cv2
import numpy as np
from numpy.typing import NDArray


def run_feed_sender(
	combined_frames: Generator[NDArray[np.uint8], None, None],
) -> None:
	cv2.namedWindow('Combined Feed', cv2.WINDOW_NORMAL)
	prev_time = time.time()
	for i, frame in enumerate(combined_frames):
		now_time = time.time()
		fps = 1 / (now_time - prev_time)
		prev_time = now_time
		print(f'📸 Frame {i} received - shape: {frame.shape} - {fps:.1f} FPS')

		cv2.imshow('Combined Feed', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()
