import json
from dataclasses import asdict

def save_items(item, filename="PathDataset.json"):
    try:
        # leggi quello che già c'è nel file
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # se il file non esiste o è vuoto/metà corrotto
        data = []

    # aggiungi i nuovi items convertendoli in dict
    data.extend([asdict(item)])

    # riscrivi tutto il file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
