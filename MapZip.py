import json
from collections import defaultdict

def convert_file(input_file, output_file):
    # Carico il file originale
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Raggruppo le mappe per map_id
    maps = defaultdict(lambda: {"map": None, "size": None, "percentage_obstacles": None, "instances": []})

    for entry in data:
        map_id = entry["map_id"]

        # Se la mappa non è stata ancora salvata, la imposto
        if maps[map_id]["map"] is None:
            maps[map_id]["map"] = entry["map"]
            maps[map_id]["size"] = entry["size"]
            maps[map_id]["percentage_obstacles"] = entry["percentage_obstacles"]

        # Aggiungo l'istanza con id e source_destination
        maps[map_id]["instances"].append({
            "id": entry["id"],
            "source_destination": entry["source_destination"]
        })

    # Trasformo nel formato finale
    result = []
    for map_id, info in maps.items():
        result.append({
            "map_id": map_id,
            "size": info["size"],
            "percentage_obstacles": info["percentage_obstacles"],
            "map": info["map"],
            "instances": info["instances"]
        })

    # Salvo il file convertito
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Conversione completata! File salvato in: {output_file}")


# ESEMPIO USO
# convert_file("input.json", "output.json")