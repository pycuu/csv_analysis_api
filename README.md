# CSV Data Analysis API

## Overview
This is a FastAPI-based application that provides various data analysis operations on CSV files. Users can upload a CSV file and perform calculations such as mean, median, standard deviation, correlation, and linear regression.

## Features
- Upload and preview CSV data
- Calculate the mean of a specified column
- Calculate the median of a specified column
- Calculate the standard deviation of a specified column
- Compute Pearson correlation between two columns
- Perform linear regression on two columns

## Installation
### Prerequisites
- Python 3.8+
- Pip

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Running the API
Run the FastAPI server with:
```sh
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Access the interactive API documentation at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### 1. Upload CSV File
**Endpoint:** `POST /upload-csv/`
**Description:** Uploads a CSV file and returns a preview of the data.

### 2. Compute Mean
**Endpoint:** `POST /mean_value/`
**Parameters:**
- `file` (CSV file)
- `column` (str) - The column name for which the mean is calculated.

### 3. Compute Median
**Endpoint:** `POST /median_value/`
**Parameters:**
- `file` (CSV file)
- `column` (str) - The column name for which the median is calculated.

### 4. Compute Standard Deviation
**Endpoint:** `POST /standard_deviation/`
**Parameters:**
- `file` (CSV file)
- `column` (str) - The column name for which the standard deviation is calculated.

### 5. Compute Pearson Correlation
**Endpoint:** `POST /correlation/`
**Parameters:**
- `file` (CSV file)
- `x_column` (str) - The first column name.
- `y_column` (str) - The second column name.

### 6. Perform Linear Regression
**Endpoint:** `POST /linear_regression/`
**Parameters:**
- `file` (CSV file)
- `x_column` (str) - The independent variable.
- `y_column` (str) - The dependent variable.

**Response Example:**
```json
{
  "filename": "data.csv",
  "x_column": "X",
  "y_column": "Y",
  "linear_regression": {
    "slope": 1.23,
    "intercept": 4.56,
    "r_squared": 0.89,
    "mean_squared_error": 2.34,
    "root_mean_squared_error": 1.53,
    "mean_absolute_error": 1.12
  }
}
```

## License
This project is open-source and available under the MIT License.

