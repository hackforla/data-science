
# Quick, beginner-friendly EDA that saves pictures into reports/
import os, yaml
import matplotlib.pyplot as plt
from src.utils import set_all_seeds, get_env
from src.data import load_text_classification, describe_dataset

def main(cfg_path="configs/baseline.yaml"):
    set_all_seeds(42)
    cfg = yaml.safe_load(open(cfg_path))
    cache = get_env("DATA_CACHE_DIR", "./.hf_cache")

    train_df, valid_df, test_df = load_text_classification(cfg["dataset"], cache_dir=cache)

    # 1) Print simple stats
    print("TRAIN:", describe_dataset(train_df))
    if valid_df is not None:
        print("VALID:", describe_dataset(valid_df))
    print("TEST :", describe_dataset(test_df))

    # 2) Plot token length histogram (train)
    lengths = train_df["text"].astype(str).str.split().map(len)
    plt.figure()
    lengths.hist(bins=50)
    plt.xlabel("Tokens per example"); plt.ylabel("Count"); plt.title("Token Lengths (train)")
    os.makedirs("reports", exist_ok=True)
    plt.savefig("reports/eda_token_lengths.png", dpi=160, bbox_inches="tight")
    print("Saved: reports/eda_token_lengths.png")

if __name__ == "__main__":
    main()
