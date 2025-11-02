import pandas as pd
import os

# --- Configuración de rutas ---
ruta_local = r"C:\Users\roger\Desktop\Python\Leer\Data\Raw\ventas_reales.csv"
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"

try:
    # --- Intentar cargar archivo local ---
    if os.path.exists(ruta_local):
        print("📂 Cargando datos desde archivo local...\n")
        df = pd.read_csv(ruta_local)
    else:
        print("🌐 Archivo local no encontrado, intentando cargar desde URL...\n")
        df = pd.read_csv(url)

    print("✅ Archivo cargado correctamente\n")
    print("Primeras filas:\n", df.head(), "\n")
    print("Resumen estadístico:\n", df.describe(), "\n")

    # --- Limpieza básica ---
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])
        df['mes'] = df['fecha'].dt.month
        df['dia_semana'] = df['fecha'].dt.day_name()

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Rellenar valores faltantes numéricos con la media
    for col in df.select_dtypes(include=['float64', 'int64']):
        df[col] = df[col].fillna(df[col].mean())

    # Rellenar texto faltante
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].fillna('Desconocido')

    print("\n✅ Datos después de limpieza y preparación:\n")
    print(df.head())

    # --- Guardar datos limpios ---
    ruta_salida_dir = r"C:\Users\roger\Desktop\Python\Leer\Data\processed"
    os.makedirs(ruta_salida_dir, exist_ok=True)

    ruta_salida = os.path.join(ruta_salida_dir, "ventas_limpias.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"\n💾 Datos limpios guardados en: {ruta_salida}")

except pd.errors.EmptyDataError:
    print("⚠️ El archivo está vacío o corrupto.")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")
