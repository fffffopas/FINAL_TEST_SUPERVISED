import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from typing import Literal
from pydantic import BaseModel
from auxiliary_elements import to_delete, to_num_nonbin, to_category # noqa: F401


app = FastAPI(title="Telco-Customer-Churn predictor")

with open("model/model", "rb") as f:
    context = joblib.load(f)
    model = context["model"]

class Features(BaseModel):
    customerID: str
    gender: Literal['Male', 'Female']
    SeniorCitizen: Literal[0, 1]
    Partner: Literal['No', 'Yes']
    Dependents: Literal['No', 'Yes']
    tenure: int
    PhoneService: Literal['No', 'Yes']
    MultipleLines: Literal['No phone service', 'No', 'Yes']
    InternetService: Literal['DSL', 'Fiber optic', 'No']
    OnlineSecurity: Literal['No', 'Yes', 'No internet service']
    OnlineBackup: Literal['Yes', 'No', 'No internet service']
    DeviceProtection: Literal['No', 'Yes', 'No internet service']
    TechSupport: Literal['No', 'Yes', 'No internet service']
    StreamingTV: Literal['No', 'Yes', 'No internet service']
    StreamingMovies: Literal['No', 'Yes', 'No internet service']
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    PaperlessBilling: Literal['Yes', 'No']
    PaymentMethod: Literal['Electronic check', 'Mailed check', 
                           'Bank transfer (automatic)',
                           'Credit card (automatic)']
    MonthlyCharges: float
    TotalCharges: float

    model_config = {
        "json_schema_extra":{
            "example":[{
                "customerID": "1234-ABCD",
                "gender" : "Male",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents" : "No",
                "tenure" : 12,
                "PhoneService":"Yes",
                "MultipleLines":"No",
                "InternetService":"DSL",
                "OnlineSecurity" : "Yes",
                "OnlineBackup" : "No",
                "DeviceProtection" :"No",
                "TechSupport" : "No",
                "StreamingTV" : "No",
                "StreamingMovies" : "No",
                "Contract":"Month-to-month",
                "PaperlessBilling":"Yes",
                "PaymentMethod" : "Electronic check",
                "MonthlyCharges":29.85,
                "TotalCharges": 29.85,
            }]
        }
    }
@app.get("/")
def read_root():
    return{
        "message" : "Telco-Customer-Churn predictor API",
        "endpoints" : {
            "/predict":"POST - Make a prediction",
            "/health" : "GET - Check API health",
            "/docs" : "GET - API documentation",
        }
    }

@app.get("/health")
def health_check():
    return {"status" :"healthy", 
            "model_loaded" : model is not None,
            "model_verison" : context["temp_version"],
            "model_metrics" : context["metrics"]
            }

@app.post("/predict")
def predict(features: list[Features]):
    try:
        input_data = pd.DataFrame([feature.model_dump() for feature in features])
        prediction = model.predict(input_data)

        return{
            "prediction": prediction.tolist(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))