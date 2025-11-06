"""
Excepciones personalizadas para el sistema de procesamiento de datos.
"""


class DataProcessingError(Exception):
    """Excepción base para errores en el procesamiento de datos."""
    pass


class ValidationError(DataProcessingError):
    """Error cuando falla la validación de datos."""
    pass


class SchemaValidationError(ValidationError):
    """Error cuando el esquema de datos no cumple con los requisitos."""
    
    def __init__(self, message: str, missing_columns: list = None):
        super().__init__(message)
        self.missing_columns = missing_columns or []


class DataQualityError(ValidationError):
    """Error cuando la calidad de los datos no es aceptable."""
    
    def __init__(self, message: str, quality_issues: dict = None):
        super().__init__(message)
        self.quality_issues = quality_issues or {}


class FileLoadError(DataProcessingError):
    """Error al cargar un archivo."""
    pass


class EmptyDataError(DataProcessingError):
    """Error cuando el DataFrame está vacío después del procesamiento."""
    pass

