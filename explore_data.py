"""
Script para explorar la estructura del archivo ArchivoSeizureDetect.mat
Identifica variables, dimensiones y organización de eventos interictal/ictal
"""

import scipy.io
import numpy as np

def explore_mat_file(filepath):
    """
    Explora la estructura de un archivo .mat
    
    Args:
        filepath: Ruta al archivo .mat
    """
    print(f"Explorando archivo: {filepath}\n")
    
    # Cargar el archivo .mat
    mat_data = scipy.io.loadmat(filepath)
    
    # Mostrar todas las claves disponibles
    print("=" * 60)
    print("CLAVES DISPONIBLES EN EL ARCHIVO:")
    print("=" * 60)
    for key in mat_data.keys():
        if not key.startswith('__'):  # Ignorar metadatos de MATLAB
            print(f"\nClave: {key}")
            data = mat_data[key]
            print(f"  Tipo: {type(data)}")
            if isinstance(data, np.ndarray):
                print(f"  Forma (shape): {data.shape}")
                print(f"  Tipo de datos: {data.dtype}")
                if data.size > 0:
                    print(f"  Rango de valores: [{np.min(data)}, {np.max(data)}]")
                    if data.ndim <= 2:
                        print(f"  Primeros valores:\n{data[:min(5, len(data))]}")
            elif isinstance(data, (list, tuple)):
                print(f"  Longitud: {len(data)}")
                if len(data) > 0:
                    print(f"  Tipo del primer elemento: {type(data[0])}")
            else:
                print(f"  Valor: {data}")
    
    # Mostrar metadatos
    print("\n" + "=" * 60)
    print("METADATOS:")
    print("=" * 60)
    for key in mat_data.keys():
        if key.startswith('__'):
            print(f"{key}: {type(mat_data[key])}")
    
    return mat_data

if __name__ == "__main__":
    filepath = "ArchivoSeizureDetect.mat"
    mat_data = explore_mat_file(filepath)

