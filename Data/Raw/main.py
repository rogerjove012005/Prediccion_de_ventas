import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Configuración de rutas 
ruta_local = r"C:\Users\roger\Desktop\Python\Leer\Data\Raw\ventas.csv"
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"

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
    print("Resumen estadístico:\n", df.describe(include='all', datetime_is_numeric=True), "\n")

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

    # Validación de datos 
    # Corrige valores negativos en unidades o precios
    if 'unidades' in df.columns and (df['unidades'] < 0).any():
        print("⚠️ Se encontraron unidades negativas. Se reemplazan por 0.")
        df['unidades'] = df['unidades'].clip(lower=0)

    if 'precio' in df.columns and (df['precio'] < 0).any():
        print("⚠️ Se encontraron precios negativos. Se reemplazan por la media.")
        df['precio'] = df['precio'].apply(lambda x: df['precio'].mean() if x < 0 else x)

    print("\n✅ Datos después de limpieza y validación:\n")
    print(df.head())

    # Resumen de calidad de datos 
    print("\n📊 Resumen de calidad de datos:")
    print(f"Filas totales: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    print(f"Valores nulos por columna:\n{df.isnull().sum()}\n")

    # Agrupaciones útiles 
    if 'producto' in df.columns and 'unidades' in df.columns:
        print("Promedio de unidades por producto:")
        print(df.groupby('producto')['unidades'].mean())

    if 'mes' in df.columns and 'unidades' in df.columns:
        print("\nVentas promedio por mes:")
        print(df.groupby('mes')['unidades'].mean())

    # Guardar datos limpios 
    ruta_salida_dir = r"C:\Users\roger\Desktop\Python\Leer\Data\processed"
    os.makedirs(ruta_salida_dir, exist_ok=True)

    # Genera nombre con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_salida = os.path.join(ruta_salida_dir, f"ventas_limpias_{timestamp}.csv")

    # Guarda CSV limpio
    df.to_csv(ruta_salida, index=False)
    print(f"\n💾 Datos limpios guardados en: {ruta_salida}")

    # Guardar reporte de limpieza 
    reporte_path = os.path.join(ruta_salida_dir, f"reporte_limpieza_{timestamp}.txt")
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("=== REPORTE DE LIMPIEZA ===\n")
        f.write(f"Fecha de procesamiento: {datetime.now()}\n\n")
        f.write(f"Filas finales: {len(df)}\n")
        f.write(f"Columnas: {list(df.columns)}\n\n")
        f.write("Valores nulos por columna:\n")
        f.write(str(df.isnull().sum()))
    print(f"📝 Reporte guardado en: {reporte_path}")

    # Visualización rápida 
    if 'producto' in df.columns and 'unidades' in df.columns:
        df.groupby('producto')['unidades'].sum().plot(kind='bar')
        plt.title('Unidades vendidas por producto')
        plt.xlabel('Producto')
        plt.ylabel('Unidades')
        plt.tight_layout()
        plt.show()

# Manejo de errores 
except FileNotFoundError as e:
    print(f"❌ {e}")
except pd.errors.EmptyDataError:
    print("⚠️ El archivo está vacío o corrupto.")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")
