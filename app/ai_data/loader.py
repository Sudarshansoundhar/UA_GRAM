import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDERS = {
    "text": BASE_DIR / "datasets/text",
    "symbols": BASE_DIR / "datasets/symbols",
    "emoji": BASE_DIR / "datasets/emoji",
    "images": BASE_DIR / "datasets/images",
}

class DatasetManager:
    def __init__(self):
        self.cache = {}
        self.reload()

    def _load_folder(self, folder):
        data = []
        if not folder.exists():
            return data

        for file in folder.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data.extend(json.load(f))
            except Exception as e:
                print(f"[AI DATA] Failed loading {file}: {e}")
        return data

    def reload(self):
        for key, folder in DATA_FOLDERS.items():
            self.cache[key] = self._load_folder(folder)

    def get(self, key):
        return self.cache.get(key, [])

# Singleton
dataset_manager = DatasetManager()
