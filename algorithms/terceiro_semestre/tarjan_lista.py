import desenhar_grafo as draw
import time
import copy


def tarjan_rec_lista(
    adj: list,
    raiz: int,
    disc: list,
    low: list,
    visited: list,
    pilha: list,
    naPilha: list,
    current_disc: list,
    grafo_lista_result: list
) -> None:
    """
    Função recursiva do algoritmo de Tarjan para lista de adjacências.
    """
    pilha.append(raiz)
    naPilha[raiz] = True
    visited[raiz] = True
    disc[raiz] = current_disc[0]
    low[raiz] = disc[raiz]
    current_disc[0] += 1

    # Itera apenas sobre os vizinhos do vértice 'raiz'
    for vizinho in adj[raiz]:
        if not visited[vizinho[0]]:  # Caso I: Aresta descendente (Tree Edge)
            tarjan_rec_lista(
                adj, vizinho[0], disc, low, visited, pilha, naPilha, current_disc , grafo_lista_result
            )
            low[raiz] = min(low[raiz], low[vizinho[0]])

        elif naPilha[
            vizinho[0]
        ]:  # Caso II: Aresta de retorno (Back Edge) para um nó na pilha
            grafo_lista_result.append([(vizinho[0], vizinho[1]/2)])
            grafo_lista_result[raiz].append((len(grafo_lista_result) - 1, vizinho[1]/2))
            grafo_lista_result[raiz].remove(vizinho)
            low[raiz] = min(low[raiz], disc[vizinho[0]])

    # Se ao final da exploração de 'raiz', low e disc são iguais, 'raiz' é a cabeça de uma SCC
    if low[raiz] == disc[raiz]:
        while True:
            retirado = pilha.pop()
            naPilha[retirado] = False
            # Atribui o mesmo valor de low-link a todos os nós na mesma SCC
            low[retirado] = low[raiz]
            if retirado == raiz:
                break


def tarjan_lista(adj: list) -> list:
    """
    Função principal de Tarjan que inicializa as estruturas e itera sobre os vértices.
    Recebe um grafo como lista de adjacências.
    """
    num_vertices = len(adj)
    pilha = []
    adj_result = copy.deepcopy(adj)
    naPilha = [False] * num_vertices
    current_disc = [0]
    visited = [False] * num_vertices
    disc = [-1] * num_vertices
    low = [-1] * num_vertices

    # Garante que todos os nós sejam visitados, mesmo em grafos desconexos
    for i in range(num_vertices):
        if not visited[i]:
            tarjan_rec_lista(adj, i, disc, low, visited, pilha, naPilha, current_disc, adj_result)

    return low, adj_result


def testeTempo(listaAdj):
    # grafo_lista_result = listaAdj.copy()
    time_ini = time.time()
    tarjan_lista(listaAdj)
    time_fim = time.time()
    
    return time_fim - time_ini

def main():
    grafo_lista_adj = [
        [(1, 20)],  # Vértice 0 aponta para 1 e peso 20
        [(0, 5)],  # Vértice 1 aponta para 0 e peso 5
        [(3, 10)],  # Vértice 2 aponta para 3 e peso 10
        [(4, 1)],  # Vértice 3 aponta para 4 e peso 1
        [(2, 3)],  # Vértice 4 aponta para 2 e peso 3
    ]
    draw.draw_weighted_graph_adj(grafo_lista_adj)
    result = tarjan_lista(grafo_lista_adj)
    draw.draw_weighted_graph_adj(result[1])
    print(result[0], result[1])

if __name__ == "__main__":
    main()

# Exemplo de como usar com o mesmo grafo do seu código:
# A matriz original:
# grafo_adj = [
#     [ 0, 1, 0, 0, 0 ],
#     [ 1, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 1, 0 ],
#     [ 0, 0, 0, 0, 1 ],
#     [ 0, 0, 1, 0, 0 ]
# ]

# A mesma estrutura como lista de adjacências:

