from picamera2 import Picamera2
from time import sleep
from threading import Thread
import numpy as np

def capture_camera(index: int, results: dict):
    try:
        print(f"📸 Iniciando cámara {index}")
        cam = Picamera2(index)
        cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
        cam.start()
        sleep(2)
        frame = cam.capture_array()
        cam.stop()
        print(f"✅ Cámara {index} capturada con tamaño: {frame.shape}")
        results[index] = frame
    except Exception as e:
        print(f"❌ Error con cámara {index}: {e}")
        results[index] = None

def main():
    results = {}
    threads = []

    for i in [0, 1]:
        t = Thread(target=capture_camera, args=(i, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Si ambas capturas fueron exitosas, combinamos las imágenes
    if all(results.get(i) is not None for i in [0, 1]):
        combined = np.hstack((results[0], results[1]))
        print(f"🧩 Frame combinado: {combined.shape}")
    else:
        print("⚠️ Una o ambas cámaras fallaron al capturar")

if __name__ == "__main__":
    main()
