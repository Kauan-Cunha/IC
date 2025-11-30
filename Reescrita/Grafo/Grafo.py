class Grafo():
    def __init__(self, V:int=0):
        """Inicializa um grafo com V vértices. (Tempo esperado: O(V))"""
        self.max_or_min = 0         #se min == 0, se max == 1
        self.maximo = float('-inf')

        self.adj = {}
        self.adj_peso_invertido = {}

        self.adjacencia = self.adj
        self.num_vertices = 0
        for v in range(V):
            self.adicionar_vertice(v)

    def adicionar_vertice(self, vertice):
        """Adiciona um vértice ao grafo. (Tempo esperado: O(1))"""

        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = {}
            self.adj_peso_invertido[vertice] = {}
            self.num_vertices += 1
    
    def adicionar_aresta(self, i, j, peso=1):
        """Adiciona uma aresta ao grafo. (Tempo esperado: O(1))"""

        # Garantir que os vértices existam no grafo
        if i not in self.adjacencia:
            self.adicionar_vertice(i)
        if j not in self.adjacencia:
            self.adicionar_vertice(j)

        # Adicionar a aresta ao grafo
        self.adj[j][i] = peso
        self.adj_peso_invertido[j][i] = -peso
        
        if peso > self.maximo:
            self.maximo = peso
    
    def obter_peso(self, i, j):
        """Retorna o peso da aresta entre os vértices i e j. (Tempo esperado: O(1))"""

        if j in self.adjacencia and i in self.adjacencia[j]:
            return self.adjacencia[j][i]
        else:
            print("Aresta não existe.")
            return None

    def obter_chegada(self, i):
        """Retorna todos os vértices que chegam ao vértice i. (Tempo esperado: O(deg(i)))"""

        if i in self.adjacencia:
            return self.adjacencia[i]
        else:
            print("Vértice não existe.")
            return None

    def obter_arestas(self):
        """Retorna todas as arestas do grafo. (Tempo esperado: O(V + E))"""

        arestas = []
        for j in self.adjacencia:
            for i in self.adjacencia[j]:
                peso = self.adjacencia[j][i]
                arestas.append((i, j, peso))
        return arestas
    
    def definir_max_ou_min(self, tipo: int):
        """Define se o grafo é de maximização ou minimização. (Tempo esperado: O(1))"""
        if tipo in [0, 1]:
            self.max_or_min = tipo
            self.adjacencia = self.adj if tipo == 0 else self.adj_peso_invertido
        else:
            print("Tipo inválido. Use 0 para minimização e 1 para maximização.")

    def obter_max(self):
        
        if self.max_or_min == 0:
            return self.maximo
        
        elif self.max_or_min == 1:
            return 0
        
    def __str__(self):
        """Retorna uma representação em string do grafo. (Tempo esperado: O(V + E))"""
        resultado = ""
        for j in self.adjacencia:
            for i in self.adjacencia[j]:
                peso = self.adjacencia[j][i]
                resultado += f"{i} -> {j} (peso: {peso})\n"
        return resultado.strip()