import networkx as nx
import matplotlib.pyplot as plt

class GrafoPonderado:
    """
    Uma classe para representar um grafo direcionado e com pesos
    a partir de uma matriz de custo.
    """

    def __init__(self, matriz_custo):
        """
        Construtor da classe. Inicializa o grafo a partir de uma matriz de custo.

        Args:
            matriz_custo (list of list of int/float): Uma matriz de adjacência onde
                                                      matriz_custo[i][j] é o peso da
                                                      aresta do nó i para o nó j.
                                                      Use float('inf') ou 0 para ausência de aresta.
        """
        self.num_vertices = len(matriz_custo)

        if any(len(row) != self.num_vertices for row in matriz_custo):
            raise ValueError("A matriz de custo deve ser quadrada.")
        
        self.matriz_custo = matriz_custo
        self.G = nx.DiGraph()

        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                peso = self.matriz_custo[i][j]
                if peso > 0 and peso != float('inf'):
                    self.G.add_edge(i, j, weight=peso)

    def mostrar_grafico(self):
        """
        Renderiza e exibe uma representação gráfica do grafo.
        O peso é colocado no meio da aresta, com um fundo branco para
        criar um efeito de linha interrompida.
        """
        pos = nx.spring_layout(self.G, seed=42)
        
        # 1. SEPARAR ARESTAS
        single_edges = []
        reciprocal_edges = []
        for u, v in self.G.edges():
            if self.G.has_edge(v, u):
                reciprocal_edges.append((u, v))
            else:
                single_edges.append((u, v))

        # 2. DESENHAR NÓS E ARESTAS
        nx.draw_networkx_nodes(self.G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_labels(self.G, pos, font_size=12, font_family='sans-serif')
        nx.draw_networkx_edges(self.G, pos, edgelist=single_edges, width=1.5, alpha=0.7, edge_color='gray', arrows=True, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_edges(self.G, pos, edgelist=reciprocal_edges, width=1.5, alpha=0.7, edge_color='orange', arrows=True, arrowstyle='->', arrowsize=20, connectionstyle='arc3,rad=0.2')

        # 3. DESENHAR RÓTULOS DAS ARESTAS (COM O TRUQUE DO BBOX)
        
        # Propriedades da caixa que vai "limpar" o fundo do texto
        bbox_props = dict(boxstyle="round,pad=0.2", # Caixa arredondada com padding
                          facecolor="white",         # Cor de fundo branca
                          edgecolor="none")          # Sem borda

        single_edge_labels = {edge: self.G.edges[edge]['weight'] for edge in single_edges}
        reciprocal_edge_labels = {edge: self.G.edges[edge]['weight'] for edge in reciprocal_edges}
        
        nx.draw_networkx_edge_labels(self.G, pos, 
                                     edge_labels=single_edge_labels, 
                                     font_color='red',
                                     bbox=bbox_props) # Aplica a caixa
        
        nx.draw_networkx_edge_labels(self.G, pos, 
                                     edge_labels=reciprocal_edge_labels, 
                                     label_pos=0.3,
                                     font_color='red',
                                     bbox=bbox_props) # Aplica a caixa

        # 4. EXIBIR O GRÁFICO
        plt.title("Representação Gráfica do Grafo")
        plt.axis('off')
        plt.show()