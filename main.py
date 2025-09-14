from PyQt6.QtWidgets import QApplication
import sys
import numpy as np
import random

from Loaders import LoaderMapFirstType
from PathVisualizer import PathVisualizer
import networkx as nx
from Data.GraphMapFirstType import GraphMapFirstType

def dfs(graph, start, goal,randomJump=False):
    stack = [(start, [start])]
    visited = set()
    

    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        visited.add(current)
        neighbors = [n for n in graph.get(current, []) if n not in visited]
        if randomJump: 
            random.shuffle(neighbors)  
        for neighbor in neighbors:
            stack.append((neighbor, path + [neighbor]))
            
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    size = 16
    file=1
    file_name = f"dataset/maps_dataset_{size}/maps_dataset_{size}_{file}.json"
    index = 0
    map_info = LoaderMapFirstType.load_map_from_json(file_name, index)
    
    graphMapTranslater=GraphMapFirstType(map_info)

    for nodo,vicini in graphMapTranslater.translateMapIntoGraph().items():
        print(nodo)
        print(vicini)

    G = nx.Graph()
    for nodo, vicini in graphMapTranslater.translateMapIntoGraph().items():
        for v in vicini:
            G.add_edge(nodo, v)

    DijkstraPath= nx.astar_path(G, map_info.source_destination[0], map_info.source_destination[1])
    DfsPath = dfs(graphMapTranslater.translateMapIntoGraph(), map_info.source_destination[0], map_info.source_destination[1])
    DfsRandomPath = dfs(graphMapTranslater.translateMapIntoGraph(),map_info.source_destination[0], map_info.source_destination[1],True)
    
    window = PathVisualizer(
        map_info.size,
        map_info.map_data,
        map_info.source_destination[0],
        map_info.source_destination[1],
        DijkstraPath
        ,5
    )

    print(DijkstraPath)

    print(f"Dijkstra:{len(DijkstraPath)}")
    print(f"Dfs:{len(DfsPath)}")
    print(f"Dfs jump:{len(DfsRandomPath)}")
    
    window.show()
    sys.exit(app.exec())


