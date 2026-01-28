import random

import numpy as np

class Map_graph_manager:
    def __init__(self, map_obj):
        self.map = map_obj
        self.graph = {}              # nodo → lista nodi adiacenti
        self.coord_to_node = {}      # (r,c) → nodo
        self.node_to_coord = {}      # nodo → (r,c)
        
        # Genera subito il grafo e le tabelle di traduzione
        self._build_graph()

    def _build_graph(self):
        rows = len(self.map.map_data)
        cols = len(self.map.map_data[0]) if rows > 0 else 0
        
        node_counter = 0
        
        for r in range(rows):
            for c in range(cols):
                if self.map.map_data[r][c] == 0:
                    self.coord_to_node[(r, c)] = node_counter
                    self.node_to_coord[node_counter] = (r, c)
                    node_counter += 1
        
        for (r, c), node in self.coord_to_node.items():
            neighbors = []
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.coord_to_node:
                    neighbors.append(self.coord_to_node[(nr, nc)])
            self.graph[node] = neighbors

    def coord_to_node_id(self, coord):
        """
        Restituisce l'indice del nodo corrispondente a (r,c).
        Se la cella è occupata o fuori dalla mappa → -1
        """
        return self.coord_to_node.get((coord[0], coord[1]), -1)

    def node_id_to_coord(self, node_id):
        """
        Restituisce le coordinate (r,c) corrispondenti al nodo.
        Se non esiste → -1
        """
        return self.node_to_coord.get(node_id, -1)
    
    def get_map(self):
        return self.map

    def get_graph(self):
        return self.graph

    def get_coord_to_node_map(self):
        return self.coord_to_node

    def get_node_to_coord_map(self):
        return self.node_to_coord
    
    def generate_random_source_destination(self):
        numberOfFreeCell=len(self.graph.items())

        source=random.randint(0,numberOfFreeCell-1)
        destination=random.randint(0,numberOfFreeCell-1)

        while not source!=destination:
            destination=random.randint(0,numberOfFreeCell-1)
        
        return [self.node_id_to_coord(source),self.node_id_to_coord(destination)]
    





    
    def calculate_probabilities(self,path):
        size =  len(self.map.map_data)
        matrix_prob = np.zeros((size, size))
        update_matrix_prob=[]

        for t in range(len(path) - 1):

            direction = self.calculate_direction(self.node_id_to_coord(path[t]), self.node_id_to_coord(path[t+1]))
            matrix_prob += self.direction_prob(self.map.map_data, size, self.node_id_to_coord(path[t]), direction)

            matrix_prob /= matrix_prob.sum()
            update_matrix_prob.append(matrix_prob.copy())

        return update_matrix_prob
    
    def count_obstacles_on_path(self,map_data, start, end):
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


    def direction_prob(self,map, size, pos_t, direction, alpha=0.1, beta=1.5, attenuation=0.4, gamma=0.4):
        """
        Calcola una matrice di probabilità che si propaga dalla posizione pos_t nella direzione data,
        tenendo conto degli ostacoli che attenuano la propagazione.

        Args:
            map_data (np.ndarray): matrice binaria (0=libero, 1=ostacolo)
            pos_t (tuple): posizione attuale (r, c)
            direction (str): direzione di movimento ('up', 'down', 'left', 'right')
            alpha (float): coeff. di decadimento con la distanza
            beta (float): coeff. che rafforza la direzione scelta
            gamma (float): coeff. di attenuazione per ogni ostacolo sulla linea di vista
        """
        prob = np.zeros((size, size))

        for r in range(size):
            for c in range(size):
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
                n_obs = self.count_obstacles_on_path(map, pos_t, (r, c))

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


    def calculate_direction(self,pos_t, pos_t1):
        if pos_t1[0] < pos_t[0]:
            return 'up'
        elif pos_t1[0] > pos_t[0]:
            return 'down'
        elif pos_t1[1] < pos_t[1]:
            return 'left'
        elif pos_t1[1] > pos_t[1]:
            return 'right'
