from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import numpy as np
import io
import uvicorn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
#asd
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



@app.post("/linear_regression/")
async def linear_regression(file: UploadFile = File(...), x_col: str = Form(...), y_col: str = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # linear regression
    X=df[[x_col]].values
    y=df[y_col].values
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
        "x_column": x_col,
        "y_column": y_col,
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