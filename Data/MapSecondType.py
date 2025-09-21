from Data.Item import Item

class MapSecondType:

    def __init__(self,paths,mapGraph,goals):
        self.paths=paths

        self.map=[]
        for nodo, _ in mapGraph.items():
            self.map.append(nodo)

        self.goals=goals
        
        self.item=Item(self.makeV(),self.makeE(mapGraph),self.makeY(),self.paths)

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
