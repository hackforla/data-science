import os
import random
import numpy as np


def set_all_seeds(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass

def get_env(name: str, default: str = "") -> str:
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv(name, default)


