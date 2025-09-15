class GraphMapFirstType():

    def __init__(self,map):
        self.map=map

    def translateMapIntoGraph(self):
        graph = {}
        rows = len(self.map.map_data)
        cols = len(self.map.map_data[0]) if rows > 0 else 0
        

        for r in range(rows):
            for c in range(cols):
                if self.map.map_data[r][c] == 0:  # 0 = cella libera
                    node = r*self.map.size+c+1
                    neighbors = []
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # su, giù, sinistra, destra
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if self.map.map_data[nr][nc] == 0:
                                neighbors.append((nr, nc))
                    neighborsTranslated=[]
                    for neighbor in neighbors:
                        neighborsTranslated.append(neighbor[0]*self.map.size+(neighbor[1]+1))  
                    graph[node] = neighborsTranslated
        return graph