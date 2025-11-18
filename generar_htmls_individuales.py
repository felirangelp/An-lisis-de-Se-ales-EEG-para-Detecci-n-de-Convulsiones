"""
Script para generar archivos HTML individuales para cada gráfica del dashboard
"""

import json
import os

# Leer el dashboard completo para extraer secciones
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

# Leer datos del dashboard
with open('datos_dashboard.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Plantilla base HTML
HTML_BASE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .graph-info {{
            margin: 20px 0;
            padding: 20px;
            background-color: #ffffff;
            border-left: 4px solid #3498db;
            border-radius: 5px;
        }}
        .graph-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .description {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            line-height: 1.6;
        }}
        .conclusion {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            border-left: 4px solid #4caf50;
            line-height: 1.6;
        }}
        .code-block {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        .code-block pre {{
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .plot-container {{
            margin: 20px 0;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .info-box {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{titulo}</h1>
        <div class="info-box">
            <strong>Pontificia Universidad Javeriana - Bogotá</strong><br>
            Procesamiento de Señales Biológicas<br>
            Realizado por: Felipe Rangel
        </div>
        
        {contenido}
        
        <div class="plot-container">
            <div id="plot-container"></div>
        </div>
    </div>

    <script>
        // Datos del dashboard
        const datosDashboard = {datos_json};
        
        {codigo_javascript}
    </script>
</body>
</html>
"""

# Función para crear HTML de gráfica temporal
def crear_html_temporal_interictal():
    titulo = "Señal EEG - Segmento Interictal"
    descripcion = """<strong>Descripción:</strong> Esta gráfica muestra la señal EEG en el dominio del tiempo para un segmento interictal (entre crisis epilépticas). La señal representa la actividad eléctrica del cerebro durante un período de actividad normal, sin convulsiones. Se observa la variación de amplitud de la señal a lo largo del tiempo, medida en microvoltios (μV)."""
    conclusion = """<strong>Conclusión:</strong> La señal interictal muestra una actividad relativamente estable con variaciones de amplitud moderadas. No se observan patrones de alta amplitud o sincronización característicos de eventos convulsivos. Esta señal sirve como referencia para comparar con la actividad ictal."""
    codigo_python = """# Código Python para visualización temporal interictal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Cargar datos del archivo .mat
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_interictal = mat_data['Data_interictal']
fs = float(mat_data['Fs'][0, 0])  # Frecuencia de muestreo

# Seleccionar el primer segmento interictal
segmento_interictal = data_interictal[0, :]

# Crear vector de tiempo en segundos
n_muestras = len(segmento_interictal)
tiempo = np.arange(n_muestras) / fs

# Crear la gráfica
plt.figure(figsize=(12, 4))
plt.plot(tiempo, segmento_interictal, 'b-', linewidth=0.5)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Amplitud (μV)', fontsize=12)
plt.title('Señal EEG - Segmento Interictal', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const trace = {
            x: datosDashboard.visualizacion.tiempo_interictal,
            y: datosDashboard.visualizacion.senal_interictal,
            type: 'scatter',
            mode: 'lines',
            line: { color: 'blue', width: 1 },
            name: 'Señal EEG'
        };

        const layout = {
            title: {
                text: 'Señal EEG - Segmento Interictal',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Tiempo (s)',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Amplitud (μV)',
                titlefont: { size: 14 }
            },
            hovermode: 'closest',
            margin: { l: 60, r: 30, t: 50, b: 50 }
        };

        Plotly.newPlot('plot-container', [trace], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de gráfica temporal ictal
def crear_html_temporal_ictal():
    titulo = "Señal EEG - Segmento Ictal"
    descripcion = """<strong>Descripción:</strong> Esta gráfica muestra la señal EEG en el dominio del tiempo para un segmento ictal (durante una crisis epiléptica). La señal captura la actividad eléctrica anormal del cerebro caracterizada por descargas sincronizadas de alta amplitud y frecuencia. Esta actividad es distintiva y permite identificar eventos convulsivos."""
    conclusion = """<strong>Conclusión:</strong> La señal ictal presenta características claramente diferentes a la interictal: mayor amplitud, patrones más sincronizados y actividad de alta frecuencia. Estas diferencias son fundamentales para el desarrollo de algoritmos de detección automática de convulsiones."""
    codigo_python = """# Código Python para visualización temporal ictal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Cargar datos del archivo .mat
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_ictal = mat_data['Data_ictal']
fs = float(mat_data['Fs'][0, 0])  # Frecuencia de muestreo

# Seleccionar el primer segmento ictal
segmento_ictal = data_ictal[0, :]

# Crear vector de tiempo en segundos
n_muestras = len(segmento_ictal)
tiempo = np.arange(n_muestras) / fs

# Crear la gráfica
plt.figure(figsize=(12, 4))
plt.plot(tiempo, segmento_ictal, 'r-', linewidth=0.5)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Amplitud (μV)', fontsize=12)
plt.title('Señal EEG - Segmento Ictal', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const trace = {
            x: datosDashboard.visualizacion.tiempo_ictal,
            y: datosDashboard.visualizacion.senal_ictal,
            type: 'scatter',
            mode: 'lines',
            line: { color: 'red', width: 1 },
            name: 'Señal EEG'
        };

        const layout = {
            title: {
                text: 'Señal EEG - Segmento Ictal',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Tiempo (s)',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Amplitud (μV)',
                titlefont: { size: 14 }
            },
            hovermode: 'closest',
            margin: { l: 60, r: 30, t: 50, b: 50 }
        };

        Plotly.newPlot('plot-container', [trace], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de espectrograma interictal
def crear_html_espectrograma_interictal():
    titulo = "Espectrograma - Segmento Interictal"
    descripcion = """<strong>Descripción:</strong> El espectrograma muestra la distribución de energía de la señal EEG en función del tiempo y la frecuencia para un segmento interictal. Utiliza la transformada de Fourier de tiempo corto (STFT) para analizar cómo varía el contenido espectral a lo largo del tiempo. Los colores representan la densidad espectral de potencia (PSD) en decibelios (dB), donde colores más intensos indican mayor energía en esa frecuencia y tiempo."""
    conclusion = """<strong>Conclusión:</strong> El espectrograma interictal muestra una distribución de energía relativamente uniforme a través de las diferentes bandas de frecuencia, sin concentraciones significativas de energía en bandas específicas. La actividad espectral es más dispersa y de menor intensidad comparada con la actividad ictal."""
    codigo_python = """# Código Python para espectrograma interictal
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io

# Cargar datos del archivo .mat
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_interictal = mat_data['Data_interictal']
fs = float(mat_data['Fs'][0, 0])  # Frecuencia de muestreo

# Seleccionar el primer segmento interictal
segmento_interictal = data_interictal[0, :]

# Calcular espectrograma usando el método de Welch
nperseg = min(256, len(segmento_interictal) // 4)
noverlap = nperseg // 2
freqs, times, Sxx = signal.spectrogram(
    segmento_interictal, 
    fs, 
    nperseg=nperseg, 
    noverlap=noverlap, 
    window='hann'
)

# Convertir a decibelios para mejor visualización
Sxx_db = 10 * np.log10(Sxx + 1e-10)  # Evitar log(0)

# Crear el espectrograma
plt.figure(figsize=(12, 6))
plt.pcolormesh(times, freqs, Sxx_db, shading='gouraud', cmap='viridis')
plt.colorbar(label='PSD (dB)')
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Frecuencia (Hz)', fontsize=12)
plt.title('Espectrograma - Segmento Interictal', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const trace = {
            x: datosDashboard.visualizacion.times_interictal,
            y: datosDashboard.visualizacion.freqs_interictal,
            z: datosDashboard.visualizacion.Sxx_interictal,
            type: 'heatmap',
            colorscale: 'Viridis',
            colorbar: {
                title: 'PSD (dB)',
                titleside: 'right'
            }
        };

        const layout = {
            title: {
                text: 'Espectrograma - Segmento Interictal',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Tiempo (s)',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Frecuencia (Hz)',
                titlefont: { size: 14 }
            },
            margin: { l: 60, r: 30, t: 50, b: 50 }
        };

        Plotly.newPlot('plot-container', [trace], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de espectrograma ictal
def crear_html_espectrograma_ictal():
    titulo = "Espectrograma - Segmento Ictal"
    descripcion = """<strong>Descripción:</strong> El espectrograma muestra la distribución de energía de la señal EEG durante un evento ictal (crisis epiléptica). Esta representación tiempo-frecuencia revela cómo la actividad espectral cambia durante la convulsión, mostrando concentraciones de energía en bandas de frecuencia específicas. Los patrones espectrales durante eventos ictales son característicos y diferentes a los observados en períodos interictales."""
    conclusion = """<strong>Conclusión:</strong> El espectrograma ictal muestra concentraciones significativas de energía, particularmente en las bandas de frecuencia más altas (beta y gamma). Se observan patrones más estructurados y sincronizados, con mayor intensidad espectral comparada con la actividad interictal. Estas características espectrales son clave para la detección automática de convulsiones."""
    codigo_python = """# Código Python para espectrograma ictal
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io

# Cargar datos del archivo .mat
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_ictal = mat_data['Data_ictal']
fs = float(mat_data['Fs'][0, 0])  # Frecuencia de muestreo

# Seleccionar el primer segmento ictal
segmento_ictal = data_ictal[0, :]

# Calcular espectrograma usando el método de Welch
nperseg = min(256, len(segmento_ictal) // 4)
noverlap = nperseg // 2
freqs, times, Sxx = signal.spectrogram(
    segmento_ictal, 
    fs, 
    nperseg=nperseg, 
    noverlap=noverlap, 
    window='hann'
)

# Convertir a decibelios para mejor visualización
Sxx_db = 10 * np.log10(Sxx + 1e-10)  # Evitar log(0)

# Crear el espectrograma
plt.figure(figsize=(12, 6))
plt.pcolormesh(times, freqs, Sxx_db, shading='gouraud', cmap='viridis')
plt.colorbar(label='PSD (dB)')
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Frecuencia (Hz)', fontsize=12)
plt.title('Espectrograma - Segmento Ictal', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const trace = {
            x: datosDashboard.visualizacion.times_ictal,
            y: datosDashboard.visualizacion.freqs_ictal,
            z: datosDashboard.visualizacion.Sxx_ictal,
            type: 'heatmap',
            colorscale: 'Viridis',
            colorbar: {
                title: 'PSD (dB)',
                titleside: 'right'
            }
        };

        const layout = {
            title: {
                text: 'Espectrograma - Segmento Ictal',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Tiempo (s)',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Frecuencia (Hz)',
                titlefont: { size: 14 }
            },
            margin: { l: 60, r: 30, t: 50, b: 50 }
        };

        Plotly.newPlot('plot-container', [trace], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de visualización multi-canal
def crear_html_multicanal():
    titulo = "Visualización Multi-Canal EEG: Transición Interictal → Ictal"
    descripcion = """<strong>Descripción:</strong> Esta visualización muestra múltiples canales de EEG (16 canales) apilados verticalmente, representando la transición desde un estado interictal (entre crisis) hacia un estado ictal (durante la crisis epiléptica). Cada línea horizontal representa un canal diferente de la señal EEG. La parte izquierda de cada canal (en azul) muestra la actividad interictal, caracterizada por amplitudes relativamente bajas y patrones irregulares. La parte derecha (en marrón) muestra la actividad ictal, con amplitudes significativamente mayores y patrones más rítmicos y sincronizados. La línea roja punteada vertical marca el punto de transición entre ambos estados."""
    conclusion = """<strong>Conclusión:</strong> La visualización multi-canal revela de manera clara y simultánea las diferencias entre los estados interictal e ictal a través de múltiples canales. Se observa una transición abrupta y sincronizada en todos los canales, donde la actividad ictal muestra amplitudes dramáticamente aumentadas y patrones más estructurados. Esta representación es fundamental para el diagnóstico clínico y demuestra visualmente por qué las características extraídas (especialmente las relacionadas con amplitud y contenido espectral) son efectivas para la clasificación automática de convulsiones."""
    codigo_python = """# Código Python para visualización multi-canal EEG
import numpy as np
import matplotlib.pyplot as plt
import scipy.io

def crear_visualizacion_multicanal(data_ictal, data_interictal, fs, n_canales=16):
    # Seleccionar n_canales eventos de cada tipo
    n_canales = min(n_canales, min(data_interictal.shape[0], data_ictal.shape[0]))
    indices_interictal = np.linspace(0, data_interictal.shape[0]-1, n_canales, dtype=int)
    indices_ictal = np.linspace(0, data_ictal.shape[0]-1, n_canales, dtype=int)
    
    # Crear vector de tiempo para cada segmento
    n_muestras = data_interictal.shape[1]
    tiempo_segmento = np.arange(n_muestras) / fs
    
    # Preparar datos para cada canal
    offset_vertical = 0
    spacing = 500  # Espaciado vertical entre canales
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    for i in range(n_canales):
        seg_interictal = data_interictal[indices_interictal[i], :]
        seg_ictal = data_ictal[indices_ictal[i], :]
        
        tiempo_interictal = tiempo_segmento
        tiempo_ictal = tiempo_segmento + tiempo_segmento[-1] + tiempo_segmento[1]
        
        senal_interictal_offset = seg_interictal + offset_vertical
        senal_ictal_offset = seg_ictal + offset_vertical
        
        ax.plot(tiempo_interictal, senal_interictal_offset, 'b-', linewidth=0.8, alpha=0.8)
        ax.plot(tiempo_ictal, senal_ictal_offset, color='#8B4513', linewidth=0.8, alpha=0.8)
        
        offset_vertical -= spacing
    
    tiempo_transicion = tiempo_segmento[-1] + tiempo_segmento[1]
    y_max = spacing * (n_canales - 1)
    ax.axvline(x=tiempo_transicion, color='red', linestyle='--', linewidth=2, label='Transición')
    
    ax.set_xlabel('Tiempo (s)', fontsize=12)
    ax.set_ylabel('Amplitud (μV) - Canales apilados', fontsize=12)
    ax.set_title('Visualización Multi-Canal EEG: Transición Interictal → Ictal', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

# Cargar datos
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_ictal = mat_data['Data_ictal']
data_interictal = mat_data['Data_interictal']
fs = float(mat_data['Fs'][0, 0])

# Crear visualización
crear_visualizacion_multicanal(data_ictal, data_interictal, fs, n_canales=16)"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const datosMulticanal = datosDashboard.visualizacion.multicanal;
        const traces = [];
        const tiempoTransicion = datosMulticanal.tiempo_transicion;
        
        datosMulticanal.canales.forEach((canal, index) => {
            traces.push({
                x: canal.tiempo_interictal,
                y: canal.senal_interictal.map(val => val + canal.offset),
                type: 'scatter',
                mode: 'lines',
                line: { color: 'blue', width: 0.8 },
                name: index === 0 ? 'Interictal' : '',
                showlegend: index === 0,
                hoverinfo: 'skip'
            });
            
            traces.push({
                x: canal.tiempo_ictal,
                y: canal.senal_ictal.map(val => val + canal.offset),
                type: 'scatter',
                mode: 'lines',
                line: { color: '#8B4513', width: 0.8 },
                name: index === 0 ? 'Ictal' : '',
                showlegend: index === 0,
                hoverinfo: 'skip'
            });
        });
        
        const yMin = Math.min(...datosMulticanal.canales.map(c => c.offset - 500));
        const yMax = Math.max(...datosMulticanal.canales.map(c => c.offset + 500));
        
        traces.push({
            x: [tiempoTransicion, tiempoTransicion],
            y: [yMin, yMax],
            type: 'scatter',
            mode: 'lines',
            line: { color: 'red', width: 2, dash: 'dash' },
            name: 'Transición',
            showlegend: true,
            hoverinfo: 'skip'
        });
        
        const layout = {
            title: {
                text: 'Visualización Multi-Canal EEG: Transición Interictal → Ictal',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Tiempo (s)',
                titlefont: { size: 14 },
                showgrid: true,
                gridcolor: 'rgba(128,128,128,0.2)'
            },
            yaxis: {
                title: 'Amplitud (μV) - Canales apilados',
                titlefont: { size: 14 },
                showgrid: true,
                gridcolor: 'rgba(128,128,128,0.2)',
                showticklabels: false
            },
            hovermode: 'closest',
            margin: { l: 60, r: 30, t: 50, b: 50 },
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)'
            },
            annotations: [
                {
                    x: tiempoTransicion / 2,
                    y: yMax - 200,
                    text: 'Interictal',
                    showarrow: false,
                    font: { size: 14, color: 'blue', bold: true },
                    bgcolor: 'rgba(255,255,255,0.7)',
                    bordercolor: 'blue',
                    borderwidth: 2
                },
                {
                    x: tiempoTransicion + (tiempoTransicion / 2),
                    y: yMax - 200,
                    text: 'Ictal',
                    showarrow: false,
                    font: { size: 14, color: '#8B4513', bold: true },
                    bgcolor: 'rgba(255,255,255,0.7)',
                    bordercolor: '#8B4513',
                    borderwidth: 2
                }
            ]
        };
        
        Plotly.newPlot('plot-container', traces, layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de características (ahora con gráficas individuales)
def crear_html_caracteristicas():
    titulo = "Comparación de Características: Interictal vs Ictal"
    descripcion = """<strong>Descripción:</strong> Las siguientes gráficas muestran las 7 características extraídas de todos los eventos EEG, comparando las clases interictal e ictal. Cada característica se presenta en una gráfica individual con su propia escala, lo que permite visualizar mejor las diferencias sin que características con valores grandes (como Variance) dominen la visualización. Las características incluyen: media (mean), varianza (variance), y densidad espectral de potencia (PSD) en las bandas delta (0.5-4 Hz), theta (4-8 Hz), alpha (8-13 Hz), beta (13-30 Hz) y gamma (30-100 Hz). Las barras muestran los valores promedio y las líneas de error representan la desviación estándar."""
    conclusion = """<strong>Conclusión:</strong> Al visualizar cada característica de manera individual, se pueden observar claramente las diferencias entre estados interictal e ictal. Las características espectrales (PSD en diferentes bandas) muestran variaciones importantes, especialmente en las bandas de mayor frecuencia (beta y gamma), donde los eventos ictales presentan mayor energía. Estas diferencias justifican el uso de estas características para la clasificación automática de convulsiones."""
    codigo_python = """# Código Python para matriz de características y comparación
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io

# Definir bandas de frecuencia EEG estándar
BANDAS_FRECUENCIA = {
    'delta': (0.5, 4),
    'theta': (4, 8),
    'alpha': (8, 13),
    'beta': (13, 30),
    'gamma': (30, 100)
}

def calcular_psd_banda(senal, fs, banda_min, banda_max):
    freqs, psd = signal.welch(senal, fs, nperseg=min(256, len(senal)), 
                              noverlap=None, nfft=None)
    idx_banda = np.where((freqs >= banda_min) & (freqs <= banda_max))[0]
    if len(idx_banda) > 0:
        psd_banda = np.mean(psd[idx_banda])
    else:
        psd_banda = 0.0
    return psd_banda

def extraer_caracteristicas(senal):
    fs = 500.0
    mean_val = np.mean(senal)
    variance_val = np.var(senal)
    psd_delta = calcular_psd_banda(senal, fs, BANDAS_FRECUENCIA['delta'][0], 
                                    BANDAS_FRECUENCIA['delta'][1])
    psd_theta = calcular_psd_banda(senal, fs, BANDAS_FRECUENCIA['theta'][0], 
                                    BANDAS_FRECUENCIA['theta'][1])
    psd_alpha = calcular_psd_banda(senal, fs, BANDAS_FRECUENCIA['alpha'][0], 
                                    BANDAS_FRECUENCIA['alpha'][1])
    psd_beta = calcular_psd_banda(senal, fs, BANDAS_FRECUENCIA['beta'][0], 
                                   BANDAS_FRECUENCIA['beta'][1])
    psd_gamma = calcular_psd_banda(senal, fs, BANDAS_FRECUENCIA['gamma'][0], 
                                   BANDAS_FRECUENCIA['gamma'][1])
    return np.array([mean_val, variance_val, psd_delta, psd_theta, 
                     psd_alpha, psd_beta, psd_gamma])

# Cargar datos
mat_data = scipy.io.loadmat('ArchivoSeizureDetect.mat')
data_ictal = mat_data['Data_ictal']
data_interictal = mat_data['Data_interictal']

# Extraer características de todos los eventos
caracteristicas_interictal = []
caracteristicas_ictal = []

for i in range(data_interictal.shape[0]):
    caracteristicas_interictal.append(extraer_caracteristicas(data_interictal[i, :]))

for i in range(data_ictal.shape[0]):
    caracteristicas_ictal.append(extraer_caracteristicas(data_ictal[i, :]))

caracteristicas_interictal = np.array(caracteristicas_interictal)
caracteristicas_ictal = np.array(caracteristicas_ictal)

# Calcular promedios y desviaciones estándar
mean_interictal = caracteristicas_interictal.mean(axis=0)
std_interictal = caracteristicas_interictal.std(axis=0)
mean_ictal = caracteristicas_ictal.mean(axis=0)
std_ictal = caracteristicas_ictal.std(axis=0)

# Nombres de las características
nombres = ['Mean', 'Variance', 'PSD Delta', 'PSD Theta', 
           'PSD Alpha', 'PSD Beta', 'PSD Gamma']

# Crear gráfica individual para cada característica
for i, nombre in enumerate(nombres):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = ['Interictal', 'Ictal']
    y = [mean_interictal[i], mean_ictal[i]]
    yerr = [std_interictal[i], std_ictal[i]]
    colors = ['blue', 'red']
    
    bars = ax.bar(x, y, yerr=yerr, color=colors, alpha=0.7, capsize=10, width=0.6)
    ax.set_ylabel('Valor', fontsize=12)
    ax.set_title(f'{nombre}: Comparación Interictal vs Ictal', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
        </div>
        
        <div class="graph-info">
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
        
        <div class="plot-container">
            <div id="plot-caracteristica-mean"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-variance"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-psd-delta"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-psd-theta"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-psd-alpha"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-psd-beta"></div>
        </div>
        <div class="plot-container">
            <div id="plot-caracteristica-psd-gamma"></div>
        </div>
    """
    
    codigo_js = """
        const nombres = datosDashboard.caracteristicas.nombres;
        const estadisticas = datosDashboard.caracteristicas.estadisticas;
        const ids = [
            'plot-caracteristica-mean',
            'plot-caracteristica-variance',
            'plot-caracteristica-psd-delta',
            'plot-caracteristica-psd-theta',
            'plot-caracteristica-psd-alpha',
            'plot-caracteristica-psd-beta',
            'plot-caracteristica-psd-gamma'
        ];
        
        nombres.forEach((nombre, index) => {
            const traceInterictal = {
                x: ['Interictal'],
                y: [estadisticas.interictal.mean[index]],
                type: 'bar',
                name: 'Interictal',
                marker: { color: 'blue' },
                error_y: {
                    type: 'data',
                    array: [estadisticas.interictal.std[index]],
                    visible: true
                },
                width: 0.5
            };

            const traceIctal = {
                x: ['Ictal'],
                y: [estadisticas.ictal.mean[index]],
                type: 'bar',
                name: 'Ictal',
                marker: { color: 'red' },
                error_y: {
                    type: 'data',
                    array: [estadisticas.ictal.std[index]],
                    visible: true
                },
                width: 0.5
            };

            const layout = {
                title: {
                    text: nombre + ': Comparación Interictal vs Ictal',
                    font: { size: 16 }
                },
                xaxis: {
                    title: 'Estado',
                    titlefont: { size: 14 }
                },
                yaxis: {
                    title: 'Valor',
                    titlefont: { size: 14 }
                },
                barmode: 'group',
                margin: { l: 60, r: 30, t: 50, b: 50 },
                legend: { x: 0.7, y: 0.95 },
                showlegend: true
            };

            Plotly.newPlot(ids[index], [traceInterictal, traceIctal], layout, {responsive: true});
        });
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de matriz de confusión
def crear_html_matriz_confusion():
    titulo = "Matriz de Confusión"
    descripcion = """<strong>Descripción:</strong> La matriz de confusión muestra el rendimiento del clasificador SVM comparando las predicciones del modelo con los valores reales de las etiquetas. La matriz es una tabla de 2x2 donde las filas representan las clases reales (Interictal e Ictal) y las columnas representan las clases predichas. Los valores en la diagonal principal (verdaderos positivos y verdaderos negativos) indican clasificaciones correctas, mientras que los valores fuera de la diagonal (falsos positivos y falsos negativos) indican errores de clasificación."""
    conclusion = """<strong>Conclusión:</strong> El clasificador SVM muestra un buen rendimiento con una precisión del 88.57%. La matriz de confusión revela que el modelo tiene una alta capacidad para identificar correctamente eventos interictales (21/21 correctos), mientras que tiene algunas dificultades con eventos ictales (10/14 correctos, 4 falsos negativos). Esto sugiere que el modelo es más conservador en la detección de convulsiones, lo cual puede ser preferible en aplicaciones clínicas para evitar falsas alarmas."""
    codigo_python = """# Código Python para matriz de confusión
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos procesados
# (asumiendo que ya se tienen las características y etiquetas)
# matriz_caracteristicas: array (n_eventos, 7)
# etiquetas: array (n_eventos,) con 0=interictal, 1=ictal

# Dividir datos en training y testing (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    matriz_caracteristicas, 
    etiquetas, 
    test_size=0.2, 
    random_state=42, 
    stratify=etiquetas
)

# Normalizar características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar clasificador SVM
clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
clf.fit(X_train_scaled, y_train)

# Realizar predicciones
y_pred = clf.predict(X_test_scaled)

# Calcular matriz de confusión
cm = confusion_matrix(y_test, y_pred)

# Crear visualización de la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Interictal', 'Ictal'],
            yticklabels=['Interictal', 'Ictal'],
            cbar_kws={{'label': 'Cantidad'}})
plt.xlabel('Predicción', fontsize=12)
plt.ylabel('Valor Real', fontsize=12)
plt.title('Matriz de Confusión', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const z = datosDashboard.clasificacion.confusion_matrix;
        const x = ['Interictal', 'Ictal'];
        const y = ['Interictal', 'Ictal'];

        const trace = {
            x: x,
            y: y,
            z: z,
            type: 'heatmap',
            colorscale: 'Blues',
            text: z.map(row => row.map(val => val.toString())),
            texttemplate: '%{text}',
            textfont: { size: 16, color: 'white' },
            showscale: true,
            colorbar: {
                title: 'Cantidad',
                titleside: 'right'
            }
        };

        const layout = {
            title: {
                text: 'Matriz de Confusión',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Predicción',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Valor Real',
                titlefont: { size: 14 }
            },
            margin: { l: 80, r: 30, t: 50, b: 50 }
        };

        Plotly.newPlot('plot-container', [trace], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Función para crear HTML de métricas
def crear_html_metricas():
    titulo = "Métricas de Clasificación por Clase"
    descripcion = """<strong>Descripción:</strong> Esta gráfica muestra las métricas de rendimiento del clasificador SVM para cada clase (Interictal e Ictal). Las métricas incluyen: Precision (precisión), que mide la proporción de predicciones positivas que fueron correctas; Recall (sensibilidad), que mide la proporción de casos positivos reales que fueron identificados correctamente; y F1-Score, que es la media armónica de precision y recall, proporcionando una medida balanceada del rendimiento. Estas métricas permiten evaluar el rendimiento del modelo de manera más detallada que solo la precisión global."""
    conclusion = """<strong>Conclusión:</strong> El análisis de métricas muestra que el clasificador tiene un excelente rendimiento para la clase Interictal (precision=0.84, recall=1.00, F1=0.91), indicando que casi todos los eventos interictales son identificados correctamente. Para la clase Ictal, el modelo tiene precision perfecta (1.00) pero recall moderado (0.71), lo que significa que cuando predice un evento ictal, siempre es correcto, pero no detecta todos los eventos ictales. El F1-Score de 0.83 para Ictal indica un buen balance general. Estas métricas confirman que el modelo es adecuado para aplicaciones de detección de convulsiones."""
    codigo_python = """# Código Python para métricas de clasificación
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Cargar datos procesados
# (asumiendo que ya se tienen las características y etiquetas)
# matriz_caracteristicas: array (n_eventos, 7)
# etiquetas: array (n_eventos,) con 0=interictal, 1=ictal

# Dividir datos en training y testing (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    matriz_caracteristicas, 
    etiquetas, 
    test_size=0.2, 
    random_state=42, 
    stratify=etiquetas
)

# Normalizar características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar clasificador SVM
clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
clf.fit(X_train_scaled, y_train)

# Realizar predicciones
y_pred = clf.predict(X_test_scaled)

# Calcular métricas por clase
precision_interictal = precision_score(y_test, y_pred, pos_label=0)
recall_interictal = recall_score(y_test, y_pred, pos_label=0)
f1_interictal = f1_score(y_test, y_pred, pos_label=0)

precision_ictal = precision_score(y_test, y_pred, pos_label=1)
recall_ictal = recall_score(y_test, y_pred, pos_label=1)
f1_ictal = f1_score(y_test, y_pred, pos_label=1)

# Preparar datos para gráfica
clases = ['Interictal', 'Ictal']
precision = [precision_interictal, precision_ictal]
recall = [recall_interictal, recall_ictal]
f1 = [f1_interictal, f1_ictal]

# Crear gráfica de barras
x = np.arange(len(clases))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width, precision, width, label='Precision', color='green', alpha=0.7)
bars2 = ax.bar(x, recall, width, label='Recall', color='orange', alpha=0.7)
bars3 = ax.bar(x + width, f1, width, label='F1-Score', color='purple', alpha=0.7)

ax.set_xlabel('Clase', fontsize=12)
ax.set_ylabel('Valor', fontsize=12)
ax.set_title('Métricas de Clasificación por Clase', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(clases)
ax.set_ylim([0, 1.1])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# Imprimir reporte completo
print(classification_report(y_test, y_pred, target_names=['Interictal', 'Ictal']))"""
    
    contenido = f"""
        <div class="graph-info">
            <div class="graph-title">{titulo}</div>
            <div class="description">{descripcion}</div>
            <div class="conclusion">{conclusion}</div>
            <div class="code-block"><pre>{codigo_python}</pre></div>
        </div>
    """
    
    codigo_js = """
        const clases = ['Interictal', 'Ictal'];
        const precision = [
            datosDashboard.clasificacion.classification_report['Interictal'].precision,
            datosDashboard.clasificacion.classification_report['Ictal'].precision
        ];
        const recall = [
            datosDashboard.clasificacion.classification_report['Interictal'].recall,
            datosDashboard.clasificacion.classification_report['Ictal'].recall
        ];
        const f1 = [
            datosDashboard.clasificacion.classification_report['Interictal']['f1-score'],
            datosDashboard.clasificacion.classification_report['Ictal']['f1-score']
        ];

        const trace1 = {
            x: clases,
            y: precision,
            type: 'bar',
            name: 'Precision',
            marker: { color: 'green' }
        };

        const trace2 = {
            x: clases,
            y: recall,
            type: 'bar',
            name: 'Recall',
            marker: { color: 'orange' }
        };

        const trace3 = {
            x: clases,
            y: f1,
            type: 'bar',
            name: 'F1-Score',
            marker: { color: 'purple' }
        };

        const layout = {
            title: {
                text: 'Métricas de Clasificación por Clase',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Clase',
                titlefont: { size: 14 }
            },
            yaxis: {
                title: 'Valor',
                titlefont: { size: 14 },
                range: [0, 1.1]
            },
            barmode: 'group',
            margin: { l: 60, r: 30, t: 50, b: 50 },
            legend: { x: 0.7, y: 0.95 }
        };

        Plotly.newPlot('plot-container', [trace1, trace2, trace3], layout, {responsive: true});
    """
    
    datos_json = json.dumps(datos, indent=2)
    
    html = HTML_BASE.format(
        titulo=titulo,
        contenido=contenido,
        datos_json=datos_json,
        codigo_javascript=codigo_js
    )
    
    return html

# Generar todos los archivos HTML
if __name__ == "__main__":
    os.makedirs('imagenes', exist_ok=True)
    
    graficas = [
        ('01_senal_temporal_interictal.html', crear_html_temporal_interictal),
        ('02_senal_temporal_ictal.html', crear_html_temporal_ictal),
        ('03_espectrograma_interictal.html', crear_html_espectrograma_interictal),
        ('04_espectrograma_ictal.html', crear_html_espectrograma_ictal),
        ('05_visualizacion_multicanal.html', crear_html_multicanal),
        ('06_comparacion_caracteristicas.html', crear_html_caracteristicas),
        ('07_matriz_confusion.html', crear_html_matriz_confusion),
        ('08_metricas_clasificacion.html', crear_html_metricas)
    ]
    
    print("Generando archivos HTML individuales...")
    for filename, funcion in graficas:
        html_content = funcion()
        filepath = os.path.join('imagenes', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ Generado: {filepath}")
    
    print(f"\n✓ Se generaron {len(graficas)} archivos HTML en la carpeta 'imagenes'")

