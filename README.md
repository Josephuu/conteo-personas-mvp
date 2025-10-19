# Conteo de Personas MVP

## Descripción general

Este proyecto implementa un prototipo de **conteo de personas en tiempo real** para cafeterías, restaurantes y supermercados, pero adaptado para pruebas en un departamento. El sistema utiliza una **webcam 1080p** conectada localmente (o cualquier cámara RTSP) para detectar personas, rastrearlas y contar entradas/salidas a través de zonas o líneas virtuales. Toda la inferencia se realiza localmente en una PC, con la opción de exportar métricas cada hora en formato CSV/Excel.

### Objetivos del MVP

* Contar personas cuando se detectan atravesando una línea de conteo.
* Procesar video de una webcam 1080p de forma local (sin cloud).
* Generar reportes horarios en CSV con timestamp, conteo de entradas y salidas, y totales acumulados.
* Privacidad por defecto: no se guarda video, sólo métricas.

### Alcance

* Ingesta de video de cámara local (USB o RTSP).
* Detección de personas con **YOLOv8**.
* Tracking multi‑objeto con **ByteTrack** u **OCSort**.
* Lógica de conteo cruzando líneas virtuales definidas en configuración.
* Exportación periódica de datos a CSV.
* Opción para un dashboard minimal (Streamlit) con gráficas de conteo.

### Arquitectura del sistema

1. **VideoSource**: captura frames de la cámara.
2. **Detector**: detecta personas usando YOLOv8 (Ultralytics) u otro modelo configurado.
3. **Tracker**: asocia detecciones a identificadores persistentes usando ByteTrack.
4. **Counter**: registra cruces de líneas/zonas para contabilizar entradas y salidas.
5. **Aggregator**: agrupa conteos por intervalos de tiempo (por ejemplo, 1 hora).
6. **Exporter**: escribe los resultados a CSV y opcionalmente a una base SQLite o Parquet.
7. **Dashboard (opcional)**: visualiza métricas en tiempo real o históricas.

### Requisitos de hardware

* PC con CPU decente (Core i5) para prototipo; se recomienda GPU (RTX 3060) para mejor rendimiento.
* Webcam 1080p (la resolución puede escalarse a 640 px en preprocesamiento).
* Sistema operativo con Python 3.10 o superior.

### Instalación

1. Clonar este repositorio:

   ```bash
   git clone https://github.com/tu‑usuario/conteo-personas-mvp.git
   cd conteo-personas-mvp
   ```

2. Crear un entorno virtual y activarlo:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar el archivo `config.yaml` para definir la fuente de video y las líneas de conteo.

### Uso

Ejecutar el script principal:

```bash
python src/main.py --config config.yaml
```

Esto iniciará el proceso de conteo. Los reportes se guardarán en la carpeta `exports/`.

### Configuración

El archivo `config.yaml` permite definir:

* `video_source`: ruta/índice de la cámara (por ejemplo, `0` para webcam local).
* `output_dir`: carpeta donde se guardan los reportes.
* `interval_minutes`: intervalo en minutos para generar reportes (por defecto, 60).
* `counting_line`: dos puntos que definen la línea de conteo dentro del frame.
* Configuración del detector (`model` y `confidence_threshold`).
* Parámetros del tracker (`max_age` y `n_init`).

### Próximos pasos

* Ajustar la posición de la cámara y calibrar la línea de conteo.
* Optimizar el rendimiento con modelos INT8/ONNX para CPU (OpenVINO).
* Implementar un dashboard de visualización de métricas (Streamlit).
