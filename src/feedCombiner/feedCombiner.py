import cv2
import numpy as np
import subprocess

from typing import Generator
from .. import config


def _read_frame_from_pipe(pipe) -> np.ndarray:
    """
    Reads a single frame from the given subprocess pipe.
    Args:
        pipe (subprocess.Popen): The subprocess pipe to read from.
    Returns:
        np.ndarray: The decoded frame in BGR format, or None if an error occurs.
    """
    
    resolution: tuple[int,int] = config.CAMERA_DEFAULT_RESOLUTION
    width, height = resolution
    frame_size = width * height * 3 // 2  # YUV420p format
    
    try:
      raw_data = pipe.stdout.read(frame_size)
    except Exception as e:
      print(f"Error reading from pipe: {e}")
      return None

    if not raw_data or len(raw_data) != frame_size:
        print("⚠️ Incomplete frame received or end of stream.")
        return None

    # Convert raw YUV420p to BGR using OpenCV
    yuv_frame = np.frombuffer(raw_data, dtype=np.uint8).reshape((height * 3 // 2, width))
    bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)

    return bgr_frame


def combine_camera_feeds(
    process_0: subprocess.Popen,
    process_1: subprocess.Popen
) -> Generator[np.ndarray, None, None]:
    """
    Combines frames from two camera feeds into a single frame.
    Args:
        process_0 (subprocess.Popen): The first camera feed process.
        process_1 (subprocess.Popen): The second camera feed process.
    Yields:
        np.ndarray: Combined frames from both camera feeds.
    """

    while True:
        try:
          frame0 = _read_frame_from_pipe(process_0)
          frame1 = _read_frame_from_pipe(process_1)

          if frame0 is None or frame1 is None:
              print("❌ Lost camera feed")
              break

          combined = np.hstack((frame0, frame1))
          yield combined
        except KeyboardInterrupt:
          print("🛑 Stopping feed combination...")
          break
        except Exception as e:
            print(f"⚠️ Error combining feeds: {e}")
            break
