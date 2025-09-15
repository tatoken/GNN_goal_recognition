from Data.Item import Item

class MapSecondType:

    def __init__(self,path,mapGraph,goal):
        self.path=path
        self.map=[]
        for nodo, vicini in mapGraph.items():
            self.map.append(nodo)

        self.goal=goal
        self.E=self.makeE(mapGraph)
        self.Y=self.makeY()

        self.items=[]
        for i in range(2,len(path)+1):
            self.items.append(Item(self.makeV(i),self.E,self.Y))

    def makeV(self,index):
        res=[]
        pathCutted=self.path[0:index]
        for cell in self.map:
            if(cell in pathCutted):
                if(cell==pathCutted[-1]):
                    res.append([0,1,0])
                else:
                    res.append([0,0,1])
            else:
                res.append([1,0,0])

        return res
            
    def makeY(self):
        res=[]
        for cell in self.map:
            if(cell==self.goal):
                res.append(1)
            else:
                res.append(0)
        return res

    def makeE(self,mapGraph):
        res=[]
        
        for nodo, vicini in mapGraph.items():
            for vicino in vicini:
                res.append([nodo,vicino])

        return res
    
    def getItems(self):
        return self.items
