import json
from Data.MapFirstType import MapFirstType

def load_map_from_json(file_name: str) -> MapFirstType:
    with open(file_name, 'r') as f:
        data = json.load(f)
    
    maps=[]
    for i in range(len(data)):
        maps.append(MapFirstType(
            map_data=data[i].get("map", []),
            source_destination=tuple(data[i].get("source_destination", (0, 0))),
            percentage_obstacles=float(data[i].get("percentage_obstacles", 0.0)),
            id=int(data[i].get("id", 0)),
            map_id=int(data[i].get("map_id", 0)),
            size=int(data[i].get("size", 0))
        ))
    
    return maps
