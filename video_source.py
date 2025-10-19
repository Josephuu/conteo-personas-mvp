"""
video_source.py
-----------------

Módulo que encapsula la captura de video desde una cámara. Permite abstraer la fuente
de video (webcam local, cámara IP/RTSP, archivo) y ofrece un método simple para
obtener frames secuenciales.
"""
import cv2


class VideoSource:
    """
    Clase simple para manejar la captura de video.

    Args:
        source (int | str): índice de la cámara o ruta RTSP/archivo.
    """

    def __init__(self, source=0):
        self.source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la fuente de video: {source}")

    def read(self):
        """Lee un frame de la cámara.

        Returns:
            frame (numpy.ndarray | None): el frame capturado o None si no hay más frames.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        """Libera los recursos de la cámara."""
        self.cap.release()