import pandas as pd
import os
import logging
from datetime import datetime
from features import crear_features  # importar el módulo de features

# --- Configuración de rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_local = os.path.join(BASE_DIR, "Data", "Raw", "ventas.csv")
url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
ruta_salida_dir = os.path.join(BASE_DIR, "Data", "processed")
ruta_logs_dir = os.path.join(BASE_DIR, "Logs")


def configurar_logging():
    """
    Configura el sistema de logging para escribir en archivo y consola.
    """
    # Crear directorio de logs si no existe
    os.makedirs(ruta_logs_dir, exist_ok=True)
    
    # Crear nombre de archivo de log con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_log = os.path.join(ruta_logs_dir, f"log_{timestamp}.txt")
    
    # Configurar formato de logging
    formato_log = '[%(asctime)s] %(levelname)s: %(message)s'
    formato_fecha = '%H:%M:%S'
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format=formato_log,
        datefmt=formato_fecha,
        handlers=[
            logging.FileHandler(archivo_log, encoding='utf-8'),
            logging.StreamHandler()  # Consola
        ]
    )
    
    return archivo_log


def main():
    """Función principal del procesamiento de datos."""
    # Configurar logging al inicio
    archivo_log = configurar_logging()
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("Sistema de logging inicializado")
    logger.info(f"Archivo de log: {archivo_log}")

    logger.info("=== Fuente de datos ===")
    logger.info("1️⃣  Archivo local")
    logger.info("2️⃣  URL remota")
    opcion = input("Elige una opción (1 o 2): ").strip()

    try:
        # --- Cargar CSV según elección ---
        if opcion == "1":
            if os.path.exists(ruta_local):
                logger.info("📂 Cargando datos desde archivo local...")
                df = pd.read_csv(ruta_local)
            else:
                raise FileNotFoundError(f"No se encontró el archivo local en: {ruta_local}")
        elif opcion == "2":
            logger.info("🌐 Cargando datos desde URL remota...")
            df = pd.read_csv(url)
        else:
            raise ValueError("Opción no válida. Debes elegir 1 o 2.")

        logger.info("✅ Archivo cargado correctamente")
        logger.info(f"Dimensiones iniciales: {df.shape}")
        logger.info(f"Columnas encontradas: {list(df.columns)}")
        logger.info(f"Primeras filas:\n{df.head()}")
        logger.info(f"Resumen estadístico:\n{df.describe(include='all')}")

        # --- Limpieza de datos ---
        logger.info("Iniciando limpieza de datos...")
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            filas_antes = len(df)
            df = df.dropna(subset=['fecha'])
            filas_despues = len(df)
            if filas_antes != filas_despues:
                logger.warning(f"Se eliminaron {filas_antes - filas_despues} filas con fechas inválidas")
            
            duplicados = df.duplicated().sum()
            df = df.drop_duplicates()
            if duplicados > 0:
                logger.warning(f"Se eliminaron {duplicados} filas duplicadas")

        for col in df.select_dtypes(include=['float64', 'int64']):
            nulos = df[col].isna().sum()
            if nulos > 0:
                df[col] = df[col].fillna(df[col].mean())
                logger.info(f"Columnas numéricas '{col}': {nulos} valores nulos rellenados con la media")

        for col in df.select_dtypes(include=['object']):
            nulos = df[col].isna().sum()
            if nulos > 0:
                df[col] = df[col].fillna('Desconocido')
                logger.info(f"Columnas de texto '{col}': {nulos} valores nulos rellenados con 'Desconocido'")

        logger.info("✅ Datos limpios")
        logger.info(f"Dimensiones finales: {df.shape}")
        logger.info(f"Primeras filas:\n{df.head()}")

        # --- Crear nuevas variables ---
        logger.info("Creando nuevas variables (features)...")
        df = crear_features(df)
        logger.info(f"✨ Nuevas variables creadas con éxito. Columnas totales: {len(df.columns)}")
        logger.info(f"Columnas finales: {list(df.columns)}")
        logger.info(f"Primeras filas:\n{df.head()}")

        # --- Guardar datos procesados ---
        os.makedirs(ruta_salida_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"ventas_limpias_{timestamp}.csv"
        ruta_salida = os.path.join(ruta_salida_dir, nombre_archivo)
        df.to_csv(ruta_salida, index=False)
        logger.info(f"💾 Datos procesados guardados en: {ruta_salida}")
        logger.info("=" * 50)
        logger.info("Proceso completado exitosamente")

    except FileNotFoundError as e:
        logger.error(f"❌ Error de archivo no encontrado: {e}")
    except pd.errors.EmptyDataError:
        logger.error("⚠️ El archivo está vacío o corrupto.")
    except ValueError as e:
        logger.error(f"❌ Error de valor: {e}")
    except Exception as e:
        logger.error(f"⚠️ Ocurrió un error inesperado: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
