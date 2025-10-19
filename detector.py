"""
detector.py
-----------

Módulo para detección de objetos (personas) utilizando modelos como YOLOv8. Esta
clase sirve como envoltorio para cargar y ejecutar un modelo de detección.
"""
from typing import List, Tuple


class Detector:
    """
    Detector de personas usando un modelo configurable (por ejemplo, YOLOv8).

    Args:
        model_name (str): nombre o ruta del modelo a cargar.
        conf_threshold (float): umbral de confianza para filtrar detecciones.
    """
    def __init__(self, model_name: str = "yolov8n", conf_threshold: float = 0.5):
        self.model_name = model_name
        self.conf_threshold = conf_threshold
        self.model = None  # Modelo aún no cargado

    def load_model(self):
        """
        Carga el modelo de detección. Para YOLOv8 se puede utilizar la librería
        Ultralytics. Este método debe inicializar `self.model`.
        """
        # TODO: integrar con la API de Ultralytics o cargar un modelo ONNX
        # from ultralytics import YOLO
        # self.model = YOLO(self.model_name)
        pass

    def detect(self, frame) -> List[Tuple[int, int, int, int, float]]:
        """
        Ejecuta la detección de personas sobre el frame proporcionado.

        Args:
            frame (numpy.ndarray): imagen BGR

        Returns:
            List[Tuple[int, int, int, int, float]]: lista de bounding boxes (x1, y1, x2, y2, confidence).
        """
        # TODO: realizar la inferencia y devolver las detecciones
        return []