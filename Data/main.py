import os
import pandas as pd

# Ruta al archivo de ventas CSV
ruta = r"C:\Users\roger\Desktop\Python\Leer\Data\ventas.csv"

# Verificación si el archivo existe
if not os.path.exists(ruta):
    print(f"No se encontró el archivo: {ruta}")
else:
    df = pd.read_csv(ruta)

    # Mostrar información básica
    print("✅ Archivo cargado correctamente\n")
    print("Primeras filas:\n", df.head(), "\n")
    print("Resumen estadístico:\n", df.describe(), "\n")

