import pandas as pd
import os

ruta = r"C:\Users\roger\Desktop\Python\Leer\Data\Raw\ventas.csv"

try:
    # Cargar el archivo CSV 
    df = pd.read_csv(ruta)
    print("✅ Archivo cargado correctamente\n")

    print("Primeras filas:\n", df.head(), "\n")
    print("Resumen estadístico:\n", df.describe(), "\n")

    # Limpieza de datos ---
    # Convertir la columna 'fecha' a tipo datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Eliminar filas con fecha inválida
    df = df.dropna(subset=['fecha'])

    # Eliminar duplicados si los hay
    df = df.drop_duplicates()

    # Rellenar valores faltantes numéricos con la media
    for col in df.select_dtypes(include=['float64', 'int64']):
        df[col] = df[col].fillna(df[col].mean())

    # Rellenar valores faltantes de texto con "Desconocido"
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].fillna('Desconocido')

    # Normalizar texto (ejemplo: nombres de productos)
    if 'producto' in df.columns:
        df['producto'] = df['producto'].str.strip().str.lower()

    # Crear nuevas columnas temporales
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.day_name()

    print("\n✅ Datos después de limpieza y preparación:\n")
    print(df.head())

    if 'producto' in df.columns and 'unidades' in df.columns:
        print("\n📊 Promedio de unidades vendidas por producto:\n")
        print(df.groupby("producto")["unidades"].mean())


    # Guardar datos limpios
    ruta_salida_dir = r"C:\Users\roger\Desktop\Python\Leer\Data\processed"
    os.makedirs(ruta_salida_dir, exist_ok=True)  # crea la carpeta si no existe

    ruta_salida = os.path.join(ruta_salida_dir, "ventas_limpias.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"\n💾 Datos limpios guardados en: {ruta_salida}")    

except FileNotFoundError:
    print(f"❌ No se encontró el archivo: {ruta}")
except pd.errors.EmptyDataError:
    print("⚠️ El archivo está vacío o corrupto.")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")
