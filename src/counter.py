"""
counter.py
----------

Implementa la lógica de conteo de personas cuando cruzan una línea virtual. Para
un prototipo en un departamento se puede usar una sola línea que divida la
imagen en dos regiones (por ejemplo, entrada/salida).
"""
from typing import List, Tuple
import numpy as np


class LineCounter:
    """
    Cuenta personas cuando cruzan una línea determinada.

    Args:
        line_start (Tuple[int, int]): punto inicial de la línea (x, y).
        line_end (Tuple[int, int]): punto final de la línea (x, y).
    """
    def __init__(self, line_start: Tuple[int, int], line_end: Tuple[int, int]):
        self.line_start = np.array(line_start, dtype=float)
        self.line_end = np.array(line_end, dtype=float)
        self.count_in = 0
        self.count_out = 0
        # Diccionario para almacenar la última posición de cada track
        self.prev_centroids = {}

    def _is_crossing(self, prev_point: np.ndarray, curr_point: np.ndarray) -> int:
        """
        Determina si un objeto cruza la línea. Devuelve 1 si entra, -1 si sale, 0 si no cruza.
        La lógica básica compara la posición previa y actual del centroide con respecto a la línea.
        """
        # Vector perpendicular a la línea
        line_vec = self.line_end - self.line_start
        perp_vec = np.array([-line_vec[1], line_vec[0]])
        # Producto puntual para determinar el lado de cada punto
        prev_side = np.dot(prev_point - self.line_start, perp_vec)
        curr_side = np.dot(curr_point - self.line_start, perp_vec)
        # Si el signo cambia hay cruce
        if prev_side >= 0 and curr_side < 0:
            return 1  # entrada
        elif prev_side <= 0 and curr_side > 0:
            return -1  # salida
        return 0

    def update(self, tracked_objects: List[Tuple[int, int, int, int, int]]):
        """
        Actualiza el contador con objetos rastreados.

        Args:
            tracked_objects: lista de tuplas (id, x1, y1, x2, y2)
        """
        for obj_id, x1, y1, x2, y2 in tracked_objects:
            curr_centroid = np.array([(x1 + x2) / 2.0, (y1 + y2) / 2.0])
            prev_centroid = self.prev_centroids.get(obj_id)
            if prev_centroid is not None:
                crossing = self._is_crossing(prev_centroid, curr_centroid)
                if crossing == 1:
                    self.count_in += 1
                elif crossing == -1:
                    self.count_out += 1
            self.prev_centroids[obj_id] = curr_centroid
