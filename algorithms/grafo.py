class GrafoList:
    def __init__(self, nNodes):
        self.nNodes = nNodes
        self.listaAdj = []
        
        for i in range(nNodes):
            self.listaAdj.append([])