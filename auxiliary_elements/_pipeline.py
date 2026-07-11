from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from catboost import CatBoostClassifier
from _transformer_function import to_num_nonbin, to_delete, to_category

def create_pipeline():
    binary_column = [
        "gender", "SeniorCitizen", "Partner",
        "Dependents", "PhoneService", "PaperlessBilling",
    ]
    to_binary_column = [
        "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV",
        "StreamingMovies",
    ]
    cat_column = [
        "remainder__InternetService", "remainder__Contract",
        "remainder__PaymentMethod",
    ]
    
    preprocess = ColumnTransformer(transformers=[
        ("to_num_bin", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), binary_column),
        ("to_num_nbin", FunctionTransformer(to_num_nonbin), to_binary_column),
    ], remainder="passthrough")

    preprocess.set_output(transform="pandas")
    model = CatBoostClassifier(cat_features=tuple(cat_column), verbose=0,
                                auto_class_weights="Balanced", random_seed=42)

    pipe = Pipeline([
        ("to_delete", FunctionTransformer(to_delete)),
        ("preprocess", preprocess),
        ("to_category", FunctionTransformer(to_category, kw_args={"col": cat_column})),
        ("model", model),
    ])
    return pipe