import json

from Map_Manager.Data.Map_input import Map_input

def load_map_from_json(file_name: str) -> Map_input:
    with open(file_name, 'r') as f:
        data = json.load(f)
    
    maps=[]
    for i in range(len(data)):
        
        maps.append(Map_input(
            map_data=data[i].get("map", []),
            percentage_obstacles=float(data[i].get("percentage_obstacles", 0.0)),
            id=int(data[i].get("id", 0)),
            map_id=int(data[i].get("map_id", 0)),
            size=int(data[i].get("size", 0))
        ))
    
    return maps
