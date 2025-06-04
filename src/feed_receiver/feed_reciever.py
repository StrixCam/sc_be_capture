"""
Module for initializing and configuring camera feeds using Picamera2.
"""

from picamera2.picamera2 import Picamera2
from picamera2.controls import Controls

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
    cam = Picamera2(camera_num=camera_id,verbose_console=0)
    cam_config = cam.create_still_configuration(
        main={"size": config.CAMERA_DEFAULT_RESOLUTION},
        display="main",
    )
    cam_config["controls"]["FrameDurationLimits"] = (int(1e6 / config.CAMERA_DEFAULT_FPS), int(1e6 / config.CAMERA_DEFAULT_FPS))
    cam.configure(cam_config)
    cam.start()
    frame = cam.capture_array(wait=True)
    if frame is None:
        raise RuntimeError(f"❌ No se pudo capturar la cámara {camera_id}.")
    print(f"✅ Cámara {camera_id} capturada con tamaño: {frame.shape}")
    return cam
