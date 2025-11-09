from Map_Manager.Item import Item
import numpy as np

class MapSecondType:

    def __init__(self,paths,manhattanDistances,mapGraph,goals,obstaclePerc):
        self.paths=paths
        self.manhattanDistances=manhattanDistances

        self.map=[]
        for nodo, _ in mapGraph.items():
            self.map.append(nodo)

        self.goals=goals
        
        self.item=Item(self.makeV(),self.makeE(mapGraph),self.makeY(),self.paths,self.computeOptimalityOf(),self.computeAvgLenght(),obstaclePerc)


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
        
            
    def makeY(self):
        resY=[]
        for goal in self.goals:
            res=[]
            for cell in self.map:
                if(cell==goal):
                    res.append(1)
                else:
                    res.append(0)
            resY.append(res)
        return resY


    def makeE(self,mapGraph):
        res=[]
        
        for nodo, vicini in mapGraph.items():
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
