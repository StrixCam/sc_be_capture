import sys
import cv2
import numpy as np
from typing import Generator
from numpy.typing import NDArray


def send_combined_feed(
    combined_frames: Generator[NDArray[np.uint8], None, None]
) -> None:
    """
    Streams combined video frames as MJPEG over stdout (to be read by ffplay).
    """
    try:
        for frame in combined_frames:
            # Codifica como JPEG
            success, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not success:
                print("⚠️ Failed to encode frame.", file=sys.stderr)
                continue

            # Escribe los bytes JPEG con delimitador adecuado para MJPEG
            sys.stdout.buffer.write(b"--frame\r\n")
            sys.stdout.buffer.write(b"Content-Type: image/jpeg\r\n\r\n")
            sys.stdout.buffer.write(encoded.tobytes())
            sys.stdout.buffer.write(b"\r\n")
            sys.stdout.flush()

    except BrokenPipeError:
        print("🛑 ffplay closed. Stopping feed.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
