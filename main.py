from PyQt6.QtWidgets import QApplication
import sys
import random
import numpy as np

from Loaders import LoaderMapFirstType
from PathVisualizer import PathVisualizer
import networkx as nx
from Data.GraphMapFirstType import GraphMapFirstType
from Savers import SaverItem

from Data.MapFirstType import MapFirstType
from Data.MapSecondType import MapSecondType

def count_obstacles_on_path(map_data, start, end):
    r0, c0 = start
    r1, c1 = end
    n_obs = 0

    dr = np.sign(r1 - r0)
    dc = np.sign(c1 - c0)
    r, c = r0 + dr, c0 + dc

    while (r, c) != (r1, c1):

        if not (0 <= r < len(map_data) and 0 <= c < len(map_data[0])):
            n_obs += 1
            break

        if map_data[r][c] == 1:
            n_obs += 1

        r += dr
        c += dc

    return n_obs


def direction_prob(map, map_shape, pos_t, direction, alpha=0.3, beta=1.5, attenuation=0.4, gamma=0.4):
    rows, cols = map_shape
    prob = np.zeros((rows, cols))

    for r in range(rows):
        for c in range(cols):
            # Calcolo la distanza manhattan dalla posizione attuale
            d = abs(r - pos_t[0]) + abs(c - pos_t[1])

            # 'match' serve a dare un peso maggiore alle celle che si trovano
            # nella direzione indicata (up/down/left/right)
            match = 0
            if direction == 'up' and r < pos_t[0]: match = 1
            if direction == 'down' and r > pos_t[0]: match = 1
            if direction == 'left' and c < pos_t[1]: match = 1
            if direction == 'right' and c > pos_t[1]: match = 1

            # calcola quante celle ostacolo ci sono lungo la linea approssimata verso (r,c)
            n_obs = count_obstacles_on_path(map, pos_t, (r, c))

            # attenuazione per ostacoli
            attenuation = gamma ** n_obs

            # Formula della probabilità grezza:
            # - np.exp(-alpha*d): decresce con la distanza (celle lontane = meno probabili)
            # - (1 + beta*match): aumenta la probabilità se la cella è nella direzione "giusta"
            prob[r, c] = np.exp(-alpha * d) * (1 + beta * match) * attenuation
  

    # Normalizzazione:
    # Divido ogni valore per la somma totale di tutti i valori
    # In questo modo, la somma di tutta la matrice prob diventa 1.0
    prob /= prob.sum()

    return prob


def calculate_direction(pos_t, pos_t1):
    if pos_t1[0] < pos_t[0]:
        return 'up'
    elif pos_t1[0] > pos_t[0]:
        return 'down'
    elif pos_t1[1] < pos_t[1]:
        return 'left'
    elif pos_t1[1] > pos_t[1]:
        return 'right'


def calculate_probabilities(map,map_shape,path):
    rows, cols = map_shape
    matrix_prob = np.zeros((rows, cols))
    update_matrix_prob=[]

    node_to_coord = {v: k for k, v in coord_to_node.items()} # mappatura inversa nodo -> coordinate
    for t in range(len(path) - 1):
        r, c = node_to_coord[path[t]]
        r1, c1 = node_to_coord[path[t+1]]
        direction = calculate_direction((r, c), (r1, c1))
        matrix_prob += direction_prob(map, map_shape, (r, c), direction)
        matrix_prob /= matrix_prob.sum()
        update_matrix_prob.append(matrix_prob.copy())

    #print(matrix_prob)
    return update_matrix_prob
    
    

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


def visualize_map(map_info,path,source,destination,cells_mapping,matrix_list):

    app = QApplication(sys.argv)
    window = PathVisualizer(
        map_info.size,
        map_info.map_data,
        source,
        destination,
        path,
        cells_mapping
        ,5
        ,matrix_list
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
            manhattanDistances=[]
            list_matrix_prob=[]
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

                chiave = None
                for k, v in coord_to_node.items():
                    if v == source:
                        chiaveS = k
                    if v == destination:
                        chiaveD = k
                

                rs = chiaveS[0]
                cs = chiaveS[1]

                rd = chiaveD[0]
                cd = chiaveD[1]

                #DijkstraPath= nx.astar_path(G,source, destination)
                #DfsPath = dfs(newGraph, source, destination)
                DfsRandomPath = dfs(newGraph,source, destination,True)

                matrix_prob=calculate_probabilities(map_info[m].map_data, [size,size], DfsRandomPath)
                
                solution_paths.append(DfsRandomPath)
                goals.append(destination)
                manhattanDistances.append(abs(rs - rd) + abs(cs - cd))
                list_matrix_prob.append(matrix_prob[-1])
            
            visualize_map(map_info[m],DfsRandomPath,source,destination,coord_to_node,matrix_prob)
                
            mapSecond=MapSecondType(solution_paths,manhattanDistances,newGraph,goals,map_info[m].percentage_obstacles)
            item=mapSecond.getItem()
                
            file_number+=1
            datasetFile=f"DfsRandomJump8/DfsRandomJumpDatasetSize{size}File{file_number}.json"
            
            SaverItem.save_items(item,datasetFile)


                
