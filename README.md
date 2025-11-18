# Análisis de Señales EEG para Detección de Convulsiones

Proyecto de análisis de señales de electroencefalografía (EEG) para la detección de convulsiones epilépticas, desarrollado para el curso de Procesamiento de Señales Biológicas de la Pontificia Universidad Javeriana.

## Autor
Felipe Rangel

## Descripción

Este proyecto implementa un sistema completo para:
1. Visualizar segmentos de señales EEG (interictal e ictal) en el tiempo y tiempo-frecuencia
2. Extraer características espectrales de las señales
3. Clasificar eventos usando máquinas de vectores de soporte (SVM)
4. Presentar resultados en un dashboard interactivo con Plotly

## Estructura del Proyecto

```
.
├── ArchivoSeizureDetect.mat    # Archivo de datos original
├── requirements.txt            # Dependencias del proyecto
├── explore_data.py             # Script para explorar estructura de datos
├── process_eeg.py              # Procesamiento y extracción de características
├── visualize_signals.py        # Generación de visualizaciones
├── classify.py                 # Clasificación con SVM
├── main.py                     # Script principal que ejecuta todo el pipeline
├── dashboard.html              # Dashboard interactivo con Plotly.js
└── README.md                   # Este archivo
```

## Instalación

1. Crear y activar el ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar el pipeline completo:

```bash
python main.py
```

Este script ejecuta todos los pasos:
- Procesamiento de señales y extracción de características
- Visualización de segmentos
- Clasificación con SVM
- Generación de datos para el dashboard

### Archivos generados:

- `datos_procesados.npz`: Datos procesados en formato NumPy
- `datos_visualizacion.json`: Datos de visualización
- `resultados_clasificacion.json`: Resultados de clasificación
- `datos_dashboard.json`: Datos completos para el dashboard
- `visualizaciones_eeg.png`: Gráficas de verificación

### Visualizar el dashboard:

Abrir el archivo `dashboard.html` en un navegador web. El dashboard requiere que el archivo `datos_dashboard.json` esté en el mismo directorio.

**Nota:** Para abrir el dashboard desde un servidor local (recomendado):
```bash
python -m http.server 8000
```
Luego abrir en el navegador: `http://localhost:8000/dashboard.html`

## Características Extraídas

Para cada evento se calculan 7 características:
1. **Mean**: Media de la señal
2. **Variance**: Varianza de la señal
3. **PSD Delta**: Densidad espectral de potencia en banda delta (0.5-4 Hz)
4. **PSD Theta**: Densidad espectral de potencia en banda theta (4-8 Hz)
5. **PSD Alpha**: Densidad espectral de potencia en banda alpha (8-13 Hz)
6. **PSD Beta**: Densidad espectral de potencia en banda beta (13-30 Hz)
7. **PSD Gamma**: Densidad espectral de potencia en banda gamma (30-100 Hz)

## Clasificación

- **Método**: Support Vector Machine (SVM) con kernel RBF
- **División de datos**: 80% entrenamiento, 20% prueba
- **Normalización**: StandardScaler aplicado a las características

## Dependencias

- numpy >= 1.24.0
- scipy >= 1.10.0
- scikit-learn >= 1.3.0
- plotly >= 5.17.0
- pandas >= 2.0.0
- matplotlib >= 3.7.0

## Notas

- La frecuencia de muestreo de los datos es aproximadamente 500 Hz
- Cada evento contiene 500 muestras
- El dataset contiene 70 eventos ictal y 104 eventos interictal

