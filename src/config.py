import yaml
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        # Convert relative data paths to absolute
        if 'data' in data:
            for key in ['raw_path', 'processed_path']:
                if key in data['data'] and not os.path.isabs(data['data'][key]):
                    data['data'][key] = str(ROOT_DIR / data['data'][key])
        return data

config = load_config()
