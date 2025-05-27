import subprocess
from typing import Optional

from .. import config

def camera_feed (
    camera_name: str,
    camera_index: int,
    width: int = config.CAMERA_DEFAULT_RESOLUTION[0],
    height: int = config.CAMERA_DEFAULT_RESOLUTION[1],
    fps: int = config.CAMERA_DEFAULT_FPS,
    codec: str = config.CAMERA_DEFAULT_CODEC,
) -> subprocess.Popen:
    """
    Initializes a camera feed using ffmpeg.
    """
    command = [
        'libcamera-vid',
        '--camera', str(camera_index),
        '--width', str(width),
        '--height', str(height),
        '--framerate', str(fps),
        '--codec', codec,
        '--no-preview',
        '--timeout', '0',
        '--output', '-'
    ]
    
    print(f"Initializing camera feed for {camera_name} with command: {' '.join(command)}")
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )
    
    return process