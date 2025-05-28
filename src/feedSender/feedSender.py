import socket
import cv2
from typing import Generator
from numpy.typing import NDArray
import numpy as np


def send_combined_feed(
    combined_frames: Generator[NDArray[np.uint8], None, None],
) -> None:
    """
    Acts as a TCP server that waits for ffplay to connect and then streams combined frames.
    """
    host: str = "0.0.0.0"
    port: int = 8888
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)

        print(f"🟢 Listening on {host}:{port} for incoming connection (e.g. ffplay)...")
        conn, addr = server_socket.accept()
        print(f"📡 Client connected from {addr}. Streaming started.")

        with conn:
            for frame in combined_frames:
                success, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                if not success:
                    print("⚠️ Failed to encode frame.")
                    continue

                try:
                    conn.sendall(encoded.tobytes())
                except Exception as e:
                    print(f"❌ Error sending frame: {e}")
                    break

        print("🛑 Streaming ended.")
