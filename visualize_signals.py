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

