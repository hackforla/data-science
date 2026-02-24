from datasets import load_dataset
import pandas as pd
from collections import Counter

def load_text_classification(name, cache_dir=None):
    """
    Loads a Hugging Face dataset and returns 3 DataFrames:
    train_df, valid_df (or None), test_df with columns: text, label
    """
    ds = load_dataset(name, cache_dir=cache_dir)
    train_df = pd.DataFrame(ds["train"])
    test_df  = pd.DataFrame(ds["test"])
    valid_df = pd.DataFrame(ds["validation"]) if "validation" in ds else None
    return train_df, valid_df, test_df

def describe_dataset(df, text_col="text", label_col="label"):
    lengths = df[text_col].astype(str).str.split().map(len)
    counts  = Counter(df[label_col])
    return {
        "rows": len(df),
        "avg_tokens": float(lengths.mean()),
        "median_tokens": float(lengths.median()),
        "label_counts": dict(counts),
    }
