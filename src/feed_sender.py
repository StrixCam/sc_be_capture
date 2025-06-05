import sys
from collections.abc import Generator

import cv2
import numpy as np
from numpy.typing import NDArray


def run_feed_sender(
	combined_frames: Generator[NDArray[np.uint8], None, None],
) -> None:
	cv2.namedWindow('Combined Feed', cv2.WINDOW_NORMAL)
	for i, frame in enumerate(combined_frames):
		print(f'📸 Frame {i} received - shape: {frame.shape}')
		cv2.imshow('Combined Feed', frame)
		cv2.waitKey(1) 
	cv2.destroyAllWindows()
