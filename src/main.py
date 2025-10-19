"""
main.py
-------

Punto de entrada para ejecutar el sistema de conteo de personas. Carga
configuración desde un archivo YAML, inicializa los componentes y procesa
frames de video en un bucle continuo. Genera reportes CSV en intervalos
periódicos.
"""
import argparse
import time
from typing import Tuple

import yaml

# Importa módulos locales. Al ejecutar `python src/main.py`, el paquete src se
# encuentra en el path gracias al __init__.py. Si aparece un error de importación,
# asegúrese de ejecutar con la raíz del repositorio como directorio actual.
from src.video_source import VideoSource
from src.detector import Detector
from src.tracker import Tracker
from src.counter import LineCounter
from src.aggregator import Aggregator
from src.exporter import CSVExporter


def load_config(path: str) -> dict:
    """Carga un archivo YAML y devuelve un diccionario."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(config_path: str):
    config = load_config(config_path)

    # Inicializar componentes a partir de la configuración
    video_source = VideoSource(config.get("video_source", 0))
    detector_cfg = config.get("detector", {})
    tracker_cfg = config.get("tracker", {})
    detector = Detector(
        model_name=detector_cfg.get("model", "yolov8n"),
        conf_threshold=detector_cfg.get("confidence_threshold", 0.5),
    )
    tracker = Tracker(
        max_age=tracker_cfg.get("max_age", 30),
        n_init=tracker_cfg.get("n_init", 3),
    )

    # Línea de conteo
    line_points: Tuple[Tuple[int, int], Tuple[int, int]] = config.get("counting_line", [[0, 0], [0, 0]])
    line_start, line_end = line_points
    counter = LineCounter(tuple(line_start), tuple(line_end))

    interval_minutes = config.get("interval_minutes", 60)
    aggregator = Aggregator(interval_minutes)
    exporter = CSVExporter(config.get("output_dir", "exports"))

    # Cargar modelo de detección
    detector.load_model()

    total_in = 0
    total_out = 0

    try:
        while True:
            frame = video_source.read()
            if frame is None:
                # Esperar un poco si no se pudo leer un frame
                time.sleep(0.05)
                continue

            # Ejecutar detección y seguimiento
            detections = detector.detect(frame)
            tracks = tracker.update(detections)

            # Actualizar contador con los tracks
            counter.update(tracks)

            # Obtener las cuentas acumuladas de este frame
            in_count = counter.count_in
            out_count = counter.count_out

            timestamp = time.time()
            aggregator.add_count(timestamp, in_count, out_count)
            total_in += in_count
            total_out += out_count

            if aggregator.should_export():
                # Preparar datos para exportar; por ahora la confianza media es un valor fijo
                export_rows = []
                for (ts, ic, oc) in aggregator.interval_data:
                    export_rows.append((ts, ic, oc, total_in, total_out, 1.0))
                csv_path = exporter.export(export_rows)
                print(f"Se exportó reporte a {csv_path}")
                aggregator.reset()

    except KeyboardInterrupt:
        print("Detenido por el usuario.")
    finally:
        video_source.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema de conteo de personas")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Ruta al archivo de configuración YAML",
    )
    args = parser.parse_args()
    main(args.config)
