class GraphMapFirstType():

    def __init__(self,map):
        self.map=map

    def translateMapIntoGraph(self):
        rows = len(self.map.map_data)
        cols = len(self.map.map_data[0]) if rows > 0 else 0
        graph = {}
        coord_to_node = {}
        node_counter = 0   # numerazione a partire da 1 (come nel tuo esempio)

        # Primo passaggio: assegno un numero solo alle celle libere
        for r in range(rows):
            for c in range(cols):
                if self.map.map_data[r][c] == 0:  # libera
                    coord_to_node[(r, c)] = node_counter
                    node_counter += 1


        # Secondo passaggio: costruisco il grafo usando quella mappatura
        for (r, c), node in coord_to_node.items():
            neighbors = []
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # su, giù, sinistra, destra
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_to_node:  # se è una cella libera numerata
                    neighbors.append(coord_to_node[(nr, nc)])
            graph[node] = neighbors

        return graph,coord_to_node