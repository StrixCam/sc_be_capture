import queue
import threading
import time

from numpy import uint8
from numpy.typing import NDArray
from picamera2 import Picamera2
from sc_be_contracts.interfaces.capturer import ICamera
from sc_be_contracts.models.capturer.format import CaptureFormat
from sc_be_contracts.models.capturer.frame import Frame
import logging

class PiCameraAdapter(ICamera):
    def __init__(
        self,
        camera_index: int,
        resolution: tuple[int, int],
        format: CaptureFormat,
        fps: int,
    ) -> None:
        self.active = False
        self.camera_index = camera_index
        self._frame_q = queue.Queue(maxsize=1)
        self._thread: threading.Thread | None = None
        self.timeout = 0.5
        self.resolution = resolution
        self.format = format
        self.fps = fps

    def init_camera(self) -> None:
        self.picam = Picamera2(camera_num=self.camera_index)
        self.picam.set_logging(logging.ERROR)
        self.video_config = self.picam.create_video_configuration(
            main={"size": self.resolution, "format": self.format},
            controls={"FrameRate": self.fps},
        )
        self.focus()
        self.picam.configure(self.video_config)
        self.active = False

    def start(self) -> None:
        if self.active:
            return
        try:
            self.init_camera()
            self.picam.start()
            self.active = True
            self._thread = threading.Thread(target=self.__capture_loop, daemon=True)
            self._thread.start()
        except Exception:
            self.active = False

    def stop(self) -> None:
        if not self.active:
            return
        try:
            self.active = False
            self.picam.stop()
            self.picam.close()
            if self._thread:
                self._thread.join()
        except Exception:
            self.active = True

    def status(self) -> bool:
        return self.active

    def focus(self) -> None:
        self.picam.set_controls({"AfMode": 2})

    def get_frame(self) -> Frame:
        frame = self._frame_q.get(timeout=self.timeout)
        return frame

    def restart(self) -> None:
        self.stop()
        self.start()

    def __capture_loop(self) -> None:
        while self.active:
            t0 = time.time()
            request = self.picam.capture_request()
            data: NDArray[uint8] = request.make_array("main")
            request.release()
            frame = Frame(data=data, timestamp=t0)

            try:
                self._frame_q.put(frame, timeout=self.timeout)
            except queue.Full:
                _ = self._frame_q.get_nowait()
                self._frame_q.put(frame, timeout=self.timeout)
