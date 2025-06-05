import time

import cv2
from picamera2 import Picamera2


def capture_frames():
	picam2 = Picamera2()
	picam2.start()
	while True:
		im = picam2.capture_array()
		print(im.shape)
		im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
		cv2.imshow('Face Attendance', im)
		cv2.waitKey(1)
	cv2.destroyAllWindows()


capture_frames()
