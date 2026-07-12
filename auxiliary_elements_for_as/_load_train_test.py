import tempfile
import mlflow
import pandas as pd
from loguru import logger

def load_train_test(experiment_id):
    last_run_id = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string="tags.mlflow.runName = 'data-splitting' and status = 'FINISHED'",
        order_by=["start_time DESC"],
    ).loc[0, "run_id"]

    with tempfile.TemporaryDirectory() as tmpdir:
        train_path = mlflow.artifacts.download_artifacts(run_id=last_run_id, artifact_path="datasets/train.csv", dst_path=tmpdir)
        test_path =  mlflow.artifacts.download_artifacts(run_id=last_run_id, artifact_path="datasets/test.csv", dst_path=tmpdir)
        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)

    logger.info(f"Loaded train/test from run {last_run_id}")
    return train, test