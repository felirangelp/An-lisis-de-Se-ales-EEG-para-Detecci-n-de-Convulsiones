"""
Script para clasificación de señales EEG usando SVM
Divide datos en training/testing, entrena el modelo y evalúa rendimiento
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import json

def clasificar_datos(matriz_caracteristicas, etiquetas, test_size=0.2, random_state=42):
    """
    Clasifica los datos usando SVM
    
    Args:
        matriz_caracteristicas: Array (n_eventos, n_caracteristicas)
        etiquetas: Array (n_eventos,) con etiquetas (0=interictal, 1=ictal)
        test_size: Proporción de datos para testing (default 0.2 = 20%)
        random_state: Semilla para reproducibilidad
    
    Returns:
        dict: Diccionario con resultados de la clasificación
    """
    print("=" * 60)
    print("CLASIFICACIÓN CON SVM")
    print("=" * 60)
    
    # Dividir datos en training y testing
    X_train, X_test, y_train, y_test = train_test_split(
        matriz_caracteristicas, etiquetas, 
        test_size=test_size, random_state=random_state, 
        stratify=etiquetas  # Mantener proporción de clases
    )
    
    print(f"\nDivisión de datos:")
    print(f"  Training: {X_train.shape[0]} eventos ({100*(1-test_size):.1f}%)")
    print(f"  Testing: {X_test.shape[0]} eventos ({100*test_size:.1f}%)")
    print(f"  Características: {X_train.shape[1]}")
    
    # Normalizar características
    print("\nNormalizando características...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar clasificador SVM
    print("Entrenando clasificador SVM...")
    clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=random_state)
    clf.fit(X_train_scaled, y_train)
    
    # Predecir en conjunto de testing
    print("Realizando predicciones...")
    y_pred = clf.predict(X_test_scaled)
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, 
                                   target_names=['Interictal', 'Ictal'],
                                   output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n" + "=" * 60)
    print("RESULTADOS DE CLASIFICACIÓN")
    print("=" * 60)
    print(f"\nPrecisión (Accuracy): {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=['Interictal', 'Ictal']))
    print("\nMatriz de Confusión:")
    print("                Predicción")
    print("              Interictal  Ictal")
    print(f"Interictal      {cm[0,0]:6d}  {cm[0,1]:4d}")
    print(f"Ictal           {cm[1,0]:6d}  {cm[1,1]:4d}")
    
    # Preparar resultados para el dashboard
    resultados = {
        'accuracy': float(accuracy),
        'confusion_matrix': cm.tolist(),
        'classification_report': report,
        'n_train': int(X_train.shape[0]),
        'n_test': int(X_test.shape[0]),
        'n_features': int(X_train.shape[1]),
        'y_test': y_test.tolist(),
        'y_pred': y_pred.tolist()
    }
    
    # Guardar resultados
    with open('resultados_clasificacion.json', 'w') as f:
        json.dump(resultados, f, indent=2)
    
    print("\nResultados guardados en 'resultados_clasificacion.json'")
    
    return resultados, clf, scaler

if __name__ == "__main__":
    # Cargar datos procesados
    datos = np.load('datos_procesados.npz')
    matriz_caracteristicas = datos['caracteristicas']
    etiquetas = datos['etiquetas']
    
    resultados, clf, scaler = clasificar_datos(matriz_caracteristicas, etiquetas)

