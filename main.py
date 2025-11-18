"""
Script principal que orquesta todo el pipeline de análisis EEG
Ejecuta: procesamiento, visualización, clasificación y genera datos para el dashboard
"""

import numpy as np
import json
from process_eeg import procesar_datos
from visualize_signals import visualizar_segmentos
from classify import clasificar_datos

def main():
    """
    Función principal que ejecuta todo el pipeline
    """
    print("=" * 70)
    print("ANÁLISIS DE SEÑALES EEG PARA DETECCIÓN DE CONVULSIONES")
    print("=" * 70)
    print("\nPontificia Universidad Javeriana - Bogotá")
    print("Procesamiento de Señales Biológicas")
    print("Realizado por: Felipe Rangel\n")
    
    filepath = "ArchivoSeizureDetect.mat"
    
    # Paso 1: Procesar datos y extraer características
    print("\n" + "=" * 70)
    print("PASO 1: PROCESAMIENTO DE SEÑALES Y EXTRACCIÓN DE CARACTERÍSTICAS")
    print("=" * 70)
    matriz_caracteristicas, etiquetas, data_ictal, data_interictal, fs = procesar_datos(filepath)
    
    # Guardar datos procesados
    np.savez('datos_procesados.npz', 
             caracteristicas=matriz_caracteristicas,
             etiquetas=etiquetas,
             data_ictal=data_ictal,
             data_interictal=data_interictal,
             fs=fs)
    
    # Paso 2: Visualizar segmentos
    print("\n" + "=" * 70)
    print("PASO 2: VISUALIZACIÓN DE SEGMENTOS")
    print("=" * 70)
    datos_plotly = visualizar_segmentos(data_ictal, data_interictal, fs, save_plotly=True)
    
    # Paso 3: Clasificación
    print("\n" + "=" * 70)
    print("PASO 3: CLASIFICACIÓN CON SVM")
    print("=" * 70)
    resultados, clf, scaler = clasificar_datos(matriz_caracteristicas, etiquetas)
    
    # Paso 4: Preparar datos adicionales para el dashboard
    print("\n" + "=" * 70)
    print("PASO 4: PREPARANDO DATOS PARA EL DASHBOARD")
    print("=" * 70)
    
    # Agregar información de características al JSON de visualización
    nombres_caracteristicas = ['Mean', 'Variance', 'PSD Delta', 'PSD Theta', 
                               'PSD Alpha', 'PSD Beta', 'PSD Gamma']
    
    # Calcular estadísticas de características por clase
    caracteristicas_interictal = matriz_caracteristicas[etiquetas == 0]
    caracteristicas_ictal = matriz_caracteristicas[etiquetas == 1]
    
    stats_caracteristicas = {
        'nombres': nombres_caracteristicas,
        'interictal': {
            'mean': caracteristicas_interictal.mean(axis=0).tolist(),
            'std': caracteristicas_interictal.std(axis=0).tolist()
        },
        'ictal': {
            'mean': caracteristicas_ictal.mean(axis=0).tolist(),
            'std': caracteristicas_ictal.std(axis=0).tolist()
        }
    }
    
    # Guardar datos completos para el dashboard
    datos_dashboard = {
        'visualizacion': datos_plotly,
        'clasificacion': resultados,
        'caracteristicas': {
            'nombres': nombres_caracteristicas,
            'valores_interictal': caracteristicas_interictal.tolist(),
            'valores_ictal': caracteristicas_ictal.tolist(),
            'estadisticas': stats_caracteristicas
        },
        'info_general': {
            'n_eventos_ictal': int(np.sum(etiquetas == 1)),
            'n_eventos_interictal': int(np.sum(etiquetas == 0)),
            'n_caracteristicas': int(matriz_caracteristicas.shape[1]),
            'fs': float(fs),
            'n_muestras_por_evento': int(data_ictal.shape[1])
        }
    }
    
    with open('datos_dashboard.json', 'w') as f:
        json.dump(datos_dashboard, f, indent=2)
    
    print("Datos completos guardados en 'datos_dashboard.json'")
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("\nArchivos generados:")
    print("  - datos_procesados.npz: Datos procesados")
    print("  - datos_visualizacion.json: Datos de visualización")
    print("  - resultados_clasificacion.json: Resultados de clasificación")
    print("  - datos_dashboard.json: Datos completos para el dashboard")
    print("  - visualizaciones_eeg.png: Gráficas de verificación")
    print("\nEl dashboard HTML puede ser generado usando 'datos_dashboard.json'")

if __name__ == "__main__":
    main()

