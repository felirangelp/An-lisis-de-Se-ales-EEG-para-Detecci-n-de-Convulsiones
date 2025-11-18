"""
Script para visualizar señales EEG
Genera gráficas temporales y tiempo-frecuencia (espectrogramas) para segmentos interictal e ictal
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

def crear_espectrograma(senal, fs, titulo):
    """
    Crea un espectrograma de una señal
    
    Args:
        senal: Array 1D con la señal
        fs: Frecuencia de muestreo
        titulo: Título para el gráfico
    
    Returns:
        tuple: (tiempos, frecuencias, espectrograma) para plotly
    """
    # Calcular espectrograma
    nperseg = min(256, len(senal) // 4)
    noverlap = nperseg // 2
    freqs, times, Sxx = signal.spectrogram(senal, fs, nperseg=nperseg, 
                                           noverlap=noverlap, 
                                           window='hann')
    
    # Convertir a dB
    Sxx_db = 10 * np.log10(Sxx + 1e-10)  # Evitar log(0)
    
    return times, freqs, Sxx_db

def crear_visualizacion_multicanal(data_ictal, data_interictal, fs, n_canales=16):
    """
    Crea una visualización multi-canal mostrando la transición interictal-ictal
    
    Args:
        data_ictal: Array con eventos ictal (n_eventos, n_muestras)
        data_interictal: Array con eventos interictal (n_eventos, n_muestras)
        fs: Frecuencia de muestreo
        n_canales: Número de canales a mostrar (default 16)
    
    Returns:
        dict: Diccionario con datos para plotly
    """
    # Seleccionar n_canales eventos de cada tipo
    n_canales = min(n_canales, min(data_interictal.shape[0], data_ictal.shape[0]))
    indices_interictal = np.linspace(0, data_interictal.shape[0]-1, n_canales, dtype=int)
    indices_ictal = np.linspace(0, data_ictal.shape[0]-1, n_canales, dtype=int)
    
    # Crear vector de tiempo para cada segmento
    n_muestras = data_interictal.shape[1]
    tiempo_segmento = np.arange(n_muestras) / fs
    
    # Concatenar interictal seguido de ictal para cada canal
    tiempo_completo = np.concatenate([tiempo_segmento, tiempo_segmento + tiempo_segmento[-1] + tiempo_segmento[1]])
    
    # Preparar datos para cada canal
    canales_datos = []
    offset_vertical = 0
    spacing = 500  # Espaciado vertical entre canales
    
    for i in range(n_canales):
        # Obtener segmentos
        seg_interictal = data_interictal[indices_interictal[i], :]
        seg_ictal = data_ictal[indices_ictal[i], :]
        
        # Concatenar y añadir offset vertical
        senal_completa = np.concatenate([seg_interictal, seg_ictal])
        senal_offset = senal_completa + offset_vertical
        
        canales_datos.append({
            'tiempo': tiempo_completo.tolist(),
            'senal': senal_offset.tolist(),
            'senal_interictal': seg_interictal.tolist(),
            'senal_ictal': seg_ictal.tolist(),
            'tiempo_interictal': tiempo_segmento.tolist(),
            'tiempo_ictal': (tiempo_segmento + tiempo_segmento[-1] + tiempo_segmento[1]).tolist(),
            'offset': float(offset_vertical)
        })
        
        offset_vertical -= spacing
    
    return {
        'canales': canales_datos,
        'n_canales': n_canales,
        'tiempo_transicion': float(tiempo_segmento[-1] + tiempo_segmento[1]),
        'fs': float(fs)
    }

def visualizar_segmentos(data_ictal, data_interictal, fs, save_plotly=True):
    """
    Crea visualizaciones temporales y tiempo-frecuencia de segmentos representativos
    
    Args:
        data_ictal: Array con eventos ictal (n_eventos, n_muestras)
        data_interictal: Array con eventos interictal (n_eventos, n_muestras)
        fs: Frecuencia de muestreo
        save_plotly: Si True, guarda datos para plotly en JSON
    """
    # Seleccionar un segmento representativo de cada tipo
    # Usar el primer evento de cada tipo
    segmento_interictal = data_interictal[0, :]
    segmento_ictal = data_ictal[0, :]
    
    # Crear vector de tiempo
    n_muestras = len(segmento_interictal)
    tiempo = np.arange(n_muestras) / fs  # tiempo en segundos
    
    # Crear espectrogramas
    print("Generando espectrogramas...")
    times_interictal, freqs_interictal, Sxx_interictal = crear_espectrograma(
        segmento_interictal, fs, "Interictal")
    times_ictal, freqs_ictal, Sxx_ictal = crear_espectrograma(
        segmento_ictal, fs, "Ictal")
    
    # Crear visualización multi-canal
    print("Generando visualización multi-canal...")
    datos_multicanal = crear_visualizacion_multicanal(data_ictal, data_interictal, fs, n_canales=16)
    
    # Preparar datos para plotly
    datos_plotly = {
        'tiempo_interictal': tiempo.tolist(),
        'senal_interictal': segmento_interictal.tolist(),
        'tiempo_ictal': tiempo.tolist(),
        'senal_ictal': segmento_ictal.tolist(),
        'times_interictal': times_interictal.tolist(),
        'freqs_interictal': freqs_interictal.tolist(),
        'Sxx_interictal': Sxx_interictal.tolist(),
        'times_ictal': times_ictal.tolist(),
        'freqs_ictal': freqs_ictal.tolist(),
        'Sxx_ictal': Sxx_ictal.tolist(),
        'multicanal': datos_multicanal,
        'fs': float(fs)
    }
    
    if save_plotly:
        with open('datos_visualizacion.json', 'w') as f:
            json.dump(datos_plotly, f)
        print("Datos de visualización guardados en 'datos_visualizacion.json'")
    
    # Crear visualizaciones con matplotlib para verificación
    print("Generando gráficas con matplotlib...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gráfica temporal interictal
    axes[0, 0].plot(tiempo, segmento_interictal, 'b-', linewidth=0.5)
    axes[0, 0].set_xlabel('Tiempo (s)')
    axes[0, 0].set_ylabel('Amplitud (μV)')
    axes[0, 0].set_title('Señal EEG - Segmento Interictal')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Espectrograma interictal
    im1 = axes[0, 1].pcolormesh(times_interictal, freqs_interictal, Sxx_interictal, 
                                shading='gouraud', cmap='viridis')
    axes[0, 1].set_xlabel('Tiempo (s)')
    axes[0, 1].set_ylabel('Frecuencia (Hz)')
    axes[0, 1].set_title('Espectrograma - Segmento Interictal')
    plt.colorbar(im1, ax=axes[0, 1], label='PSD (dB)')
    
    # Gráfica temporal ictal
    axes[1, 0].plot(tiempo, segmento_ictal, 'r-', linewidth=0.5)
    axes[1, 0].set_xlabel('Tiempo (s)')
    axes[1, 0].set_ylabel('Amplitud (μV)')
    axes[1, 0].set_title('Señal EEG - Segmento Ictal')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Espectrograma ictal
    im2 = axes[1, 1].pcolormesh(times_ictal, freqs_ictal, Sxx_ictal, 
                               shading='gouraud', cmap='viridis')
    axes[1, 1].set_xlabel('Tiempo (s)')
    axes[1, 1].set_ylabel('Frecuencia (Hz)')
    axes[1, 1].set_title('Espectrograma - Segmento Ictal')
    plt.colorbar(im2, ax=axes[1, 1], label='PSD (dB)')
    
    plt.tight_layout()
    plt.savefig('visualizaciones_eeg.png', dpi=150, bbox_inches='tight')
    print("Gráficas guardadas en 'visualizaciones_eeg.png'")
    plt.close()
    
    return datos_plotly

if __name__ == "__main__":
    # Cargar datos procesados
    datos = np.load('datos_procesados.npz')
    data_ictal = datos['data_ictal']
    data_interictal = datos['data_interictal']
    fs = datos['fs']
    
    datos_plotly = visualizar_segmentos(data_ictal, data_interictal, fs)

