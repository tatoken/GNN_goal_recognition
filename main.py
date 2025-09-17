from PyQt6.QtWidgets import QApplication
import sys
import numpy as np
import random

from Loaders import LoaderMapFirstType
from PathVisualizer import PathVisualizer
import networkx as nx
from Data.GraphMapFirstType import GraphMapFirstType
from Savers import SaverItem


from Data.MapFirstType import MapFirstType
from Data.MapSecondType import MapSecondType
import MapZip 

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


def visualize_map(map_info,path):

    app = QApplication(sys.argv)
    window = PathVisualizer(
        map_info.size,
        map_info.map_data,
        map_info.source_destination[0],
        map_info.source_destination[1],
        path
        ,5
    )
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    size=16
    file=1
    
    for i in [16,32,128]:
        for f in range(1,101):
            datasetFile=f"dataset/maps_dataset_{i}/maps_dataset_{i}_{f}.json"
            datasetFileOutput=f"datasetMapsNew/maps_dataset_{i}/maps_dataset_{i}_{f}.json"
            MapZip.convert_file(datasetFile,datasetFileOutput)
        

    """
    size = 128
    file_number=0
    datasetFile=f"DatasetSpezzatoOgni10/DfsPathDatasetSize{size}File{file_number}.json"

    for i in range(1,101): 
        file=i
        file_name = f"dataset/maps_dataset_{size}/maps_dataset_{size}_{file}.json"
        map_info = LoaderMapFirstType.load_map_from_json(file_name)
        for m in range(len(map_info)):
             
            #mapTest={0:[1,2],1:[0],2:[0,4],3:[6],4:[2,5],5:[4,6],6:[3,5]}

            print(f"file:{file} - mappa:{m}")

            graphMapTranslater=GraphMapFirstType(map_info[m])

            G = nx.Graph()

            for nodo, vicini in graphMapTranslater.translateMapIntoGraph().items():
                for v in vicini:
                    G.add_edge(nodo, v)

            #visualize_map(map_info[m],[0,1])

            rS = (map_info[m].source_destination[0] // map_info[m].size)
            cS = (map_info[m].source_destination[0] % map_info[m].size)

            rD = (map_info[m].source_destination[1] // map_info[m].size)
            cD = (map_info[m].source_destination[1] % map_info[m].size)

            source=map_info[m].source_destination[0]
            destination=map_info[m].source_destination[1]
            
            if(   (map_info[m].map_data[rS][cS]!=0 or map_info[m].map_data[rD][cD]!=0)   or   (rS==rD and cS==cD)   ):

                ended=False
                while not ended:
                    sourceX=random.randint(0,map_info[m].size-1)
                    sourceY=random.randint(0,map_info[m].size-1)
                    if(map_info[m].map_data[sourceX][sourceY]==0):
                        source=sourceX*map_info[m].size+sourceY
                        ended=True

                ended=False
                while not ended:
                    destinationX=random.randint(0,map_info[m].size-1)
                    destinationY=random.randint(0,map_info[m].size-1)
                    if(map_info[m].map_data[sourceX][sourceY]==0 and (destinationX!=sourceX and destinationY!= sourceY)):
                        destination=destinationX*map_info[m].size+destinationY
                        ended=True

            DijkstraPath= nx.astar_path(G, map_info[m].source_destination[0], map_info[m].source_destination[1])
            #DfsPath = dfs(graphMapTranslater.translateMapIntoGraph(), source, destination)
            #DfsRandomPath = dfs(graphMapTranslater.translateMapIntoGraph(),map_info.source_destination[0], map_info.source_destination[1],True)
            

            mapSecond=MapSecondType(DijkstraPath,graphMapTranslater.translateMapIntoGraph(),destination)
            items=mapSecond.getItems()
            
            if(m%10==0):
                file_number+=1
                datasetFile=f"DatasetSpezzatoOgni10/DfsPathDatasetSize{size}File{file_number}.json"

            #SaverItem.save_items(items,datasetFile)
            

            

    """
