#ESSE ARQUIVO E ESPECÍFICO PARA ARMAZENAR A DEFINIÇÃO DA ESTRUTURA DE DAODS SOB A QUAL CHAMAMOS DE GRAFO
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, lista_adjacencia = []):
        self.lista_adjacencia = lista_adjacencia
    



    def max 

    def desenhar(self, layout = 'circular'):
        """
        Desenha seu grafo ponderado.

        MADE BY AI
        """
        # 1. Usar MultiDiGraph para aceitar arestas paralelas
        G = nx.MultiDiGraph()

        for no_destino, entradas in enumerate(self.lista_adjacencia):
            if entradas:
                for pai, peso in entradas:
                    G.add_edge(pai, no_destino, weight=peso)
            else:
                if not G.has_node(no_destino):
                    G.add_node(no_destino)

        # 2. Definir Posição
        if layout == 'circular':
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)

        plt.figure(figsize=(10, 8)) # Um pouco maior para caber as curvas
        ax = plt.gca() # Pegar os eixos para desenhar

        # 3. Desenhar Nós e Rótulos dos Nós
        nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=700,
                                edgecolors='black', linewidths=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', ax=ax)

        # --- 4. Lógica para Desenhar Múltiplas Setas ---
        
        # Dicionário para rastrear quantas arestas entre (u, v) já desenhamos
        # Usamos pares ordenados (u, v) para tratar 1->0 e 0->1 separadamente
        edge_rads = {}

        for u, v, key in G.edges(keys=True):
            pair = (u, v)
            if pair not in edge_rads:
                edge_rads[pair] = []
            
            edge_rads[pair].append(key)

        # Agora desenhamos, calculando o rad
        for pair, keys in edge_rads.items():
            u, v = pair
            total_edges = len(keys)
            
            for i, key in enumerate(keys):
                edge_num = i + 1
                rad = 0
                
                if total_edges > 1:
                    # Fórmula para calcular curvaturas dinamicamente
                    # Ex (2 arestas): rad=0.1, rad=-0.1
                    # Ex (3 arestas): rad=0.2, rad=0, rad=-0.2
                    if total_edges % 2 == 1: # Ímpar
                        rad = (edge_num - (total_edges // 2) - 1) * 0.2
                    else: # Par
                        rad = (edge_num - (total_edges / 2) - 0.5) * 0.2
                
                # Caso especial: arestas recíprocas (ex: 0->1 e 1->0)
                # Elas não são paralelas, mas se sobrepõem. Vamos curvá-las.
                if total_edges == 1 and G.has_edge(v, u):
                    rad = 0.15 # Curva todas as arestas recíprocas
                
                connectionstyle = f'arc3,rad={rad}'

                nx.draw_networkx_edges(G, pos, edgelist=[(u, v, key)],
                                    connectionstyle=connectionstyle,
                                    edge_color='black', node_size=700,
                                    arrowstyle='->', arrowsize=20, ax=ax)

        # --- 5. Lógica para Rótulos Agregados (como antes) ---
        # Agora que temos múltiplas setas, o rótulo agregado faz mais sentido
        
        unique_edges_uv = set(G.edges(keys=False))
        aggregated_labels = {}
        for u, v in unique_edges_uv:
            key_data_dict = G.get_edge_data(u, v)
            weights = [str(data.get('weight', '')) for data in key_data_dict.values()]
            aggregated_labels[(u, v)] = ", ".join(weights)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=aggregated_labels,
                                    font_color='black', font_size=10,
                                    label_pos=0.3, ax=ax,
                                    # Fundo branco "falso" para não sobrepor a linha
                                    bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=0.1))

        plt.title("Grafo Ponderado (com Setas Múltiplas)")
        plt.axis('off')
        plt.show()