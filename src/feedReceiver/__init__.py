from .. import config
from .feedReciever import camera_feed


def run_feed_recieved(return_processes: bool = False):
    """
    Initializes and runs camera feeds using libcamera-vid.
    If `return_processes` is True, returns the camera feed processes instead of blocking.
    Args:
        return_processes (bool): If True, returns the camera feed processes.
    Returns:
        tuple[subprocess.Popen, subprocess.Popen] or None: Camera feed processes if `return_processes` is True, otherwise None.
    """
    camera0 = camera_feed(
        camera_name=config.CAMERA_0_NAME,
        camera_index=0,
        width=config.CAMERA_DEFAULT_RESOLUTION[0],
        height=config.CAMERA_DEFAULT_RESOLUTION[1],
        fps=config.CAMERA_DEFAULT_FPS,
        codec=config.CAMERA_DEFAULT_CODEC
    )

    camera1 = camera_feed(
        camera_name=config.CAMERA_1_NAME,
        camera_index=1,
        width=config.CAMERA_DEFAULT_RESOLUTION[0],
        height=config.CAMERA_DEFAULT_RESOLUTION[1],
        fps=config.CAMERA_DEFAULT_FPS,
        codec=config.CAMERA_DEFAULT_CODEC
    )

    if return_processes:
        return camera0, camera1

    # Default behavior: block and wait
    try:
        print("🟢 Camera feeds running. Press Ctrl+C to stop.")
        camera0.wait()
        camera1.wait()
    except KeyboardInterrupt:
        print("🛑 Terminating camera feeds...")
        camera0.terminate()
        camera1.terminate()
