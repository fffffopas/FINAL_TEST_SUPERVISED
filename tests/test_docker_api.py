import pandas as pd
import pytest
import requests
from sklearn.metrics import recall_score, precision_score, accuracy_score

pytestmark = pytest.mark.docker


BASE_URL = "http://localhost:8000"

def test_calculate_model_via_docker():
    tests = pd.read_csv("required_data/tests.csv")
    X = tests.drop(["Churn"], axis=1)
    y = tests["Churn"]

    data = X.to_dict(orient="records")
    response = requests.post(f"{BASE_URL}/predict", json=data)
    assert response.status_code == 200

    predictions = pd.Series(response.json()["prediction"])
    RECALL = recall_score(y, predictions, pos_label="Yes")
    PRECISION = precision_score(y, predictions, pos_label="Yes")
    ACCURACY = accuracy_score(y, predictions)

    assert RECALL >= 0.6
    assert PRECISION >= 0.55
    assert ACCURACY >= 0.75