import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auxiliary_elements import to_delete, to_num_nonbin, to_category # noqa: F401


app = FastAPI(title="Telco-Customer-Churn predictor")

with open("model/model_cb.joblib", "rb") as f:
    model = joblib.load(f)

class Features(BaseModel):
    customerID: str
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

    model_config = {
        "json_schema_extra":{
            "example":{
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
            }
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
    return {"status" :"healthy", "model_loaded" : model is not None}

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