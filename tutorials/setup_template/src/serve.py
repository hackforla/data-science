
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc, glob

app = FastAPI(title="T0 Baseline Inference")

class InferRequest(BaseModel):
    text: str

def _latest_model_path():
    # look for the newest model saved by MLflow locally
    candidates = sorted(glob.glob("mlruns/*/*/artifacts/model"))
    if not candidates:
        raise RuntimeError("No model artifacts found. Run baseline first.")
    return candidates[-1]

@app.post("/infer")
def infer(payload: InferRequest):
    model = mlflow.pyfunc.load_model(_latest_model_path())
    pred = model.predict([payload.text])
    return {"label": int(pred[0])}
