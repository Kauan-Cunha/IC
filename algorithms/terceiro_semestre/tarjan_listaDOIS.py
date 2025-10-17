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

# ==============================================================================
# == NOVAS FUNÇÕES (USANDO GRAFO CRÍTICO COMO GUIA) ============================
# ==============================================================================

def tarjan_rec_dual(
    grafo_guia: list,
    u: int,
    disc: list,
    low: list,
    visited: list,
    pilha: list,
    naPilha: list,
    current_disc: list,
    grafo_a_modificar: list
) -> None:
    """
    Função recursiva que percorre o 'grafo_guia' para encontrar ciclos e aplica
    os cortes diretamente no 'grafo_a_modificar'.
    Ambos os grafos devem ser listas de adjacência DIRETAS.
    """
    pilha.append(u)
    naPilha[u] = True
    visited[u] = True
    disc[u] = current_disc[0]
    low[u] = disc[u]
    current_disc[0] += 1

    # A mudança crucial: percorremos as arestas do grafo-guia
    if u < len(grafo_guia):
        for vizinho_info in grafo_guia[u]:
            v, peso = vizinho_info[0], vizinho_info[1]

            if not visited[v]:
                tarjan_rec_dual(grafo_guia, v, disc, low, visited, pilha, naPilha, current_disc, grafo_a_modificar)
                low[u] = min(low[u], low[v])
            
            elif naPilha[v]: # Aresta de retorno encontrada no grafo-guia
                low[u] = min(low[u], disc[v])

                # --- AÇÃO DE CORTE DIRETAMENTE NO GRAFO PRINCIPAL ---
                print(f"  Ciclo crítico encontrado. Cortando aresta {u} -> {v} no grafo principal.")

                # O ID do novo nó é baseado no tamanho do grafo que está sendo modificado
                id_novo_no = len(grafo_a_modificar)
                grafo_a_modificar.append([]) # Adiciona o novo nó
                
                peso_metade = peso / 2
                
                # A aresta a ser removida do grafo principal deve ter o mesmo destino e peso
                aresta_original_no_principal = (v, peso)

                if aresta_original_no_principal in grafo_a_modificar[u]:
                     grafo_a_modificar[u].remove(aresta_original_no_principal)
                     # Adiciona as novas arestas no grafo principal
                     grafo_a_modificar[u].append((id_novo_no, peso_metade))
                     grafo_a_modificar[id_novo_no].append((v, peso_metade))
                else:
                    # Aviso caso a aresta crítica não seja encontrada no grafo principal.
                    # Isso não deve acontecer na sua lógica, mas é uma boa prática.
                    print(f"Aviso: Aresta crítica {u}->{v} com peso {peso} não encontrada no grafo principal para remoção.")

    if low[u] == disc[u]:
        while True:
            retirado = pilha.pop()
            naPilha[retirado] = False
            if retirado == u:
                break

def tarjan_com_guia(grafo_principal: list, grafo_guia: list) -> list:
    """
    Percorre o 'grafo_guia' para encontrar ciclos e aplica os cortes
    diretamente no 'grafo_principal'. Retorna o grafo principal modificado.
    """
    num_vertices = len(grafo_principal)
    grafo_modificado = copy.deepcopy(grafo_principal)

    pilha = []
    # O tamanho precisa ser grande o suficiente para acomodar novos nós
    tamanho_max_estimado = num_vertices * 2 
    naPilha = [False] * tamanho_max_estimado
    visited = [False] * tamanho_max_estimado
    disc = [-1] * tamanho_max_estimado
    low = [-1] * tamanho_max_estimado
    current_disc = [0]

    # Percorre os nós do grafo principal. A recursão usará o guia.
    for i in range(num_vertices):
        if not visited[i]:
            tarjan_rec_dual(grafo_guia, i, disc, low, visited, pilha, naPilha, current_disc, grafo_modificado)
    
    return grafo_modificado


# ==============================================================================
# == FUNÇÕES DE TESTE ==========================================================
# ==============================================================================

def testeTempo(listaAdj):
    time_ini = time.time()
    tarjan_lista(listaAdj)
    time_fim = time.time()
    return time_fim - time_ini

def main():
    grafo_lista_adj = [
        [(3, 1)],  # Vértice 0 aponta para 1 e peso 20
        [(0, 100), (2, 1)],   # Vértice 1 aponta para 0 e peso 5
        [],  # Vértice 2 aponta para 3 e peso 10
        [(1, 1)],   # Vértice 3 aponta para 4 e peso 1
   # Vértice 4 aponta para 2 e peso 3
    ]
    print("Grafo de teste (direto):")
    # Para desenhar, precisamos converter para o formato reverso que a função espera
    grafo_reverso_para_desenho = [[] for _ in range(len(grafo_lista_adj))]
    for u, arestas in enumerate(grafo_lista_adj):
        for v, w in arestas:
            grafo_reverso_para_desenho[v].append((u, w))
    draw.draw_weighted_graph_adj(grafo_reverso_para_desenho)

    print("\nExecutando Tarjan com Guia...")
    # Teste: O guia será o próprio grafo (cortará todos os ciclos)
    grafo_cortado = tarjan_com_guia(grafo_lista_adj, grafo_lista_adj)
    
    print("\nGrafo após o corte:")
    grafo_reverso_cortado = [[] for _ in range(len(grafo_cortado))]
    for u, arestas in enumerate(grafo_cortado):
        for v, w in arestas:
             while v >= len(grafo_reverso_cortado):
                grafo_reverso_cortado.append([])
             grafo_reverso_cortado[v].append((u, w))
    draw.draw_weighted_graph_adj(grafo_reverso_cortado)

if __name__ == '__main__':
    main()