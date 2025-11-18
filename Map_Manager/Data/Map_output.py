from Map_Manager.Data.Map_path_solution_output import Map_path_solution_output
import numpy as np

from Map_Manager.Map_graph_manager import Map_graph_manager

class Map_output:

    def __init__(self,paths,manhattanDistances,graphMapManager:Map_graph_manager,goals,matrix_percentage_list,obstaclePerc):
        self.paths=paths
        self.manhattanDistances=manhattanDistances
        self.graphMapManager=graphMapManager
        self.size=len(graphMapManager.get_map().map_data)

        self.map=[]
        for nodo, _ in graphMapManager.get_graph().items():
            self.map.append(nodo)

        self.goals=goals
        
        self.item=Map_path_solution_output(self.makeV(),self.makeE(),self.makeY(matrix_percentage_list),self.paths,self.computeOptimalityOf(),self.computeAvgLenght(),obstaclePerc)


    def computeOptimalityOf(self):
       result=[]
       for pathNr in range(len(self.paths)):
            result.append(self.manhattanDistances[pathNr]/(len(self.paths[pathNr])-1)*100)
       return result
        

    def computeAvgLenght(self):
        sum=0
        for path in self.paths:
            sum+=len(path)
        return sum/len(self.paths)


    def makeV(self):
        resV=[]
        for path in self.paths:
            res=[]
            for cell in self.map:
                if(cell in path):
                    if(cell==path[-1]):
                        res.append([0,1,0])
                    else:
                        res.append([0,0,1])
                else:
                    res.append([1,0,0])
            resV.append(res)
        return resV
        
            
    def makeY(self,matrix_percentage_list):
        resY=[]
        for matrix_percentage in matrix_percentage_list:

            flatted_matrix = []
            for row in range(self.size):
                for col in range(self.size):
                    if(self.graphMapManager.get_map().map_data[row][col]==0):
                        flatted_matrix.append(matrix_percentage[row][col])

            resY.append(flatted_matrix)
        return resY


    def makeE(self):
        res=[]
        
        for nodo, vicini in self.graphMapManager.get_graph().items():
            for vicino in vicini:
                res.append([nodo,vicino])

        return res
    

    def getItem(self):
        return self.item
    
    def direction_prob(map_shape, pos_t, direction, alpha=0.3, beta=1.5):
        rows, cols = map_shape
        prob = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                d = abs(r - pos_t[0]) + abs(c - pos_t[1])
                match = 0
                if direction == 'up' and r < pos_t[0]: match = 1
                if direction == 'down' and r > pos_t[0]: match = 1
                if direction == 'left' and c < pos_t[1]: match = 1
                if direction == 'right' and c > pos_t[1]: match = 1
                prob[r, c] = np.exp(-alpha*d) * (1 + beta*match)
        prob /= prob.sum()
        return prob
