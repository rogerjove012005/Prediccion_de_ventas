# src/__init__.py

# Importar funciones comunes (opcional)
from .features import crear_features
from .validation import validar_esquema, validar_calidad_datos, validar_despues_limpieza
from .exceptions import (
    DataProcessingError,
    ValidationError,
    SchemaValidationError,
    DataQualityError,
    FileLoadError,
    EmptyDataError
)

# Definir versión del paquete (buena práctica)
__version__ = "1.0.0"

