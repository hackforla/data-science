
import os, yaml, mlflow, mlflow.sklearn
from src.utils import set_all_seeds, get_env
from src.data import load_text_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def run_baseline(cfg_path="configs/baseline.yaml"):
    set_all_seeds(42)
    cfg = yaml.safe_load(open(cfg_path))

    mlflow.set_tracking_uri(get_env("MLFLOW_TRACKING_URI", "./mlruns"))
    mlflow.set_experiment(cfg["experiment_name"])

    train_df, valid_df, test_df = load_text_classification(
        cfg["dataset"], cache_dir=get_env("DATA_CACHE_DIR", "./.hf_cache")
    )

    if valid_df is None:
        train_df, valid_df = train_test_split(
            train_df, test_size=cfg["test_size"], random_state=cfg["random_state"], stratify=train_df["label"]
        )

    X_train, y_train = train_df["text"].astype(str), train_df["label"]
    X_valid, y_valid = valid_df["text"].astype(str), valid_df["label"]
    X_test,  y_test  = test_df["text"].astype(str),  test_df["label"]

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=cfg["tfidf"]["max_features"],
            ngram_range=tuple(cfg["tfidf"]["ngram_range"])
        )),
        ("clf", LogisticRegression(
            C=cfg["model"]["C"],
            max_iter=cfg["model"]["max_iter"]
        ))
    ])

    with mlflow.start_run():
        # log params
        mlflow.log_params({
            "dataset": cfg["dataset"],
            "tfidf_max_features": cfg["tfidf"]["max_features"],
            "tfidf_ngram_range": str(cfg["tfidf"]["ngram_range"]),
            "model": cfg["model"]["type"],
            "C": cfg["model"]["C"],
            "max_iter": cfg["model"]["max_iter"],
            "random_state": cfg["random_state"]
        })

        pipe.fit(X_train, y_train)
        y_pred_valid = pipe.predict(X_valid)
        y_pred_test  = pipe.predict(X_test)

        # metrics
        acc_valid = accuracy_score(y_valid, y_pred_valid)
        f1_valid  = f1_score(y_valid, y_pred_valid, average=cfg["metrics"]["average"])
        acc_test  = accuracy_score(y_test, y_pred_test)
        f1_test   = f1_score(y_test, y_pred_test, average=cfg["metrics"]["average"])

        mlflow.log_metrics({
            "valid_accuracy": acc_valid,
            "valid_f1_macro": f1_valid,
            "test_accuracy": acc_test,
            "test_f1_macro": f1_test
        })

        # save confusion matrix
        os.makedirs("reports", exist_ok=True)
        fig = ConfusionMatrixDisplay.from_predictions(y_test, y_pred_test).figure_
        fig.savefig("reports/confusion_matrix.png", dpi=180, bbox_inches="tight")
        mlflow.log_artifact("reports/confusion_matrix.png")

        # save text report
        report = classification_report(y_test, y_pred_test)
        with open("reports/classification_report.txt", "w") as f:
            f.write(report)
        mlflow.log_artifact("reports/classification_report.txt")

        # save model
        mlflow.sklearn.log_model(pipe, artifact_path="model")

        print("Validation -> acc:", acc_valid, "f1_macro:", f1_valid)
        print("Test       -> acc:", acc_test,  "f1_macro:", f1_test)
        print("\nClassification report saved at reports/classification_report.txt")

if __name__ == "__main__":
    run_baseline()
