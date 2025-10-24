import desenhar_grafo as draw
import time
import copy

# ==============================================================================
# == FUNÇÕES ORIGINAIS (PARA GRAFO DIRETO PADRÃO) ==============================
# ==============================================================================

def tarjan_rec_lista(
    adj: list,
    u: int,
    disc: list,
    low: list,
    visited: list,
    pilha: list,
    naPilha: list,
    current_disc: list,
    grafo_lista_result: list
) -> None:
    """
    Função recursiva do algoritmo de Tarjan para lista de adjacências diretas.
    """
    pilha.append(u)
    naPilha[u] = True
    visited[u] = True
    disc[u] = current_disc[0]
    low[u] = disc[u]
    current_disc[0] += 1

    for vizinho_info in list(grafo_lista_result[u]):
        v, peso = vizinho_info[0], vizinho_info[1]

        if not visited[v]:
            tarjan_rec_lista(
                adj, v, disc, low, visited, pilha, naPilha, current_disc, grafo_lista_result
            )
            low[u] = min(low[u], low[v])

        elif naPilha[v]:
            low[u] = min(low[u], disc[v])
            id_novo_no = len(grafo_lista_result)
            grafo_lista_result.append([])
            peso_metade = peso / 2
            if vizinho_info in grafo_lista_result[u]:
                grafo_lista_result[u].remove(vizinho_info)
                grafo_lista_result[u].append((id_novo_no, peso_metade))
                grafo_lista_result[id_novo_no].append((v, peso_metade))

    if low[u] == disc[u]:
        while True:
            retirado = pilha.pop()
            naPilha[retirado] = False
            if retirado == u:
                break

def tarjan_lista(adj: list) -> tuple:
    """
    Função principal de Tarjan que opera em um grafo de lista de adjacências diretas.
    """
    num_vertices = len(adj)
    pilha = []
    adj_result = copy.deepcopy(adj)
    naPilha = [False] * num_vertices
    current_disc = [0]
    visited = [False] * num_vertices
    disc = [-1] * num_vertices
    low = [-1] * num_vertices

    for i in range(num_vertices):
        if not visited[i]:
            tarjan_rec_lista(adj, i, disc, low, visited, pilha, naPilha, current_disc, adj_result)

    return low, adj_result

#--------------------------------------------------
#FUNÇÕES COM O GUIA
#--------------------------------------------------

def tarjan_rec_subgrafo_lista(
    u: int,
    disc: list,
    low: list,
    visited: list,
    pilha: list,
    naPilha: list,
    current_disc: list,
    grafo_principal_result: list,
    subgrafo_result: list
) -> None:
    """
    Função recursiva modificada.
    Percorre o SUBGRAFO, mas corta as arestas em AMBOS os grafos.
    """
    pilha.append(u)
    naPilha[u] = True
    visited[u] = True
    disc[u] = current_disc[0]
    low[u] = disc[u]
    current_disc[0] += 1

    # A lógica de travessia (o for) acontece sobre o SUBGRAFO
    for vizinho_info_subgrafo in list(subgrafo_result[u]):
        v, peso_subgrafo = vizinho_info_subgrafo[0], vizinho_info_subgrafo[1]

        if not visited[v]:
            tarjan_rec_subgrafo_lista(
                v, disc, low, visited, pilha, naPilha, current_disc, grafo_principal_result, subgrafo_result
            )
            low[u] = min(low[u], low[v])

        elif naPilha[v]:
            low[u] = min(low[u], disc[v])
            
            # Quando um ciclo é encontrado no subgrafo, a modificação
            # deve acontecer em AMBOS os grafos.
            
            # 1. Define o ID do novo nó com base no grafo principal (que é maior)
            id_novo_no = len(grafo_principal_result)

            # 2. Adiciona o novo nó em ambos os grafos para manter a consistência de IDs
            grafo_principal_result.append([])
            # Se o subgrafo for menor, expande ele até o tamanho necessário
            while len(subgrafo_result) <= id_novo_no:
                subgrafo_result.append([])

            # 3. Encontra a aresta correspondente no grafo principal para obter o peso original
            aresta_principal_original = None
            for aresta in grafo_principal_result[u]:
                if aresta[0] == v:
                    aresta_principal_original = aresta
                    break
            
            # Se a aresta existir em ambos, procede com o corte
            if aresta_principal_original is not None:
                peso_principal = aresta_principal_original[1]

                # 4. Modifica o SUBGRAFO
                subgrafo_result[u].remove(vizinho_info_subgrafo)
                subgrafo_result[u].append([id_novo_no, peso_subgrafo / 2])
                subgrafo_result[id_novo_no].append([v, peso_subgrafo / 2])
                
                # 5. Modifica o GRAFO PRINCIPAL
                grafo_principal_result[u].remove(aresta_principal_original)
                grafo_principal_result[u].append([id_novo_no, peso_principal / 2])
                grafo_principal_result[id_novo_no].append([v, peso_principal / 2])

    if low[u] == disc[u]:
        while True:
            retirado = pilha.pop()
            naPilha[retirado] = False
            if retirado == u:
                break

def tarjan_subgrafo_lista(grafo_principal: list, subgrafo: list) -> tuple:
    """
    Função principal modificada para operar em um subgrafo,
    refletindo as mudanças no grafo principal.
    """
    # As estruturas de controle usam o tamanho do grafo principal para garantir
    # que todos os vértices sejam mapeados corretamente.
    num_vertices = len(grafo_principal)
    
    pilha = []
    # Cria cópias para não modificar os grafos originais
    grafo_principal_result = copy.deepcopy(grafo_principal)
    subgrafo_result = copy.deepcopy(subgrafo)

    naPilha = [False] * num_vertices
    current_disc = [0]
    visited = [False] * num_vertices
    disc = [-1] * num_vertices
    low = [-1] * num_vertices

    # A iteração inicial pode ser feita sobre os vértices do subgrafo
    # ou do grafo principal. Fazer sobre o principal é mais seguro.
    for i in range(num_vertices):
        # Apenas inicia a busca para nós que existem no subgrafo e não foram visitados
        if i < len(subgrafo_result) and subgrafo_result[i] is not None and not visited[i]:
            tarjan_rec_subgrafo_lista(
                i, disc, low, visited, pilha, naPilha, current_disc, grafo_principal_result, subgrafo_result
            )

    return low, grafo_principal_result, subgrafo_result

def main():
    grafo = [
        [(3, 1)],  # Vértice 0 aponta para 1 e peso 20
        [(0, 100), (2, 1)],   # Vértice 1 aponta para 0 e peso 5
        [(1, 50)],  # Vértice 2 aponta para 3 e peso 10
        [(1, 1)],   # Vértice 3 aponta para 4 e peso 1
    ]

    sub_grafo =[
        [(3, 1)],  
        [(0, 100), (2, 1)],  
        [],  
        [(1, 1)],   
    ]
    print("Grafo de teste (direto):")
    draw.draw_weighted_graph_adj(sub_grafo)
    result = tarjan_subgrafo_lista(grafo, sub_grafo)
    draw.draw_weighted_graph_adj(result[1])
if __name__ == '__main__':
    main()