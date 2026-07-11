import sys
import pandas as pd
import optuna
import argparse
import tempfile
import warnings
import mlflow

from sklearn.model_selection import cross_val_score
from optuna.samplers import TPESampler
from auxiliary_elements import create_pipeline
from loguru import logger


logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.ERROR)

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

def objective(trial, pipeline_cat_boost, X_train, y_train):
    params = {
        "model__n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "model__max_depth": trial.suggest_int("max_depth", 2, 10),
        "model__learning_rate": trial.suggest_float("learning_rate", 1e-4, 0.3, log=True),
        "model__subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "model__l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
    }

    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        pipeline_cat_boost.set_params(**params)
        score = cross_val_score(pipeline_cat_boost, X_train, y_train, cv=5, scoring="accuracy").mean()
        mlflow.log_metric("accuracy", score)
        logger.info(f"Trial {trial.number}, accuracy: {score:.4f}")
        return score

if __name__ == "__main__":
    N_TRIALS = 25
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-trials", default=N_TRIALS, type=int)
    N_TRIALS = parser.parse_args().n_trials

    logger.info(f"Hyperparameters tuning started with: {N_TRIALS}")

    experiment_id = mlflow.set_experiment("Churn_Classification").experiment_id

    with mlflow.start_run(run_name="hyperparameters-tuning", log_system_metrics=True):
        train, test = load_train_test(experiment_id)
        target_col = "Churn"
        X_train, y_train = train.drop([target_col], axis=1), train[target_col]

        pipeline_cat_boost = create_pipeline()

        study = optuna.create_study(direction="maximize", sampler=TPESampler(seed=42))
        study.optimize(lambda trial: objective(trial, pipeline_cat_boost, X_train, y_train), n_trials=N_TRIALS)
        best_trial = study.best_trial
        logger.info(f"Best params: {best_trial.params}, accuracy: {best_trial.value:.4f}")

        mlflow.log_params(best_trial.params)
        mlflow.log_metric("best_accuracy", best_trial.value)