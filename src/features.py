import pandas as pd

def crear_features(df):
    """
    Crea nuevas variables (features) derivadas de las columnas existentes.
    """

    # --- Variables temporales (si hay fecha) ---
    if 'fecha' in df.columns:
        df['anio'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['dia'] = df['fecha'].dt.day
        df['dia_semana'] = df['fecha'].dt.day_name()

    # --- Variable de importe total ---
    if 'precio' in df.columns and 'unidades' in df.columns:
        df['importe_total'] = df['precio'] * df['unidades']

    # --- Clasificación simple por tipo de producto ---
    if 'producto' in df.columns:
        df['categoria'] = df['producto'].apply(
            lambda x: 'electrónica' if 'tv' in x.lower() or 'smart' in x.lower()
            else 'hogar' if 'silla' in x.lower() or 'mesa' in x.lower()
            else 'otros'
        )

    return df
