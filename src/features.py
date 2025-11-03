import pandas as pd
import numpy as np

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

    # --- Nuevos features añadidos ---
    # precio por unidad y log de importe
    if 'precio' in df.columns and 'unidades' in df.columns:
        df['precio_unitario'] = np.where(df['unidades'] > 0, df['precio'] / df['unidades'], np.nan)
        df['log_importe_total'] = np.log1p(df['importe_total'].fillna(0))

    # features temporales adicionales
    if 'fecha' in df.columns:
        df['is_weekend'] = df['fecha'].dt.weekday >= 5
        # encoding cíclico del mes
        df['mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)
        # estación simple (ajustar según hemisferio)
        df['estacion'] = df['mes'].map({
            12: 'verano', 1: 'verano', 2: 'verano',
            3: 'otoño', 4: 'otoño', 5: 'otoño',
            6: 'invierno', 7: 'invierno', 8: 'invierno',
            9: 'primavera', 10: 'primavera', 11: 'primavera'
        })

    # features de texto del producto
    if 'producto' in df.columns:
        df['producto_len'] = df['producto'].str.len()
        df['producto_has_num'] = df['producto'].str.contains(r'\d', regex=True)
        brands = ['sony', 'samsung', 'lg', 'panasonic']
        df['producto_brand'] = df['producto'].apply(lambda x: next((b for b in brands if b in x.lower()), 'other'))

    # agregados por categoria
    if 'categoria' in df.columns and 'precio' in df.columns:
        df['precio_medio_categoria'] = df.groupby('categoria')['precio'].transform('mean')

    # flags de nulos para columnas clave
    for col in ['precio', 'unidades', 'producto', 'fecha']:
        if col in df.columns:
            df[f'{col}_missing'] = df[col].isna()

    # RFM simple por cliente (si existe cliente_id)
    if 'cliente_id' in df.columns and 'fecha' in df.columns:
        ref_date = df['fecha'].max() + pd.Timedelta(days=1)
        rfm = df.groupby('cliente_id').agg(
            recency=('fecha', lambda x: (ref_date - x.max()).days),
            frequency=('fecha', 'count'),
            monetary=('importe_total', 'sum')
        ).reset_index().rename(columns={'monetary': 'monetario'})
        df = df.merge(rfm, on='cliente_id', how='left')

    return df