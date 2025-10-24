import numpy as np
import desenhar_grafo as draw
import grafoCriticoAlt as critic
import copy

def oleinik(f, c_adj, m):
    """
    Calcula a constante de lax-oleinik e o argmax(nó que maximiza).
    """
    Tc = []
    Argmin = []
    MinCost = []
    for i in range(len(c_adj)):
        
        # Se o nó 'i' não tiver arestas de entrada (é um nó de origem)
        if not c_adj[i]:
            Tc.append(f[i])      # O valor da função não se altera, pois não há max a ser feito.
            Argmin.append(i)     # O nó aponta para si mesmo, pois não tem predecessor.
            MinCost.append(float('inf'))
            continue             # Pula para a próxima iteração do laço principal.

        # Se o nó tiver arestas de entrada, executa a lógica original
        j = -1 # Inicializa com um valor inválido para garantir que seja atualizado
        u = float("inf")
        custo_aresta_min = float("inf")
        for pai in c_adj[i]:
            valor_candidato = f[pai[0]] - m + pai[1]
            if valor_candidato < u:
                u = valor_candidato
                j = pai[0]
                custo_aresta_min = pai[1]

        Tc.append(u)
        Argmin.append(j)
        MinCost.append(custo_aresta_min)

    return Tc, Argmin, MinCost

def floria_rec(custo ,conjunto_v, f, m, iterada=1):
    """Função recursiva que calcula simutaneamente a Constate Cíclica Minimal e os Corretores de um grafo.
        Entrada:
        custo: matriz custo de grafo conexo. (em arestas inexistentes o valor deve ser math.inf);
        conjunto_v: vetor de tamanho #V(G) com todas as entradas [1]. (Marca se o vértice foi otimizado.);
        f: vetor/função arbitrária de tamanho #V(G);
    """

    #Esse custo_sigma guarda os valores dos pais para serem usados em media_dinâmica
    Tc, sigma, custos_sigma = oleinik(f, custo, m) #calcula o lax_oleinik para todo i e parcialmente sigma.

    for j in range(conjunto_v.size):
        if f[j] - Tc[j] > 1e-13:  #se f[j] é maior que u[0]
            conjunto_v[j] = 1   
            f[j] = Tc[j]
        else:                    #se for menor ou igual
            conjunto_v[j] = 0    #Calcula se os vértices foram otimizados e atualiza o conjunto_v.
    

    if np.count_nonzero(conjunto_v) == 0 or iterada == 200:  
        return f, m, iterada                                #Condição de parada: Caso conjunto V tenha apenas zeros ou atinja o limite de iteradas.

    ciclos = []
    for j in range(len(conjunto_v)):
        if conjunto_v[j] == 1:
            k = j
            custo_din = 0
            for passagem in range(1, iterada+1):
                # Substitui a chamada peso_aresta por um acesso O(1)
                custo_din = (custo_din*(passagem-1) + custos_sigma[k])/passagem

                if sigma[k] == j:
                    ciclos.append(custo_din)
                
                k = sigma[k]

    if len(ciclos) > 0:
        m = min(m, min(ciclos))                                 #atualiza a constante.

    return floria_rec(custo, conjunto_v, f, m, iterada + 1)

def floria(custo, min, is_max_or_min = 'min'):
    """
    Creates all auxiliar estructure;
    Checks tag if it was supposed to give you the minimal or maximal ciclo
    
    """
    if is_max_or_min == 'min':
        conjunto_v = np.ones(shape=len(custo), dtype= np.int8)
        f = np.zeros(shape=len(custo))
        vetor, valor, iterada = floria_rec(custo, conjunto_v, f, min)
        return vetor, valor, iterada, custo
    
    elif is_max_or_min == 'max':
        custo_invertido = copy.deepcopy(custo)
        for vtx in custo_invertido:
            for edge in vtx:
                edge[1] = -edge[1]  #inverte os pesos do grafo
        
        conjunto_v = np.ones(shape=len(custo), dtype= np.int8)
        f = np.zeros(shape=len(custo))
        vetor, valor, iterada = floria_rec(custo_invertido, conjunto_v, f,0)
        return vetor, valor, iterada, custo_invertido

if __name__ == '__main__':
#Perceba que todo o custo deve ser negativado para tirar o max
    grafo = [
        [[3, 1]],  # Vértice 0 aponta para 1 e peso 20
        [[0, 100], [2, 1]],   # Vértice 1 aponta para 0 e peso 5
        [[1, 50]],  # Vértice 2 aponta para 3 e peso 10
        [[1, 1]],   # Vértice 3 aponta para 4 e peso 1
    ]
    draw.draw_weighted_graph_adj(grafo)
    
    vetor, valor, iterada, custo = floria(grafo, 100, is_max_or_min='min')
    grafo_critico = critic.grafoCritico_adj(custo, valor, vetor)

    draw.draw_weighted_graph_adj(grafo_critico)
    print(f"vetor: {vetor}, valor: {valor}, iterada: {iterada}")