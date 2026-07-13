import sys
import argparse
import mlflow
import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
warnings.filterwarnings("ignore")

def get_telco_customer_dataset():
    df = pd.read_csv("Data/Telco-Customer-Churn.csv")
    X = df.drop(["Churn"], axis=1)
    y = df["Churn"]
    logger.info("Telco_customer_data loaded")

    return X, y

def main():
    TEST_SIZE = 0.3
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-size", default=TEST_SIZE, type=float)
    TEST_SIZE = parser.parse_args().test_size
    logger.info(f"Data splitting with test size: {TEST_SIZE}")
    
    #experiment_id = mlflow.set_experiment("Churn_Classification").experiment_id
    with mlflow.start_run(run_name="data-splitting"):
        X, y = get_telco_customer_dataset()

        mlflow.log_metric("Full_data_size", X.shape[0])
        mlflow.log_metric("Feature_count", X.shape[1])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=42)
        mlflow.log_metric("Train_size", X_train.shape[0])
        mlflow.log_metric("Test_size", X_test.shape[0])

        train = X_train.assign(Churn=y_train)
        mlflow.log_text(train.to_csv(index=False), "datasets/train.csv")
        dataset_source_link = mlflow.get_artifact_uri("datasets/train.csv")
        dataset = mlflow.data.from_pandas(train, name="train", targets="Churn", source=dataset_source_link)
        mlflow.log_input(dataset)

        test = X_test.assign(Churn=y_test)
        mlflow.log_text(test.to_csv(index=False), "datasets/test.csv")
        dataset_source_link = mlflow.get_artifact_uri("datasets/test.csv")
        dataset = mlflow.data.from_pandas(test, name="test", targets="Churn", source=dataset_source_link)
        mlflow.log_input(dataset)

        logger.info("Data splitting finished")

if __name__ == "__main__":
    main()