from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import numpy as np
import io
import uvicorn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

app = FastAPI()

# this is for testing, delete later
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# this one is useless, also for testing (since we use POST for every request)
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    head = df.head().to_dict(orient="records")
    

    return {"filename": file.filename, "head": head}


@app.post("/mean_value/")
async def mean_column(file: UploadFile = File(...), column: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    mean = df[column].mean()
    return {"mean_value": mean}



@app.post("/median_value/") 
async def mean_column(file: UploadFile = File(...), column: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    median = df[column].median()
    return {"median_value": median}




@app.post("/standard_deviation/")
async def mean_column(file: UploadFile = File(...), column: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if column not in df.columns:
        return {"error": "Column not found in the dataset"}

    #x = df[column]
    #std_dev = pow((abs(pow(x-(x.mean()),2))).mean(),(1/2))
    std_dev = df[column].std(ddof=0)
    return {"standard_deviation": std_dev}


# Pearson correlation, (-1, 1)
# Close to 0 means no correlation
@app.post("/correlation/")
async def correlation(file: UploadFile = File(...), x_column: str = Form(...), y_column: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    if x_column not in df.columns or y_column not in df.columns:
        return {"error": "One or both columns not found in the dataset"}
    
    correlation_value = df[x_column].corr(df[y_column])

    return {"correlation": correlation_value}




@app.post("/linear_regression/")
async def linear_regression(file: UploadFile = File(...), x_column: str = Form(...), y_column: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if x_column not in df.columns or y_column not in df.columns:
        return {"error": "One or both columns not found in the dataset"}

    # linear regression
    X=df[[x_column]].values
    y=df[y_column].values
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0]
    intercept = model.intercept_

    # additional analysis
    r_squared = model.score(X, y)
    y_pred = model.predict(X)
    #residuals = (y - y_pred).tolist()
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, y_pred)

    output_json = {
        "filename": file.filename,
        "x_column": x_column,
        "y_column": y_column,
        "linear_regression": {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "mean_squared_error": mse,
            "root_mean_squared_error": rmse,
            "mean_absolute_error": mae
        }
    }

    return output_json