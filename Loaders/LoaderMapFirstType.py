import json
from Data.MapFirstType import MapFirstType

def load_map_from_json(file_name: str, index: int) -> MapFirstType:
    with open(file_name, 'r') as f:
        data = json.load(f)
    
    if index < 0 or index >= len(data):
        raise IndexError(f"Indice {index} fuori dal range dei dati disponibili ({len(data)} elementi).")
    
    map_entry = data[index]
    
    return MapFirstType(
        map_data=map_entry.get("map", []),
        source_destination=tuple(map_entry.get("source_destination", (0, 0))),
        percentage_obstacles=float(map_entry.get("percentage_obstacles", 0.0)),
        id=int(map_entry.get("id", 0)),
        map_id=int(map_entry.get("map_id", 0)),
        size=int(map_entry.get("size", 0))
    )
