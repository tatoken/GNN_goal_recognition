import json
from dataclasses import asdict

def save_items(item, filename="PathDataset.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.extend([asdict(item)])

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
