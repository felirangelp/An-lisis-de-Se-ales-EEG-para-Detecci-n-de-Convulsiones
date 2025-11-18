"""
Script para procesar señales EEG y extraer características
Calcula: mean, variance, PSD en bandas delta, theta, alpha, beta, gamma
"""

import scipy.io
import numpy as np
from scipy import signal

# Bandas de frecuencia EEG estándar (en Hz)
BANDAS_FRECUENCIA = {
    'delta': (0.5, 4),
    'theta': (4, 8),
    'alpha': (8, 13),
    'beta': (13, 30),
    'gamma': (30, 100)
}

def calcular_psd_banda(senal, fs, banda_min, banda_max):
    """
    Calcula la densidad espectral de potencia (PSD) promedio en una banda de frecuencia
    
    Args:
        senal: Array 1D con la señal
        fs: Frecuencia de muestreo
        banda_min: Frecuencia mínima de la banda (Hz)
        banda_max: Frecuencia máxima de la banda (Hz)
    
    Returns:
        PSD promedio en la banda especificada
    """
    # Calcular PSD usando el método de Welch
    freqs, psd = signal.welch(senal, fs, nperseg=min(256, len(senal)), 
                              noverlap=None, nfft=None)
    
    # Encontrar índices de la banda de frecuencia
    idx_banda = np.where((freqs >= banda_min) & (freqs <= banda_max))[0]
    
    # Calcular PSD promedio en la banda
    if len(idx_banda) > 0:
        psd_banda = np.mean(psd[idx_banda])
    else:
        psd_banda = 0.0
    
    return psd_banda

def extraer_caracteristicas(senal):
    """
    Extrae las 7 características de un segmento de señal
    
    Args:
        senal: Array 1D con la señal
    
    Returns:
        Array con las características: [mean, variance, psd_delta, psd_theta, 
                                        psd_alpha, psd_beta, psd_gamma]
    """
    # Obtener frecuencia de muestreo (asumimos 500 Hz basado en la exploración)
    fs = 500.0
    
    # 1. Media
    mean_val = np.mean(senal)
    
    # 2. Varianza
    variance_val = np.var(senal)
    
    # 3-7. PSD en cada banda de frecuencia
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

def procesar_datos(filepath):
    """
    Carga y procesa los datos del archivo .mat
    
    Args:
        filepath: Ruta al archivo .mat
    
    Returns:
        tuple: (matriz_caracteristicas, etiquetas, datos_ictal, datos_interictal, fs)
    """
    # Cargar datos
    mat_data = scipy.io.loadmat(filepath)
    
    data_ictal = mat_data['Data_ictal']
    data_interictal = mat_data['Data_interictal']
    fs = float(mat_data['Fs'][0, 0])
    
    print(f"Frecuencia de muestreo: {fs:.2f} Hz")
    print(f"Eventos ictal: {data_ictal.shape[0]}")
    print(f"Eventos interictal: {data_interictal.shape[0]}")
    print(f"Muestras por evento: {data_ictal.shape[1]}")
    
    # Extraer características de todos los eventos
    caracteristicas_list = []
    etiquetas_list = []
    
    # Procesar eventos ictal (etiqueta = 1)
    print("\nProcesando eventos ictal...")
    for i in range(data_ictal.shape[0]):
        senal = data_ictal[i, :]
        caracteristicas = extraer_caracteristicas(senal)
        caracteristicas_list.append(caracteristicas)
        etiquetas_list.append(1)  # 1 = ictal
    
    # Procesar eventos interictal (etiqueta = 0)
    print("Procesando eventos interictal...")
    for i in range(data_interictal.shape[0]):
        senal = data_interictal[i, :]
        caracteristicas = extraer_caracteristicas(senal)
        caracteristicas_list.append(caracteristicas)
        etiquetas_list.append(0)  # 0 = interictal
    
    # Convertir a arrays numpy
    matriz_caracteristicas = np.array(caracteristicas_list)
    etiquetas = np.array(etiquetas_list)
    
    print(f"\nMatriz de características: {matriz_caracteristicas.shape}")
    print(f"Etiquetas: {etiquetas.shape}")
    print(f"  - Ictal (1): {np.sum(etiquetas == 1)}")
    print(f"  - Interictal (0): {np.sum(etiquetas == 0)}")
    
    return matriz_caracteristicas, etiquetas, data_ictal, data_interictal, fs

if __name__ == "__main__":
    filepath = "ArchivoSeizureDetect.mat"
    matriz_caracteristicas, etiquetas, data_ictal, data_interictal, fs = procesar_datos(filepath)
    
    # Guardar resultados para uso posterior
    np.savez('datos_procesados.npz', 
             caracteristicas=matriz_caracteristicas,
             etiquetas=etiquetas,
             data_ictal=data_ictal,
             data_interictal=data_interictal,
             fs=fs)
    
    print("\nDatos guardados en 'datos_procesados.npz'")

