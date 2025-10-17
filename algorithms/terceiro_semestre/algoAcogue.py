import flor_adj as flor
import desenhar_grafo as draw
import grafoCriticoAlt as critico
import tarjan_listaDOIS as tarjan
import copy

def converter_adj_reversa_para_direta(adj_reversa: list) -> list:
    """
    Converte uma lista de adjacência reversa para uma lista de adjacência direta.

    Na representação reversa (usada por 'floria'), adj[i] contém as arestas que CHEGAM em i.
    Ex: adj_reversa[filho] = [(pai, peso), ...]

    Na representação direta (usada por 'tarjan'), adj[i] contém as arestas que SAEM de i.
    Ex: adj_direta[pai] = [(filho, peso), ...]

    Args:
        adj_reversa (list): O grafo em formato de lista de adjacência reversa.

    Returns:
        list: O mesmo grafo em formato de lista de adjacência direta.
    """
    # 1. Determina o número total de nós no grafo.
    #    Começamos com o número de listas (que é o maior nó de destino).
    num_nos = len(adj_reversa)
    #    Depois, verificamos se existe algum nó de origem (pai) com índice maior.
    for arestas in adj_reversa:
        for pai, _ in arestas:
            if pai + 1 > num_nos:
                num_nos = pai + 1

    # 2. Inicializa a lista de adjacência direta com listas vazias para cada nó.
    adj_direta = [[] for _ in range(num_nos)]

    # 3. Percorre a lista reversa para preencher a lista direta.
    #    'filho' é o índice do nó de destino.
    for filho, arestas_de_entrada in enumerate(adj_reversa):
        # 'pai' é o nó de origem da aresta.
        for pai, peso in arestas_de_entrada:
            # Se a aresta é de 'pai' para 'filho', na lista direta,
            # adicionamos a tupla (filho, peso) na lista do 'pai'.
            adj_direta[pai].append((filho, peso))

    return adj_direta


def converter_adj_direta_para_reversa(adj_direta: list) -> list:
    """
    Converte uma lista de adjacência direta para uma lista de adjacência reversa.

    Args:
        adj_direta (list): O grafo em formato de lista de adjacência direta.

    Returns:
        list: O mesmo grafo em formato de lista de adjacência reversa.
    """
    # A lógica é a mesma da função anterior, apenas invertida.
    num_nos = len(adj_direta)
    for arestas in adj_direta:
        for filho, _ in arestas:
            if filho + 1 > num_nos:
                num_nos = filho + 1

    adj_reversa = [[] for _ in range(num_nos)]

    # 'pai' é o índice do nó de origem.
    for pai, arestas_de_saida in enumerate(adj_direta):
        # 'filho' é o nó de destino.
        for filho, peso in arestas_de_saida:
            # Se a aresta é de 'pai' para 'filho', na lista reversa,
            # adicionamos a tupla (pai, peso) na lista do 'filho'.
            adj_reversa[filho].append((pai, peso))

    return adj_reversa

def acougue_teste(custo_reverso, media_esperada):
    """
    Versão da função 'acougue' modificada para retornar o número de iterações.
    """
    grafo_modificado_direto = converter_adj_reversa_para_direta(custo_reverso)
    iteracao = 0

    while True:
        grafo_modificado_reverso = converter_adj_direta_para_reversa(grafo_modificado_direto)
        
        # O segundo argumento de floria é ignorado se você fez as correções anteriores
        vetor, valor, _ = flor.floria(grafo_modificado_reverso, 200)

        # Condição de parada principal
        if valor <= media_esperada:
            break
        
        # Limite de segurança para evitar loops infinitos em casos extremos
        if iteracao >= 100: 
            # print("Aviso: Limite de 100 iterações atingido.")
            break
        
        # Encontre o subgrafo crítico
        custo_critico_reverso = critico.grafoCritico_adj(grafo_modificado_reverso, valor, vetor)
        
        # Trava de segurança para problemas de precisão numérica
        num_arestas_criticas = sum(len(arestas) for arestas in custo_critico_reverso)
        if num_arestas_criticas == 0:
            # print(f"Aviso: Nenhuma aresta crítica encontrada para a média {valor:.4f}. Interrompendo.")
            break

        # Prossiga com o corte
        iteracao += 1 # Incremente o contador apenas quando um corte for realizado
        custo_critico_direto = converter_adj_reversa_para_direta(custo_critico_reverso)
        grafo_modificado_direto = tarjan.tarjan_com_guia(grafo_modificado_direto, custo_critico_direto)

    return iteracao # Retorna o número de cortes realizados


def acougue(custo_reverso, media_esperada):
    # Usaremos o formato direto para Tarjan e reverso para Floria
    grafo_modificado_direto = converter_adj_reversa_para_direta(custo_reverso)
    iteracao = 0

    while True:
        # 1. Converta para reverso para usar Floria
        draw.draw_weighted_graph_adj(grafo_modificado_direto)
        grafo_modificado_reverso = converter_adj_direta_para_reversa(grafo_modificado_direto)
        vetor, valor, _ = flor.floria(grafo_modificado_reverso, 500)
        print(f"\nIteração {iteracao}: Média atual = {valor:.4f}")

        if valor <= media_esperada:
            break
        iteracao += 1

        # 2. Encontre o subgrafo crítico (em formato reverso)
        custo_critico_reverso = critico.grafoCritico_adj(grafo_modificado_reverso, valor, vetor)
        # Converta para o formato direto, que é o que Tarjan espera
        custo_critico_direto = converter_adj_reversa_para_direta(custo_critico_reverso)

        # 3. Chame a nova função de Tarjan
        #    - Grafo principal para MODIFICAR: grafo_modificado_direto
        #    - Grafo guia para PERCORRER: custo_critico_direto
        grafo_modificado_direto = tarjan.tarjan_com_guia(grafo_modificado_direto, custo_critico_direto)


    print(f"\nProcesso finalizado.")
    return converter_adj_direta_para_reversa(grafo_modificado_direto) # Retorna no formato original

def main():
    c_adj = [
        [(0, 274)],
        [(1, 267), (4, 41)],
        [(0, 28), (1, 35), (3, 44), (4, 242)],
        [(0, 7), (2, 277), (3, 29)],
        [(1, 27), (3, 212)]
    ]
    
    print("Grafo Original:")
    draw.draw_weighted_graph_adj(c_adj)
    
    # Tenta reduzir a média do ciclo para menos de 40.
    # O ciclo (0,1) de média 51 será cortado.
    result = acougue(c_adj, 30)
    
    print("\nGrafo Final Modificado:")
    draw.draw_weighted_graph_adj(result)

def teste_convergencia(custo_adj, media):
    return acougue_teste(custo_adj, media)

if __name__ == "__main__":
    main()