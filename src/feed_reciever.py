from typing import Any

import numpy as np
from numpy.typing import NDArray
from picamera2 import Picamera2

from config import envs


def camera_feed(camera_name: str, camera_id: int) -> Picamera2:
	print(f'📸 Iniciando cámara {camera_id}: {camera_name}')
	cam = Picamera2(camera_num=camera_id)
	if cam.started:
		cam.stop()
	cam_config: dict[str, Any] = cam.create_still_configuration(
		main={'size': envs.CAMERA_DEFAULT_RESOLUTION},
		controls={'FrameRate': envs.CAMERA_DEFAULT_FPS},
		display='main',
	)
	
	cam.configure(cam_config)
	cam.start()
	frame: NDArray[np.uint8] = cam.capture_array(wait=True)
	if frame is None:
		raise RuntimeError(f'❌ No se pudo capturar la cámara {camera_id}.')
	print(f'✅ Cámara {camera_id} capturada con tamaño: {frame.shape}')
	return cam


def run_feed_recieved() -> tuple[Picamera2, Picamera2]:
	cap0: Picamera2 = camera_feed(camera_name=envs.CAMERA_0_NAME, camera_id=envs.CAMERA_0_INDEX)
	cap1: Picamera2 = camera_feed(camera_name=envs.CAMERA_1_NAME, camera_id=envs.CAMERA_1_INDEX)

	return cap0, cap1
