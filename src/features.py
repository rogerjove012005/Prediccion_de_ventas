import pandas as pd
import numpy as np

def crear_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea nuevas variables (features) optimizadas y más robustas.
    
    Genera features temporales, de producto, de precio, RFM y flags de valores
    faltantes basándose en las columnas disponibles en el DataFrame.
    
    Args:
        df: DataFrame con datos de ventas. Debe contener al menos la columna 'fecha'.
            Columnas opcionales: 'precio', 'unidades', 'producto', 'cliente_id'.
    
    Returns:
        DataFrame con las features adicionales creadas. El DataFrame original
        no se modifica (se retorna una copia).
    """
    # validar df
    if df is None or len(df) == 0:
        return df

    df = df.copy()

    # columnas disponibles
    has_fecha = 'fecha' in df.columns
    has_precio = 'precio' in df.columns
    has_unidades = 'unidades' in df.columns
    has_producto = 'producto' in df.columns
    has_cliente = 'cliente_id' in df.columns

    # normalizar fecha
    if has_fecha:
        df.loc[:, 'fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df.loc[:, 'anio'] = df['fecha'].dt.year
        df.loc[:, 'mes'] = df['fecha'].dt.month
        df.loc[:, 'dia'] = df['fecha'].dt.day
        df.loc[:, 'dia_semana'] = df['fecha'].dt.day_name()

    # importe_total
    if has_precio and has_unidades:
        df.loc[:, 'importe_total'] = df['precio'] * df['unidades']

    # categoria producto (vectorizado)
    if has_producto:
        prod = df['producto'].fillna('').astype(str).str.lower()
        cond_elec = prod.str.contains(r'\b(tv|smart|phone|laptop|tablet)\b', regex=True)
        cond_hogar = prod.str.contains(r'\b(silla|mesa|sofa|cama)\b', regex=True)
        df.loc[:, 'categoria'] = np.select([cond_elec, cond_hogar], ['electrónica', 'hogar'], default='otros')

    # precio_unitario y log importe
    if has_precio and has_unidades:
        df.loc[:, 'precio_unitario'] = np.where(df['unidades'] > 0, df['precio'] / df['unidades'], np.nan)
        df.loc[:, 'log_importe_total'] = np.log1p(df['importe_total'].fillna(0))

    # features temporales adicionales
    if has_fecha:
        df.loc[:, 'es_fin_de_semana'] = df['fecha'].dt.weekday >= 5
        # codificación cíclica del mes (si mes existe)
        if 'mes' in df.columns and df['mes'].notna().any():
            df.loc[:, 'mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
            df.loc[:, 'mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)
            estaciones = {12: 'verano', 1: 'verano', 2: 'verano',
                          3: 'otoño', 4: 'otoño', 5: 'otoño',
                          6: 'invierno', 7: 'invierno', 8: 'invierno',
                          9: 'primavera', 10: 'primavera', 11: 'primavera'}
            df.loc[:, 'estacion'] = df['mes'].map(estaciones)

    # features de texto del producto (vectorizados)
    if has_producto:
        prod = df['producto'].fillna('').astype(str)
        df.loc[:, 'producto_len'] = prod.str.len()
        df.loc[:, 'producto_has_num'] = prod.str.contains(r'\d', regex=True)
        brands = ['sony', 'samsung', 'lg', 'panasonic']
        brand_pattern = r'(' + '|'.join(brands) + r')'
        df.loc[:, 'producto_brand'] = prod.str.lower().str.extract(brand_pattern, expand=False).fillna('other')

    # precio medio por categoria (solo si existen)
    if 'categoria' in df.columns and has_precio:
        df.loc[:, 'precio_medio_categoria'] = df.groupby('categoria')['precio'].transform('mean')

    # flags de nulos
    for col in ['precio', 'unidades', 'producto', 'fecha']:
        if col in df.columns:
            df.loc[:, f'{col}_missing'] = df[col].isna()

    # RFM simple usando map en lugar de merge
    if has_cliente and has_fecha:
        ref_date = df['fecha'].max() + pd.Timedelta(days=1)
        grouped = df.groupby('cliente_id').agg(
            recency_days=('fecha', lambda x: (ref_date - x.max()).days),
            frequency=('fecha', 'count'),
            monetary=('importe_total', 'sum')
        )
        # mapear al df para evitar merge completo
        df.loc[:, 'recency'] = df['cliente_id'].map(grouped['recency_days'])
        df.loc[:, 'frequency'] = df['cliente_id'].map(grouped['frequency'])
        df.loc[:, 'monetary'] = df['cliente_id'].map(grouped['monetary'])

    return df
