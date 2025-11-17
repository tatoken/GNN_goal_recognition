from PyQt6.QtWidgets import QApplication
import sys
import random
import numpy as np

from Map_Manager import Map_loader
from Path_Visualizer.PathVisualizer import PathVisualizer
from Map_Manager.Map_graph_manager import Map_graph_manager
from Map_Manager import Output_instance_saver

from Map_Manager.Data.Map_output import Map_output    

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


def visualize_map(map_graph_manager,path,source,destination,matrix_list):
    app = QApplication(sys.argv)

    window = PathVisualizer(
        map_graph_manager,
        source,
        destination,
        path,
        50
        ,matrix_list
    )
    window.show()
    sys.exit(app.exec())

def print_info_of_current_process(source_destinations_per_map, source_destination):
    print("Percorso:",end="")
    print("█"*source_destination,end="")
    print("░"*(source_destinations_per_map-(source_destination+1)),end="")
    print(f"{source_destination+1}/{source_destinations_per_map}")

if __name__ == "__main__":

    number_of_files=100
    size = 8
    file=1
    file_number=0   
    source_destinations_per_map=10

    for file in range(1,number_of_files+1): 

        file_name = f"Datasets/Modified_dataset/maps_dataset_{size}/maps_dataset_{size}_{file}.json"
        maps_in_file = Map_loader.load_map_from_json(file_name)
        
        for map in range(len(maps_in_file)): 

            solution_paths=[]
            goals=[]
            manhattanDistances=[]
            list_matrix_prob=[]

            graphMapManager=Map_graph_manager(maps_in_file[map])
            newGraph=graphMapManager.get_graph()

            print(f"File:{file} - Mappa:{maps_in_file[map].map_id} ")

            for source_destination in range(source_destinations_per_map):

                print_info_of_current_process(source_destinations_per_map, source_destination)
                
                source,destination=graphMapManager.generate_random_source_destination()
                
                #DijkstraPath= nx.astar_path(G,source, destination)
                #DfsPath = dfs(newGraph, source, destination)
                DfsRandomPath = dfs(newGraph, graphMapManager.coord_to_node_id(source), graphMapManager.coord_to_node_id(destination),True)

                matrix_prob=graphMapManager.calculate_probabilities(DfsRandomPath)     

                solution_paths.append(DfsRandomPath)
                goals.append(destination)
                manhattanDistances.append(abs(source[0] - destination[0]) + abs(source[1] - destination[1]))

                list_matrix_prob.append(matrix_prob[-1])
            print("_________________________")

            visualize_map(graphMapManager,DfsRandomPath,source,destination,matrix_prob)
            """"
            mapSecond=Map_output(solution_paths,manhattanDistances,newGraph,goals,map_info[m].percentage_obstacles)
            item=mapSecond.getItem()
                
            file_number+=1
            datasetFile=f"DfsRandomJump8/DfsRandomJumpDatasetSize{size}File{file_number}.json"
            
            Output_instance_saver.save_items(item,datasetFile)
            """


                
