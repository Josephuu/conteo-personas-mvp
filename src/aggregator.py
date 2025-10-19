"""
aggregator.py
-------------

Módulo que agrupa conteos de eventos en intervalos de tiempo definidos (p. ej.
por hora). También calcula totales acumulados y determina cuándo es momento
de exportar un reporte.
"""
from datetime import datetime, timedelta
from typing import List, Tuple


class Aggregator:
    """
    Agrupa eventos de conteo en intervalos de tiempo.

    Args:
        interval_minutes (int): número de minutos para cada intervalo.
    """
    def __init__(self, interval_minutes: int = 60):
        self.interval = timedelta(minutes=interval_minutes)
        self.current_start: datetime = datetime.now()
        self.interval_data: List[Tuple[float, int, int]] = []

    def add_count(self, timestamp: float, in_count: int, out_count: int):
        """
        Agrega un evento de conteo al acumulador.

        Args:
            timestamp: marca de tiempo Unix del evento.
            in_count: número de entradas registradas.
            out_count: número de salidas registradas.
        """
        self.interval_data.append((timestamp, in_count, out_count))

    def should_export(self) -> bool:
        """
        Determina si ha transcurrido el intervalo definido y se debe exportar.
        """
        return datetime.now() - self.current_start >= self.interval

    def reset(self):
        """
        Reinicia el acumulador y actualiza el inicio del siguiente intervalo.
        """
        self.current_start = datetime.now()
        self.interval_data = []
