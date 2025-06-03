import socket
import cv2
import numpy as np
from typing import Generator
from numpy.typing import NDArray


def send_combined_feed(combined_frames: Generator[NDArray[np.uint8], None, None]) -> None:
    """
    Starts a TCP server and streams combined video frames to a single client using JPEG encoding.

    Args:
        combined_frames: Generator yielding combined BGR frames as NDArray[np.uint8].
    """
    host = "0.0.0.0"
    port = 8888

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)

        print(f"🟢 Waiting for ffplay to connect at tcp://<RASPBERRY-IP>:{port} ...")
        conn, addr = server_socket.accept()
        print(f"📡 Client connected from {addr}. Streaming started.")

        with conn:
            try:
                for frame in combined_frames:
                    # Optionally resize or transform frame if needed
                    success, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                    if not success:
                        print("⚠️ Failed to encode frame.")
                        continue

                    conn.sendall(encoded.tobytes())
            except Exception as e:
                print("❌ Client disconnected or error during streaming:", e)

        print("🛑 Streaming ended.")
