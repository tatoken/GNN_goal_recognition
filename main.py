from PyQt6.QtWidgets import QApplication
import sys
import random

from Loaders import LoaderMapFirstType
from PathVisualizer import PathVisualizer
import networkx as nx
from Data.GraphMapFirstType import GraphMapFirstType
from Savers import SaverItem


from Data.MapFirstType import MapFirstType
from Data.MapSecondType import MapSecondType

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


def visualize_map(map_info,path,source,destination,cells_mapping):

    app = QApplication(sys.argv)
    window = PathVisualizer(
        map_info.size,
        map_info.map_data,
        source,
        destination,
        path,
        cells_mapping
        ,5
    )
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    size = 16
    file=1
    file_number=0

    for i in range(1,101): 
        file=i
        file_name = f"datasetMapsNew/maps_dataset_{size}/maps_dataset_{size}_{file}.json"
        map_info = LoaderMapFirstType.load_map_from_json(file_name)
        for m in range(len(map_info)):
            solution_paths=[]
            goals=[]
            #mapTest={0:[1,2],1:[0],2:[0,4],3:[6],4:[2,5],5:[4,6],6:[3,5]}
            for sd in range(len(map_info[m].source_destinations)):

                print(f"file:{file} - mappa:{map_info[m].map_id} - percorso:{sd}")

                graphMapTranslater=GraphMapFirstType(map_info[m])

                G = nx.Graph()

                newGraph,coord_to_node=graphMapTranslater.translateMapIntoGraph()
                
                numberOfFreeCell=len(newGraph.items())

                for nodo, vicini in newGraph.items():
                    for v in vicini:
                        G.add_edge(nodo, v)

                source=random.randint(0,numberOfFreeCell-1)
                destination=random.randint(0,numberOfFreeCell-1)

                while not source!=destination:
                    destination=random.randint(0,numberOfFreeCell-1)

                DijkstraPath= nx.astar_path(G,source, destination)

                #visualize_map(map_info[m],DijkstraPath,source,destination,coord_to_node)
                #DfsPath = dfs(graphMapTranslater.translateMapIntoGraph(), source, destination)
                #DfsRandomPath = dfs(graphMapTranslater.translateMapIntoGraph(),source, destination,True)
                
                solution_paths.append(DijkstraPath)
                goals.append(destination)

            mapSecond=MapSecondType(solution_paths,graphMapTranslater.translateMapIntoGraph(),goals)
            item=mapSecond.getItem()
                
            file_number+=1
            datasetFile=f"DatasetSpezzatoOgni10/DijkstraPathDatasetSize{size}File{file_number}.json"
            
            SaverItem.save_items(item,datasetFile)

                