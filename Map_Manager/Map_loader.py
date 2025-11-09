import json

from Map_Manager.Map import Map

def load_map_from_json(file_name: str) -> Map:
    with open(file_name, 'r') as f:
        data = json.load(f)
    
    maps=[]
    for i in range(len(data)):

        source_and_destionations=[]
        for source_and_destination in data[i].get("instances"):
            source_and_destionations.append(tuple(source_and_destination.get("source_destination", (0, 0))))
        
        maps.append(Map(
            map_data=data[i].get("map", []),
            source_destinations=source_and_destionations,
            percentage_obstacles=float(data[i].get("percentage_obstacles", 0.0)),
            id=int(data[i].get("id", 0)),
            map_id=int(data[i].get("map_id", 0)),
            size=int(data[i].get("size", 0))
        ))
    
    return maps
