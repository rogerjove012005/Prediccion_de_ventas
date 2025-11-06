"""
Módulo de validación de datos para el sistema de procesamiento.
"""

import pandas as pd
import logging
from typing import List, Dict, Optional
from .exceptions import SchemaValidationError, DataQualityError, EmptyDataError


def validar_esquema(df: pd.DataFrame, columnas_requeridas: List[str]) -> None:
    """
    Valida que el DataFrame contenga las columnas requeridas.
    
    Args:
        df: DataFrame a validar.
        columnas_requeridas: Lista de nombres de columnas que deben estar presentes.
    
    Raises:
        SchemaValidationError: Si faltan columnas requeridas.
        EmptyDataError: Si el DataFrame está vacío.
    """
    if df is None:
        raise EmptyDataError("El DataFrame es None.")
    
    if len(df) == 0:
        raise EmptyDataError("El DataFrame está vacío.")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Se esperaba un DataFrame, se recibió: {type(df)}")
    
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        raise SchemaValidationError(
            f"Columnas requeridas faltantes: {columnas_faltantes}. "
            f"El archivo debe contener al menos: {columnas_requeridas}",
            missing_columns=columnas_faltantes
        )


def validar_calidad_datos(df: pd.DataFrame, logger: Optional[logging.Logger] = None) -> Dict[str, any]:
    """
    Valida la calidad de los datos y retorna un reporte.
    
    Args:
        df: DataFrame a validar.
        logger: Logger opcional para registrar advertencias.
    
    Returns:
        Diccionario con métricas de calidad de datos.
    
    Raises:
        DataQualityError: Si la calidad de los datos es inaceptable.
    """
    if df is None or len(df) == 0:
        raise EmptyDataError("No se puede validar un DataFrame vacío.")
    
    issues = {}
    warnings = []
    
    # Verificar duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        warnings.append(f"Se encontraron {duplicados} filas duplicadas")
        issues['duplicados'] = duplicados
    
    # Verificar valores nulos por columna
    nulos_por_columna = df.isnull().sum()
    columnas_con_nulos = nulos_por_columna[nulos_por_columna > 0]
    
    if len(columnas_con_nulos) > 0:
        porcentaje_nulos = (columnas_con_nulos / len(df)) * 100
        columnas_criticas = porcentaje_nulos[porcentaje_nulos > 50].index.tolist()
        
        if columnas_criticas:
            issues['columnas_criticas_nulos'] = {
                col: float(porcentaje_nulos[col]) 
                for col in columnas_criticas
            }
            warnings.append(
                f"Columnas con más del 50% de valores nulos: {columnas_criticas}"
            )
        
        issues['nulos_por_columna'] = nulos_por_columna.to_dict()
    
    # Validar fechas si existe la columna
    if 'fecha' in df.columns:
        fechas_invalidas = pd.to_datetime(df['fecha'], errors='coerce').isna().sum()
        if fechas_invalidas > 0:
            porcentaje_fechas_inv = (fechas_invalidas / len(df)) * 100
            issues['fechas_invalidas'] = {
                'cantidad': int(fechas_invalidas),
                'porcentaje': float(porcentaje_fechas_inv)
            }
            if porcentaje_fechas_inv > 50:
                warnings.append(
                    f"Advertencia: {porcentaje_fechas_inv:.1f}% de fechas son inválidas"
                )
    
    # Validar valores numéricos negativos donde no deberían
    columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    for col in columnas_numericas:
        if col in ['precio', 'unidades', 'importe_total']:
            valores_negativos = (df[col] < 0).sum()
            if valores_negativos > 0:
                issues[f'{col}_negativos'] = int(valores_negativos)
                warnings.append(
                    f"Se encontraron {valores_negativos} valores negativos en '{col}'"
                )
    
    # Registrar advertencias si hay logger
    if logger:
        for warning in warnings:
            logger.warning(f"⚠️ {warning}")
    
    # Reporte de calidad
    reporte = {
        'total_filas': len(df),
        'total_columnas': len(df.columns),
        'issues': issues,
        'warnings': warnings,
        'calidad_aceptable': len([k for k in issues.keys() 
                                  if k in ['columnas_criticas_nulos', 'fechas_invalidas'] 
                                  and issues.get(k, {}).get('porcentaje', 0) > 50]) == 0
    }
    
    return reporte


def validar_despues_limpieza(df: pd.DataFrame, logger: Optional[logging.Logger] = None) -> None:
    """
    Valida que después de la limpieza el DataFrame aún tenga datos válidos.
    
    Args:
        df: DataFrame después de la limpieza.
        logger: Logger opcional.
    
    Raises:
        EmptyDataError: Si el DataFrame quedó vacío después de la limpieza.
        DataQualityError: Si la calidad sigue siendo inaceptable.
    """
    if df is None or len(df) == 0:
        raise EmptyDataError(
            "El DataFrame quedó vacío después de la limpieza. "
            "Revisa los datos de entrada."
        )
    
    # Validar que al menos tenga la columna fecha
    if 'fecha' in df.columns:
        fechas_validas = df['fecha'].notna().sum()
        if fechas_validas == 0:
            raise DataQualityError(
                "No quedaron fechas válidas después de la limpieza.",
                quality_issues={'fechas_validas': 0}
            )
    
    if logger:
        logger.info(f"✅ Validación post-limpieza: {len(df)} filas válidas")

