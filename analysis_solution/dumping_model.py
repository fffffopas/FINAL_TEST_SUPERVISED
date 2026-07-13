import mlflow
import joblib

MODEL_NAME = "ChurnModel"

def dump_model():
    client = mlflow.MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    last_version_info = max(versions, key=lambda v: int(v.version))

    model_uri = f"models:/{MODEL_NAME}/{last_version_info.version}"
    model = mlflow.sklearn.load_model(model_uri)

    experiment_id = mlflow.set_experiment("Churn_Classification").experiment_id
    eval_run = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string="tags.mlflow.runName = 'model-evaluation' and status = 'FINISHED'",
        order_by=["start_time DESC"]
    ).iloc[0]
    metrics = {col.replace("metrics.", ""): eval_run[col] for col in eval_run.index if col.startswith("metrics.")}

    with open("model/model", "wb") as f:
        context = {
                    "model": model,
                    "temp_version": last_version_info.version,
                    "metrics" : metrics
                   }
        
        joblib.dump(context, f)
        

dump_model()

