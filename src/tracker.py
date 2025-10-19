"""
tracker.py
----------

Módulo para seguimiento (tracking) de objetos detectados. Este ejemplo define
una clase `Tracker` que en el futuro puede integrar algoritmos como ByteTrack
u OCSort. Por ahora se trata de un esqueleto de código.
"""
from typing import List, Tuple


class Tracker:
    """
    Clase de seguimiento de objetos.

    Args:
        max_age (int): número máximo de frames que un objeto puede no aparecer antes de ser eliminado.
        n_init (int): número de detecciones iniciales necesarias para confirmar una pista.
    """
    def __init__(self, max_age: int = 30, n_init: int = 3):
        self.max_age = max_age
        self.n_init = n_init
        # Aquí se inicializarían las estructuras internas del tracker

    def update(self, detections: List[Tuple[int, int, int, int, float]]):
        """
        Actualiza el tracker con nuevas detecciones y devuelve los objetos seguidos.

        Args:
            detections: lista de bounding boxes (x1, y1, x2, y2, confidence)

        Returns:
            List[Tuple[int, int, int, int, int]]: lista de tuplas (id, x1, y1, x2, y2).
        """
        # TODO: implementar ByteTrack u OCSort y devolver tracks
        return []
