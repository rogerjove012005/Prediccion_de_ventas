import pandas as pd
import os
from features import crear_features  # importar el módulo de features

# --- Configuración de rutas ---
ruta_local = r"C:\Users\roger\Desktop\Python\Leer\Data\Raw\ventas.csv"
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
ruta_salida_dir = r"C:\Users\roger\Desktop\Python\Leer\Data\processed"

print("=== Fuente de datos ===")
print("1️⃣  Archivo local")
print("2️⃣  URL remota")
opcion = input("Elige una opción (1 o 2): ").strip()

try:
    # --- Cargar CSV según elección ---
    if opcion == "1":
        if os.path.exists(ruta_local):
            print("\n📂 Cargando datos desde archivo local...\n")
            df = pd.read_csv(ruta_local)
        else:
            raise FileNotFoundError(f"No se encontró el archivo local en: {ruta_local}")
    elif opcion == "2":
        print("\n🌐 Cargando datos desde URL remota...\n")
        df = pd.read_csv(url)
    else:
        raise ValueError("Opción no válida. Debes elegir 1 o 2.")

    print("✅ Archivo cargado correctamente\n")
    print("Primeras filas:\n", df.head(), "\n")
    print("Resumen estadístico:\n", df.describe(include='all', datetime_is_numeric=True), "\n")

    # --- Limpieza de datos ---
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])
        df = df.drop_duplicates()

    for col in df.select_dtypes(include=['float64', 'int64']):
        df[col] = df[col].fillna(df[col].mean())

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].fillna('Desconocido')

    print("\n✅ Datos limpios:\n")
    print(df.head())

    # --- Crear nuevas variables ---
    df = crear_features(df)
    print("\n✨ Nuevas variables creadas con éxito:\n")
    print(df.head())

    # --- Guardar datos procesados ---
    os.makedirs(ruta_salida_dir, exist_ok=True)
    ruta_salida = os.path.join(ruta_salida_dir, "ventas_limpias.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"\n💾 Datos procesados guardados en: {ruta_salida}")

except FileNotFoundError as e:
    print(f"❌ {e}")
except pd.errors.EmptyDataError:
    print("⚠️ El archivo está vacío o corrupto.")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")
