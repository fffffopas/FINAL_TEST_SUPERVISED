import sys
import mlflow
import warnings
import logging
from loguru import logger
from auxiliary_elements import load_train_test, create_pipeline

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logging.getLogger("mlflow").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

def load_best_params(experiment_id):
    run = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string="tags.mlflow.runName = 'hyperparameters-tuning' and status = 'FINISHED'",
        order_by=["metrics.best_accuracy DESC"],
    ).iloc[0]

    best_params = {
        col.replace("params.", ""):run[col]
        for col in run.index
        if col.startswith("params.")
    }

    for key in ["n_estimators", "max_depth"]:
        best_params[key] = int(best_params[key])

    for key in ["learning_rate", "subsample", "l2_leaf_reg"]:
        best_params[key] = float(best_params[key])


    logger.info(f"Best params was loaded: {best_params}")
    return best_params

if __name__ == "__main__":
    logger.info("Model training started")

    experiment_id = mlflow.set_experiment("Churn_Classification").experiment_id

    with mlflow.start_run(run_name="model-training") as run:
        run_id = run.info.run_id
        logger.info(f"Start mlflow run: {run_id}")

        train, test = load_train_test(experiment_id)
        best_params = load_best_params(experiment_id)

        target_col = "Churn"
        X_train, y_train = train.drop([target_col], axis=1), train[target_col]
        pipeline_cat_boost = create_pipeline()
        pipeline_cat_boost.set_params(**{f"model__{k}":v for k, v in best_params.items()})
        pipeline_cat_boost.fit(X_train, y_train)

        trusted_types = [
            "auxiliary_elements._transformer_function.to_category",
            "auxiliary_elements._transformer_function.to_delete",
            "auxiliary_elements._transformer_function.to_num_nonbin",
            "catboost.core.CatBoostClassifier",
        ]   
        input_example = X_train.iloc[:5]
        mlflow.sklearn.log_model(pipeline_cat_boost, "model", input_example=input_example, skops_trusted_types=trusted_types)

        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri, "ChurnModel")
        logger.info("Model training finished, model was registered")
