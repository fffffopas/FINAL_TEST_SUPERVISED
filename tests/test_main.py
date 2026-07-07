from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_calculate_model():
    data = {
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
                "TotalCharges": 29.85
            }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert response.json()["prediction"] == ["No"]