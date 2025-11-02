import os
import pandas as pd

# Ruta al archivo de ventas CSV
ruta = r"C:\Users\roger\Desktop\Python\Leer\Data\ventas.csv"

try:
    df = pd.read_csv(ruta)
    print("✅ Archivo cargado correctamente\n")
    print("Primeras filas:\n", df.head(), "\n")
    print("Resumen estadístico:\n", df.describe(), "\n")

    # Limpieza y preparación básica 
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])  # elimina filas sin fecha válida
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.day_name()

    print("\nDatos después de limpieza y preparación:\n")
    print(df.head())

    print("Promedio de unidades por producto:")
    print(df.groupby("producto")["unidades"].mean())

except FileNotFoundError:
    print(f" No se encontró el archivo: {ruta}")
except pd.errors.EmptyDataError:
    print(" El archivo está vacío o corrupto.")
except Exception as e:
    print(f" Ocurrió un error inesperado: {e}")
