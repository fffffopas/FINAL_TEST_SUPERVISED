import sys
import warnings
import logging
import mlflow
from loguru import logger
from auxiliary_elements_for_as import load_train_test

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)

if __name__ == "__main__":
    logger.info("Model evaluation started")
    experiment_id = mlflow.set_experiment("Churn_Classification").experiment_id

    with mlflow.start_run(run_name="model-evaluation") as run:
        train, test = load_train_test(experiment_id)
        eval_dataset = mlflow.data.from_pandas(test, targets="Churn")

        last_version = mlflow.MlflowClient().get_registered_model("ChurnModel").latest_versions[0].version
        logger.info(f"Evaluated model version: {last_version}")

        mlflow.evaluate(data=eval_dataset, model_type="classifier", model=f"models:/ChurnModel/{last_version}")
        logger.info("Model evaluation finished")