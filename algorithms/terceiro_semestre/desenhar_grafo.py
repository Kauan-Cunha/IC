import networkx as nx
import matplotlib.pyplot as plt

def draw_weighted_graph_adj(grafo_ponderado, layout='circular'):
    """
    Desenha um grafo direcionado e ponderado a partir de uma lista de adjacência reversa,
    onde cada sublista contém tuplas (pai, peso), ou seja, arestas que chegam em cada nó.

    Args:
        grafo_ponderado (list): Lista de listas, cada sublista representa as arestas que chegam em um nó.
                                Cada tupla é (pai, peso).
        layout (str): O algoritmo de layout a ser usado ('circular', 'spring', etc.).
    """
    G = nx.DiGraph()

    # Adiciona as arestas ponderadas ao grafo
    for no_destino, entradas in enumerate(grafo_ponderado):
        for pai, peso in entradas:
            G.add_edge(pai, no_destino, weight=peso)

    # Define a posição dos nós
    if layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 6))

    # Desenha os componentes do grafo
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=700,
                             edgecolors='black', linewidths=1.5)

    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    nx.draw_networkx_edges(G, pos, edge_color='black', node_size=700,
                           arrowstyle='->', arrowsize=20,
                           connectionstyle='arc3,rad=0.15')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                font_color='black', font_size=10,
                                label_pos=0.3)

    plt.title("Grafo Ponderado")
    plt.axis('off')
    plt.show()

def main():
    """
    Função de exemplo para demonstrar o grafo com arestas recíprocas (0 <-> 1).
    """
    grafo_com_ciclo = [
        [(1, 5), (3, 4)],  # Nó 0
        [(0, 2), (2, 3)],  # Nó 1
        [(3, 1)],          # Nó 2
        [(0, 4)]           # Nó 3
    ]

    print("Desenhando grafo com pesos de arestas recíprocas separados...")
    draw_weighted_graph_adj(grafo_com_ciclo)

if __name__ == "__main__":
    main()