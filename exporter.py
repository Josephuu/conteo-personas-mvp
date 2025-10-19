"""
exporter.py
-----------

Contiene una clase simple para exportar datos de conteo a un archivo CSV. Cada
llamada a `export` escribirá un nuevo archivo en el directorio especificado.
"""
import csv
import os
from datetime import datetime
from typing import List, Tuple


class CSVExporter:
    """
    Exporta datos de conteo a archivos CSV.

    Args:
        output_dir (str): carpeta donde se guardan los CSV.
    """
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, data: List[Tuple[float, int, int, int, int, float]], file_prefix: str = "report") -> str:
        """
        Escribe las filas proporcionadas en un archivo CSV y devuelve la ruta.

        Args:
            data: lista de tuplas (timestamp, in_count, out_count, total_in_day,
                  total_out_day, confidence_mean)
            file_prefix: prefijo del nombre del archivo.

        Returns:
            str: ruta al archivo creado.
        """
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{file_prefix}_{date_str}.csv"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "in_count",
                "out_count",
                "total_in_day",
                "total_out_day",
                "confidence_mean",
            ])
            writer.writerows(data)
        return path