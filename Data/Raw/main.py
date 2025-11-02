import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import shutil  # para eliminar carpetas

# Configuración de rutas 
ruta_local = r"C:\Users\roger\Desktop\Python\Leer\Data\Raw\ventas.csv"
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
ruta_salida_dir = r"C:\Users\roger\Desktop\Python\Leer\Data\processed"

print("=== Fuente de datos ===")
print("1️⃣  Archivo local")
print("2️⃣  URL remota")
opcion = input("Elige una opción (1 o 2): ").strip()

try:
    # Cargar CSV según elección 
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
    print("Resumen estadístico:\n", df.describe(include='all'), "\n")

    # Limpieza de datos 
    if 'fecha' in df.columns:
        # Convierte fechas y elimina las inválidas
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])
        # Crea columnas auxiliares de fecha
        df['mes'] = df['fecha'].dt.month
        df['dia_semana'] = df['fecha'].dt.day_name()

    # Elimina duplicados
    df = df.drop_duplicates()

    # Rellena valores faltantes numéricos con la media
    for col in df.select_dtypes(include=['float64', 'int64']):
        df[col] = df[col].fillna(df[col].mean())

    # Rellena valores faltantes de texto con "Desconocido"
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].fillna('Desconocido')

    print("\n✅ Datos después de limpieza y validación:\n")
    print(df.head())

    # Guardar datos limpios 
    os.makedirs(ruta_salida_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_salida = os.path.join(ruta_salida_dir, f"ventas_limpias_{timestamp}.csv")

    df.to_csv(ruta_salida, index=False)
    print(f"\n💾 Datos limpios guardados en: {ruta_salida}")

    # Visualización rápida 
    if 'producto' in df.columns and 'unidades' in df.columns:
        df.groupby('producto')['unidades'].sum().plot(kind='bar')
        plt.title('Unidades vendidas por producto')
        plt.xlabel('Producto')
        plt.ylabel('Unidades')
        plt.tight_layout()
        plt.show()

    # Sistema de limpieza de la carpeta processed 
    print("\n🗑️ ¿Quieres eliminar todos los archivos procesados?")
    print("1️⃣  Sí, eliminar")
    print("2️⃣  No, conservar")
    eliminar = input("Elige una opción (1 o 2): ").strip()

    if eliminar == "1":
        if os.path.exists(ruta_salida_dir):
            shutil.rmtree(ruta_salida_dir)
            print(f"✅ Carpeta '{ruta_salida_dir}' eliminada correctamente.")
        else:
            print("⚠️ La carpeta ya no existe o no contiene archivos.")
    else:
        print("🟢 Archivos procesados conservados.")

# Manejo de errores 
except FileNotFoundError as e:
    print(f"❌ {e}")
except pd.errors.EmptyDataError:
    print("⚠️ El archivo está vacío o corrupto.")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")
