"""
Module for initializing and configuring camera feeds using Picamera2.
"""

import numpy as np
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from picamera2.picamera2 import Picamera2

from .. import config

def camera_feed(camera_name: str, camera_id: int)  -> Picamera2:
    """
    Initializes and configures a Picamera2 object for the given camera.

    Args:
        camera_name (str): Descriptive name for logs.
        camera_id (int): Camera ID (e.g. 0 or 1).

    Returns:
        Picamera2: The configured Picamera2 instance.
    """
    print(f"📸 Iniciando cámara {camera_id}: {camera_name}")
    cam = Picamera2(camera_num=camera_id)
    cam_config = cam.create_still_configuration(
        main={"size": config.CAMERA_DEFAULT_RESOLUTION},
        display="main"
    )
    cam.configure(cam_config)
    cam.start()
    frame: np.ndarray[np.uint8, np.uint8] = cam.capture_array()
    if frame is None:
        raise RuntimeError(f"❌ No se pudo capturar la cámara {camera_id}.")
    print(f"✅ Cámara {camera_id} capturada con tamaño: {frame.shape}")
    return cam
