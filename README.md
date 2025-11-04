# Sales Data Processing System

Enterprise-grade data processing and feature engineering system for sales analytics. Automated data cleaning, validation, and feature generation pipeline designed for production environments.

## Overview

The Sales Data Processing System provides a robust, production-ready solution for transforming raw sales data into analysis-ready datasets. The system includes automated data validation, comprehensive cleaning procedures, and advanced feature engineering capabilities optimized for machine learning and business intelligence applications.

## Features

### Data Processing
- Automated data cleaning with duplicate removal and null value handling
- Schema validation and required column verification
- Date normalization and temporal feature extraction
- Support for local file and remote URL data sources

### Feature Engineering
- Temporal features: year, month, day, day of week, weekend indicators, seasonal encoding
- Product features: automatic categorization, brand extraction, text analysis
- Pricing features: total amount, unit price, logarithmic transformations, category averages
- RFM analysis: recency, frequency, and monetary value calculations (when customer data available)
- Cyclical encoding for temporal patterns
- Missing value indicators

### Operational Features
- Comprehensive logging system with timestamped files
- Error handling and validation at multiple stages
- Relative path configuration for cross-platform compatibility
- Automatic output file naming with timestamps for versioning

## Requirements

- Python 3.8 or higher
- pandas >= 2.0.0
- numpy >= 1.24.0

## Installation

### Prerequisites

Ensure Python 3.8+ is installed on your system:

```bash
python --version
```

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Leer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

For production environments, consider using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Basic Execution

Run the main processing script:

```bash
python src/main.py
```

The system will prompt you to select a data source:
- Option 1: Load from local file (default: `Data/Raw/ventas.csv`)
- Option 2: Load from remote URL

### Input Data Requirements

#### Required Columns
- `fecha`: Transaction date (format: YYYY-MM-DD)

#### Optional Columns
- `precio`: Product price (numeric)
- `unidades`: Quantity sold (numeric)
- `producto`: Product name or identifier (string)
- `cliente_id`: Customer identifier (string or numeric)
- `tienda`: Store name or identifier (string)
- `promocion`: Promotion indicator (0 or 1)

#### Example Input Format

```csv
fecha,producto,tienda,unidades,precio,promocion
2024-01-01,A,Centro,12,9.99,0
2024-01-02,A,Centro,15,9.99,1
2024-01-03,B,Sur,8,19.99,0
```

### Output

Processed data is automatically saved to:
```
Data/processed/ventas_limpias_YYYYMMDD_HHMMSS.csv
```

Each execution generates a timestamped output file to maintain processing history and enable version tracking.

## Generated Features

### Temporal Features
- `anio`: Year extracted from date
- `mes`: Month (1-12)
- `dia`: Day of month
- `dia_semana`: Day of week name
- `es_fin_de_semana`: Boolean weekend indicator
- `estacion`: Season (verano, otoño, invierno, primavera)
- `mes_sin`, `mes_cos`: Cyclical encoding of month (sine/cosine)

### Product Features
- `categoria`: Automatic product categorization (electrónica, hogar, otros)
- `producto_len`: Product name length
- `producto_has_num`: Boolean indicating numeric characters in product name
- `producto_brand`: Extracted brand name (if detected)

### Pricing Features
- `importe_total`: Total transaction amount (precio × unidades)
- `precio_unitario`: Price per unit
- `log_importe_total`: Logarithmic transformation of total amount
- `precio_medio_categoria`: Average price by product category

### RFM Features (requires cliente_id)
- `recency`: Days since last purchase
- `frequency`: Purchase frequency count
- `monetary`: Total monetary value per customer

### Missing Value Indicators
- `precio_missing`: Boolean flag for missing price values
- `unidades_missing`: Boolean flag for missing unit values
- `producto_missing`: Boolean flag for missing product values
- `fecha_missing`: Boolean flag for missing date values

## Project Structure

```
Leer/
├── src/
│   ├── main.py              # Main processing script
│   ├── features.py          # Feature engineering module
│   └── __init__.py          # Package initialization
├── Data/
│   ├── Raw/                 # Input data directory
│   └── processed/           # Output data directory
├── Logs/                    # Log files directory
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## Logging

All operations are logged with timestamps to files in the `Logs/` directory:

```
Logs/log_YYYYMMDD_HHMMSS.txt
```

Log entries include:
- Data loading status and source information
- Data validation results
- Cleaning operation statistics
- Feature generation details
- Error messages and warnings
- Processing completion status

Log levels: INFO, WARNING, ERROR

## Error Handling

The system implements comprehensive error handling:

- **Schema Validation**: Verifies required columns before processing
- **File Not Found**: Clear error messages for missing input files
- **Empty Data**: Detection and reporting of empty or corrupted files
- **Invalid Dates**: Automatic removal of rows with invalid date formats
- **Type Errors**: Handling of unexpected data types

All errors are logged with full traceback information for debugging.

## Data Processing Pipeline

1. **Data Loading**: Load from local file or remote URL
2. **Schema Validation**: Verify required columns are present
3. **Data Cleaning**:
   - Date normalization and validation
   - Duplicate removal
   - Null value handling (mean imputation for numeric, 'Desconocido' for text)
4. **Feature Engineering**: Generate temporal, product, pricing, and RFM features
5. **Output Generation**: Save processed data with timestamp

## Configuration

The system uses relative paths based on the project structure. All paths are automatically calculated from the script location, ensuring cross-platform compatibility.

Default paths:
- Input: `Data/Raw/ventas.csv`
- Output: `Data/processed/`
- Logs: `Logs/`

## Performance Considerations

- Vectorized operations for efficient processing
- Optional column handling to avoid unnecessary computations
- Memory-efficient data processing with pandas
- Suitable for datasets up to several million rows

## Security

- Input validation to prevent path traversal attacks
- Safe handling of user-provided URLs
- No execution of external code or scripts
- Comprehensive logging for audit trails

## Testing

To verify installation:

```bash
python src/main.py
```

Select option 1 and ensure `Data/Raw/ventas.csv` exists with proper format.

## Troubleshooting

### Common Issues

**FileNotFoundError**: Ensure the input file exists in `Data/Raw/` directory or provide correct path.

**ValueError - Missing Columns**: Verify your CSV contains at least the `fecha` column.

**Empty Output**: Check input data format and ensure dates are valid (YYYY-MM-DD).

**Import Errors**: Verify all dependencies are installed: `pip install -r requirements.txt`

## Support

For technical support or feature requests, contact the development team.

## License

[Specify license]

## Version

Current Version: 1.0.0

## Changelog

### Version 1.0.0
- Initial release
- Core data processing functionality
- Feature engineering module
- Logging system
- Schema validation
