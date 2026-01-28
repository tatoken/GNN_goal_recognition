import os
import sys
import random
import platform
from PyQt6.QtWidgets import QApplication

from Datasets.Database_blender import concatena_json
from Map_Manager import Map_loader
from Map_Manager.Map_graph_manager import Map_graph_manager
from Map_Manager import Output_instance_saver
from Map_Manager.Data.Map_output import Map_output
from Path_Visualizer.window import VisualizerWindow

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def dfs(graph, start, goal, randomJump=False):
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

def visualize_map( raw_map,path, format_mapping_map,delay,matrix_list=None):
    """
    Funzione wrapper per lanciare la nuova GUI.
    ATTENZIONE: Questa funzione è BLOCCANTE. Il codice si ferma qui finché
    la finestra non viene chiusa.
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = VisualizerWindow(
        raw_map,
        path,
        format_mapping_map,
        delay,
        matrix_list
    )
    
    window.show()
    
    # 3. Avvia il loop. Quando chiudi la finestra, l'esecuzione riprende dopo questa riga.
    app.exec()

def print_info_of_current_process(source_destinations_per_map, source_destination):
    print("█"*(source_destination+1),end="")
    print("░"*(source_destinations_per_map-(source_destination+1)),end="")
    print(f"{source_destination+1}/{source_destinations_per_map}")

if __name__ == "__main__":

    # --- CONFIGURAZIONE ---
    number_of_files = 100
    size = 8
    starting_file=10
    delay=100
    source_destinations_per_map = 10
    output_dir = f"Datasets/Resulted_dataset/DfsRandomJump{size}/"
    
    # [IMPORTANTE] Imposta a True se vuoi vedere la grafica e fermarti.
    VISUALIZE_ONE_AND_STOP = True 

    os.makedirs(output_dir, exist_ok=True)
    
    # Contatore globale per i file di output
    file_number_counter = 23

    for file_idx in range(starting_file, number_of_files + 1): 

        file_name = f"Datasets/Modified_dataset/maps_dataset_{size}/maps_dataset_{size}_{file_idx}.json"
        
        try:
            maps_in_file = Map_loader.load_map_from_json(file_name)
        except FileNotFoundError:
            print(f"File non trovato: {file_name}")
            continue

        # Nota: iteriamo su tutte le mappe nel file
        for map_obj in maps_in_file: 
    
            solution_paths = []
            goals = []
            manhattanDistances = []
            list_matrix_prob_final = [] 
            
            last_path = None
            last_source = None
            last_dest = None
            last_prob_frames = None

            graphMapManager = Map_graph_manager(map_obj)
            newGraph = graphMapManager.get_graph()

            print(f"\nProcessing File:{file_idx} - Mappa ID:{map_obj.map_id}")

            for i in range(source_destinations_per_map):
                print_info_of_current_process(source_destinations_per_map, i)
                
                source, destination = graphMapManager.generate_random_source_destination()
                
                start_id = graphMapManager.coord_to_node_id(source)
                goal_id = graphMapManager.coord_to_node_id(destination)
                
                DfsRandomPath = dfs(newGraph, start_id, goal_id, randomJump=True)

                if DfsRandomPath is None:
                    # Gestione caso path non trovato (se grafo non connesso)
                    continue

                # Calcolo probabilità (ritorna lista di matrici [frame1, frame2...])
                matrix_prob_frames = graphMapManager.calculate_probabilities(DfsRandomPath)     

                # Salvataggio dati per dataset
                solution_paths.append(DfsRandomPath)
                goals.append(destination)
                manhattanDistances.append(abs(source[0] - destination[0]) + abs(source[1] - destination[1]))

                if matrix_prob_frames:
                    list_matrix_prob_final.append(matrix_prob_frames[-1])
                
                last_path = DfsRandomPath
                last_source = source
                last_dest = destination
                last_prob_frames = matrix_prob_frames

            # --- SALVATAGGIO ---
            mapSecond = Map_output(
                solution_paths,
                manhattanDistances,
                graphMapManager,
                goals,
                list_matrix_prob_final,
                map_obj.percentage_obstacles
            )
            item = mapSecond.getItem()
            file_number_counter += 1
            datasetFile = f"{output_dir}/DfsRandomJumpDatasetSize{size}File{file_number_counter}.json"
            Output_instance_saver.save_items(item, datasetFile)

            # --- VISUALIZZAZIONE ---
            if VISUALIZE_ONE_AND_STOP:
                print("\n\n[INFO] Avvio visualizzazione grafica...")
                print(f"Source: {last_source}, Dest: {last_dest}")
                
                visualize_map(
                    graphMapManager.get_map().map_data,
                    last_path,  
                    graphMapManager.coord_to_node,
                    delay,
                    last_prob_frames
                )
                
                print("[INFO] Finestra chiusa. Interruzione script (Debug Mode).")
                sys.exit(0) # Esce dopo la prima visualizzazione

            clear()
            
    if not VISUALIZE_ONE_AND_STOP:
        concatena_json(output_dir, f"DfsRandomJump{size}.json")