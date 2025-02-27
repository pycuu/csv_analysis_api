from fastapi import FastAPI, File, UploadFile, Form
from typing import Dict, Any
import pandas as pd
import numpy as np
import io
import uvicorn
import seaborn as sns
import matplotlib.pyplot as plt
app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# mean value of a column
@app.post("/mean_value/")
async def mean_column(file: UploadFile = File(...), column: str = Form(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    mean = df[column].mean()
    return {"mean_value": mean}


# median value of a column
@app.post("/median_value/") 
async def mean_column(file: UploadFile = File(...), column: str = Form(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    median = df[column].median()
    return {"median_value": median}



# standard deviation of a column
@app.post("/standard_deviation/")
async def mean_column(file: UploadFile = File(...), column: str = Form(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    #std_dev = (abs(pow(df[column]-(df[column].mean()),2))).mean()**(1/2)
    std_dev = df[column].std(ddof=0)
    return {"standard_deviation": std_dev}


# Pearson correlation, (-1, 1)
# Close to 0 means no correlation
@app.post("/pearson_correlation/")
async def correlation(file: UploadFile = File(...), x_column: str = Form(...), y_column: str = Form(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    if x_column not in df.columns or y_column not in df.columns:
        return {"error": "One or both columns not found in the dataset"}
    
    correlation_value = df[x_column].corr(df[y_column])

    return {"correlation": correlation_value}


# linear regression
@app.post("/linear_regression/")
async def linear_regression(file: UploadFile = File(...), X_column: str = Form(...), y_column: str = Form(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    

    if X_column not in df.columns or y_column not in df.columns:
        return {"error": "One or both columns not found in the dataset"}

    X_mean = df[X_column].mean()
    y_mean = df[y_column].mean()

    X_deviations = df[X_column] - X_mean
    y_deviations = df[y_column] - y_mean

    numerator = sum(X_deviations * y_deviations)
    denominator = sum(X_deviations ** 2)

    if denominator == 0:
        return {"error": "Denominator is zero, cannot compute slope"}

    regression_slope = numerator / denominator

    if np.isnan(regression_slope):
        return {"error": "Calculation resulted in NaN"}
    

    regression_intercept = y_mean - regression_slope*X_mean


    ss_tot = sum((df[y_column]-y_mean)**2)
    ss_res = sum((df[y_column] - (regression_slope * df[X_column] + regression_intercept)) ** 2)

    if ss_tot == 0:
        return {"error": "ss_tot is zero, cannot compute r_squared"}

    r_squared = 1-(ss_res/ss_tot)


    mean_squared_error = sum((df[y_column]-(regression_slope * df[X_column] + regression_intercept))**2)/df.shape[0]
    root_mean_squared_error = mean_squared_error**(1/2)

    mean_absolute_error = sum(abs(df[y_column]-(regression_slope * df[X_column] + regression_intercept)))/df.shape[0]

    output_json = {
        "filename": file.filename,
        "x_column": X_column,
        "y_column": y_column,
        "linear_regression": {
            "slope": regression_slope,
            "intercept": regression_intercept,
            "r_squared": r_squared,
            "mean_squared_error": mean_squared_error,
            "root_mean_squared_error": root_mean_squared_error,
            "mean_absolute_error": mean_absolute_error
        }
    }
    return output_json



# correlation matrix
@app.post("/correlation_matrix/")
async def correlation_matrix(file: UploadFile = File(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        return {"error": "No numeric columns found in the dataset"}

    correlation_matrix = numeric_df.corr().to_dict()

    return {"correlation_matrix": correlation_matrix}
