# Data Analysis API

## Project Description
Data Analysis API is a Python application built with FastAPI that allows users to analyze numerical data from uploaded CSV files. The API provides statistical calculations without relying on any machine learning libraries.

## Features
The API supports the following operations (for now):
- Calculating the mean value of a selected column (`/mean_value/`)
- Calculating the median (`/median_value/`)
- Calculating the standard deviation (`/standard_deviation/`)
- Pearson correlation between two columns (`/pearson_correlation/`)
- Linear regression (`/linear_regression/`)
- Correlation matrix for the dataset (`/correlation_matrix/`)

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- Pandas
- NumPy

## Installation
To run the application locally:
```bash
# Clone the repository
git clone https://github.com/pycuu/csv_analysis_api.git
cd csv_analysis_api

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

## Usage
Once the server is running, the API will be available at:
```
http://127.0.0.1:8000
```
Interactive documentation can be accessed at:
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

## Example Usage
Each endpoint requires uploading a CSV file along with optional parameters.

### Calculating the mean value of a column
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mean_value/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@data.csv' \
  -F 'column=column_name'
```

### Linear Regression
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/linear_regression/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@data.csv' \
  -F 'X_column=x_column_name' \
  -F 'y_column=y_column_name'
```

#### Example JSON Response for Linear Regression
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

- This API does **not** use any machine learning libraries such as scikit-learn or TensorFlow. All calculations are performed using fundamental statistical formulas.
- The API only works with numerical data columns.
- Ensure that your CSV file contains valid numerical data before making requests.

