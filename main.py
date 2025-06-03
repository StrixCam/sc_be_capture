"""
This module provides the entry point for the feed sender, which sends combined frames over TCP.
"""

from src.feed_receiver import run_feed_recieved
from src.feed_combiner import run_feed_combiner
from src.feed_sender import run_feed_sender


def main() -> None:
    """
    Orchestrates the full video pipeline:
    1. Initializes two camera feeds using Picamera2.
    2. Combines the frames horizontally.
    3. Streams the combined feed over TCP to a client (e.g., ffplay).
    """
    camera_feeds = run_feed_recieved(return_processes=True)
    if not camera_feeds:
        raise RuntimeError("❌ No se pudieron inicializar las cámaras.")

    camera0, camera1 = camera_feeds

    combined_frames = run_feed_combiner(camera0, camera1)
    run_feed_sender(combined_frames)


if __name__ == "__main__":
    main()
