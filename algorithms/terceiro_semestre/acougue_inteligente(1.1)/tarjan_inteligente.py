import desenhar_grafo as draw
import time
import copy

#--------------------------------------------------
#FUNÇÕES COM O GUIA (MODIFICADAS)
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
    subgrafo_result: list,
    # --- NOVOS PARÂMETROS ---
    parent: list,
    parent_edge_sub: list,
    parent_edge_princ: list
) -> None:
    """
    Função recursiva modificada.
    Percorre o SUBGRAFO. Ao encontrar um ciclo, identifica TODAS as arestas
    do ciclo, encontra a de MAIOR peso absoluto (do grafo principal) e
    corta APENAS ela em AMBOS os grafos.
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
            # --- MODIFICAÇÃO: Rastrear pais e arestas da árvore ---
            parent[v] = u
            
            # Encontra a aresta principal correspondente
            aresta_principal_arvore = None
            for aresta in grafo_principal_result[u]:
                if aresta[0] == v:
                    aresta_principal_arvore = aresta
                    break
            
            # Salva ambas as arestas da árvore
            if aresta_principal_arvore is not None:
                parent_edge_sub[v] = vizinho_info_subgrafo
                parent_edge_princ[v] = aresta_principal_arvore
            # --- Fim da Modificação ---
            
            tarjan_rec_subgrafo_lista(
                v, disc, low, visited, pilha, naPilha, current_disc, 
                grafo_principal_result, subgrafo_result,
                parent, parent_edge_sub, parent_edge_princ # Passa adiante
            )
            low[u] = min(low[u], low[v])

        elif naPilha[v]:
            # Tarjan padrão
            low[u] = min(low[u], disc[v])
            
            # --- INÍCIO DA NOVA LÓGICA DE CORTE ---
            # Ciclo detectado (u, v). Agora vamos encontrar a aresta de maior peso no ciclo.
            
            max_peso_abs = -1
            # (u_c, v_c, aresta_sub_obj, aresta_princ_obj)
            aresta_a_cortar = None

            # 1. Avaliar a aresta de retorno (u, v)
            aresta_principal_original = None
            for aresta in grafo_principal_result[u]:
                if aresta[0] == v:
                    aresta_principal_original = aresta
                    break
            
            if aresta_principal_original is not None:
                peso_principal_back = aresta_principal_original[1]
                max_peso_abs = abs(peso_principal_back)
                # Salva (u, v, aresta_sub, aresta_princ)
                aresta_a_cortar = (u, v, vizinho_info_subgrafo, aresta_principal_original)

            # 2. Avaliar as arestas da árvore (de u subindo até v)
            curr = u
            while curr != v:
                p = parent[curr]
                if p == -1: break # Segurança, não deve acontecer num ciclo
                
                aresta_sub_tree = parent_edge_sub[curr]
                aresta_princ_tree = parent_edge_princ[curr]
                
                if aresta_sub_tree and aresta_princ_tree:
                    peso_princ_tree = aresta_princ_tree[1]
                    
                    if abs(peso_princ_tree) > max_peso_abs:
                        max_peso_abs = abs(peso_princ_tree)
                        # Salva (p, curr, aresta_sub, aresta_princ)
                        aresta_a_cortar = (p, curr, aresta_sub_tree, aresta_princ_tree)
                
                curr = p
            
            # 3. Realizar o corte na aresta "vencedora"
            if aresta_a_cortar is not None:
                u_cut, v_cut, a_sub_cut, a_princ_cut = aresta_a_cortar
                
                # Se a aresta a cortar for a de retorno (u,v), os objetos já
                # são os corretos. Se for uma da árvore (p, curr), também são.
                peso_subgrafo_cut = a_sub_cut[1]
                peso_principal_cut = a_princ_cut[1]

                # Define o ID do novo nó com base no grafo principal
                id_novo_no = len(grafo_principal_result)

                # Adiciona o novo nó em ambos os grafos
                grafo_principal_result.append([])
                while len(subgrafo_result) <= id_novo_no:
                    subgrafo_result.append([])

                # Modifica o SUBGRAFO
                subgrafo_result[u_cut].remove(a_sub_cut)
                subgrafo_result[u_cut].append([id_novo_no, peso_subgrafo_cut / 2])
                subgrafo_result[id_novo_no].append([v_cut, peso_subgrafo_cut / 2])
                
                # Modifica o GRAFO PRINCIPAL
                grafo_principal_result[u_cut].remove(a_princ_cut)
                grafo_principal_result[u_cut].append([id_novo_no, peso_principal_cut / 2])
                grafo_principal_result[id_novo_no].append([v_cut, peso_principal_cut / 2])
            
            # --- FIM DA NOVA LÓGICA DE CORTE ---

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
    num_vertices = len(grafo_principal)
    
    pilha = []
    grafo_principal_result = copy.deepcopy(grafo_principal)
    subgrafo_result = copy.deepcopy(subgrafo)

    naPilha = [False] * num_vertices
    current_disc = [0]
    visited = [False] * num_vertices
    disc = [-1] * num_vertices
    low = [-1] * num_vertices

    # --- NOVOS ARRAYS DE RASTREAMENTO ---
    parent = [-1] * num_vertices
    parent_edge_sub = [None] * num_vertices
    parent_edge_princ = [None] * num_vertices
    # --- FIM DA MODIFICAÇÃO ---

    for i in range(num_vertices):
        if i < len(subgrafo_result) and subgrafo_result[i] is not None and not visited[i]:
            tarjan_rec_subgrafo_lista(
                i, disc, low, visited, pilha, naPilha, current_disc, 
                grafo_principal_result, subgrafo_result,
                parent, parent_edge_sub, parent_edge_princ # Passa os novos arrays
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
    
    print("Resultado")
    draw.draw_weighted_graph_adj(result[1])
if __name__ == '__main__':
    main()